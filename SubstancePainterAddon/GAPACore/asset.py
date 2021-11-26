import json
import importlib
from pathlib import Path

from . import pipeline as pipelineModule

importlib.reload(pipelineModule)

pipeline_states = ["files missing", "not_started", "in_progress", "published"]


class Asset:
    def __init__(self, name: str, level: str, project_dir=None, pipeline_dir=None, tags=None, asset_type="Model", comment=""):
        if tags is None:
            tags = []
        self.name = name
        self.level = level
        self.tags = tags
        self.asset_type = asset_type
        self.pipeline_dir = pipeline_dir
        self.pipeline = pipelineModule.Pipeline()
        if pipeline_dir is None:
            if project_dir is None:
                raise Exception("If pipeline dir is None, expected project Dir to load Asset")
            self.load(project_dir)
        else:
            self.pipeline.load(pipeline_dir)
            self.set_initial_pipeline_progress()

        self.comment = comment
        self.workfile_paths = {}

    def set_initial_pipeline_progress(self) -> None:
        self.pipeline_progress = {}
        for step in self.pipeline.pipeline_steps:
            output_uids = []
            for o in step.outputs:
                output_uids.append(o.uid)
            output_set = self.create_new_output_set(output_uids)
            outputs_info = {"None": output_set}
            state = pipeline_states[0]
            if len(step.inputs) == 0:
                state = pipeline_states[1]
            step_asset_info = {"state": state,
                               "has_multi_outputs": step.has_set_outputs,
                               "output_info": outputs_info,
                               "old_version": False}
            self.pipeline_progress[step.uid] = step_asset_info
            # {step_uid: {
            #       "state": "files missing", -> progress on step, indicates if a user can begin or is finished
            #       "has_multi_outputs" : false
            #       "output_info": {
            #           "None": {
            #               output_uid: {
            #                   "published": False, -> whether output has been exported
            #                   "version": 0 -> current version of published asset, increases with new publish
            #                   }
            #               }
            #           }
            #       "old_version": False -> user works with old version
            #       }
            # }

    def init_output_sets(self, step_index: int, output_set_names: list) -> None:
        step_uid = self.pipeline.pipeline_steps[step_index].uid
        if not self.pipeline.pipeline_steps[step_index].has_set_outputs:
            print(f"[GAPA] Trying to create output sets for step {step_uid} where there should be none")
            return
        output_info = {}
        for output_set_name in output_set_names:
            output_set = {}
            for output in self.pipeline.pipeline_steps[step_index].outputs:
                output_set[output.uid] = {"published": False, "version": 0}
            output_info[output_set_name] = output_set
        self.pipeline_progress[step_uid]["output_info"] = output_info

    def create_new_output_set(self, output_uids: list) -> dict:
        output_set = {}
        for o in output_uids:
            output_set[o] = {"published": False,
                             "version": 0}
        return output_set

    def check_all_exported(self, step_uid: str) -> bool:
        all_exported = True
        step_data = self.pipeline_progress[step_uid]
        for output_set in step_data["output_info"]:
            for output in list(step_data["output_info"][output_set].values()):
                if output["published"] is False:
                    all_exported = False
                    break
        return all_exported

    def publish_step_file(self, step_uid: str,
                          output_uids: list,
                          export_suffix: str,
                          output_sets=None) -> dict:
        """
        Updates the pipeline progress and returns the
        export directory for the file to be published.
        :param step_uid: unique identifier of the pipeline step
        :param output_uids: unique identifiers of the outputs
        :param export_suffix: export suffix without .
        :param output_sets: names of the sets that will be exported
        :returns: relative path to the project directory the file should be saved in
        """

        # Set new Update and Old Version
        self.pipeline_progress[step_uid]["old_version"] = False
        has_multi_outputs = self.pipeline_progress[step_uid]["has_multi_outputs"]
        # Check if all Outputs are exported and update output data
        if has_multi_outputs:
            # Multi outputs (Outputs sets)
            if output_sets is not None:
                # TODO: Delete None Entry in PipelineProgress
                for output_set in output_sets:
                    output_set_data = {}
                    if output_set in self.pipeline_progress[step_uid]["output_info"]:
                        # Get Output Set if already exists
                        output_set_data = dict(self.pipeline_progress[step_uid]["output_info"][output_set])
                    else:
                        # Create new Set if nothing exists under that name
                        step_index = self.pipeline.get_step_index_by_uid(step_uid)
                        all_output_uids = []
                        for o in self.pipeline.pipeline_steps[step_index].outputs:
                            all_output_uids.append(o.uid)
                        output_set_data = self.create_new_output_set(all_output_uids)
                    for output_uid in output_uids:
                        # Is Published
                        output_set_data[output_uid]["published"] = True

                        # Update Version
                        version = output_set_data[output_uid]["version"] + 1
                        output_set_data[output_uid]["version"] = version
                    self.pipeline_progress[step_uid]["output_info"][output_set] = output_set_data
            else:
                print("[GAPA] Step has multi outputs but no sets were specified!")
        else:
            # No Multifile Outputs (Output Sets)
            output_set_data = dict(self.pipeline_progress[step_uid]["output_info"]["None"])
            for output_uid in output_uids:
                # Is Published
                output_set_data[output_uid]["published"] = True

                # Update Version
                version = output_set_data[output_uid]["version"] + 1
                output_set_data[output_uid]["version"] = version
            self.pipeline_progress[step_uid]["output_info"]["None"] = output_set_data

        all_exported = self.check_all_exported(step_uid)
        if all_exported is True:
            self.pipeline_progress[step_uid]["state"] = pipeline_states[3]
        else:
            self.pipeline_progress[step_uid]["state"] = pipeline_states[2]

        # Update next steps that they use an old version

        # Update Pipeline Progress
        # Check to which inputs the output is connected
        connected_inputs = self.pipeline.get_connected_inputs(output_uids)
        affected_steps = set()
        for i in connected_inputs:
            affected_steps.add(self.pipeline.get_step_uid_from_io(i))

        # For steps of connected inputs see if all inputs have outputs that have published files
        for a_step_uid in affected_steps:
            # Check if affected step is missing files
            if self.pipeline_progress[a_step_uid]["state"] == pipeline_states[0]:
                # Get step index
                a_step_index = self.pipeline.get_step_index_by_uid(a_step_uid)
                has_all_files = True
                for i in self.pipeline.pipeline_steps[a_step_index].inputs:
                    # Get output UID connected to input
                    connected_output_uid = self.pipeline.io_connections.get(i.uid)
                    # Skip if no Output is connected
                    if connected_output_uid is None:
                        continue

                    # Get Step UID of output
                    output_step_uid = self.pipeline.get_step_uid_from_io(connected_output_uid)

                    #   look up states of other inputs of step
                    if self.pipeline_progress[output_step_uid]["has_multi_outputs"]:
                        output_info = self.pipeline_progress[output_step_uid]["output_info"]
                        output_published = True
                        for output_set in output_info.values():
                            if not output_set[connected_output_uid]:
                                output_published = False
                                break
                    else:
                        output_published = self.pipeline_progress[output_step_uid]["output_info"]["None"][connected_output_uid]["published"]
                    if not output_published:
                        has_all_files = False

                # check if all inputs have files
                if has_all_files:
                    # if so set pipeline state to not_started
                    self.pipeline_progress[a_step_uid]["state"] = pipeline_states[1]
            else:
                self.pipeline_progress[a_step_uid]["old_version"] = True

        # Generate File Path
        step_index = self.pipeline.get_step_index_by_uid(step_uid)
        step_folder_name = self.pipeline.pipeline_steps[step_index].get_folder_name()
        if has_multi_outputs:
            file_paths = {}
            for output_set in self.pipeline_progress[step_uid]["output_info"]:
                output_set_data = {}
                for o in output_uids:
                    output_index = self.pipeline.pipeline_steps[step_index].get_io_index_by_uid(o)
                    if o == -1:
                        raise Exception("[GAPA] -1 is no Valid output index")
                    file_name = self.pipeline.pipeline_steps[step_index].outputs[output_index].get_file_name()
                    output_version = self.pipeline_progress[step_uid]["output_info"][output_set][o]["version"]
                    output_set_data[o] = Path() / self.level / self.name / step_folder_name / "export" / output_set / f"{file_name}.{output_version}.{export_suffix}"
                file_paths[output_set] = output_set_data
            return file_paths
        else:
            file_paths = {}
            for o in output_uids:
                output_index = self.pipeline.pipeline_steps[step_index].get_io_index_by_uid(o)
                if o == -1:
                    raise Exception("[GAPA] -1 is no Valid output index")

                file_name = self.pipeline.pipeline_steps[step_index].outputs[output_index].get_file_name()
                output_version = self.pipeline_progress[step_uid]["output_info"]["None"][o]["version"]
                file_paths[o] = (Path() / self.level / self.name / step_folder_name / "export" / f"{file_name}.{output_version}.{export_suffix}")
                return {"None": file_paths}

    def import_assets(self, step_index: int) -> tuple:
        """
        :param step_index: index of the pipeline step
        :returns: list of filepaths for assets to import
        """
        rel_asset_dir = Path() / self.level / self.name
        file_format = "fbx"  # TODO(Blender Addon): implement file type
        filepaths = {}
        for i in self.pipeline.pipeline_steps[step_index].inputs:
            # get connected output
            output_uid = self.pipeline.io_connections[i.uid]
            # reconstruct relative file path
            #   get step folder
            output_step_uid = self.pipeline.get_step_uid_from_io(output_uid)
            output_step_index = self.pipeline.get_step_index_by_uid(output_step_uid)
            folder_name = self.pipeline.pipeline_steps[output_step_index].get_folder_name()
            #   get file name of output
            output_index = self.pipeline.pipeline_steps[output_step_index].get_io_index_by_uid(output_uid)
            file_name = self.pipeline.pipeline_steps[output_step_index].outputs[output_index].get_file_name()
            if self.pipeline_progress[output_step_uid]["has_multi_outputs"]:
                for output_set in self.pipeline_progress[output_step_uid]["output_info"]:
                    version = self.pipeline_progress[output_step_uid]["output_info"][output_set][output_uid]["version"]
                    filepaths[output_set][output_uid] = (i.name, rel_asset_dir / folder_name / "export" / output_set / f"{file_name}.{version}.{file_format}")
            else:
                version = self.pipeline_progress[output_step_uid]["output_info"]["None"][output_uid]["version"]
                filepaths["None"] = {output_uid: (i.name, rel_asset_dir / folder_name / "export" / f"{file_name}.{version}.{file_format}")}
        return filepaths, self.pipeline.pipeline_steps[step_index].config, self.pipeline.pipeline_steps[step_index].additional_settings

    def save_work_file(self, step_uid: str, workfile_path: str) -> None:
        self.pipeline_progress[step_uid]["state"] = pipeline_states[2]
        self.workfile_paths[step_uid] = workfile_path

    def save(self, project_dir: Path) -> None:
        asset_dir = project_dir / self.level / self.name

        # Create Folder structure

        if not asset_dir.exists():
            # Create Asset Directories
            # Structure:
            #    Asset
            #        step
            #            workfiles
            #            export

            for step in self.pipeline.pipeline_steps:
                step_dir = asset_dir / step.get_folder_name()
                workfiles_dir = step_dir / "workfiles"
                print(f"[Asset Creation] Creating: {workfiles_dir}")
                workfiles_dir.mkdir(parents=True)
                export_dir = step_dir / "export"
                print(f"[Asset Creation] Creating: {export_dir}")
                export_dir.mkdir()

        asset_path = asset_dir / f"{self.name}.meta"
        if not asset_path.exists():
            if not asset_path.is_file():
                asset_path.touch()
        asset_data = {
            "name": self.name,
            "level": self.level,
            "type": self.asset_type,
            "pipeline_dir": str(self.pipeline_dir),
            "pipeline_progress": self.pipeline_progress,
            "tags": self.tags,
            "comment": self.comment,
            "workfile_paths": self.workfile_paths
        }

        with asset_path.open('w', encoding="utf-8") as f:
            f.write(json.dumps(asset_data, indent=4))
            f.close()

    def load(self, project_dir: Path) -> None:
        asset_path = project_dir / self.level / self.name / f"{self.name}.meta"
        if not asset_path.exists():
            if not asset_path.is_file():
                raise Exception("File does not exist!")
        with asset_path.open('r', encoding='utf-8') as f:
            data = f.read()
            asset_data = json.loads(data)
            self.name = asset_data["name"]
            self.level = asset_data["level"]
            self.asset_type = asset_data["type"]
            self.pipeline_dir = Path(asset_data["pipeline_dir"])
            self.pipeline.load(self.pipeline_dir)
            self.pipeline_progress = asset_data["pipeline_progress"]
            self.tags = asset_data["tags"]
            self.comment = asset_data["comment"]
            self.workfile_paths = asset_data["workfile_paths"]
