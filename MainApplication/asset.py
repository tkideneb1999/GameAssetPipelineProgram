import json
from pathlib import Path

from pipeline import Pipeline

pipeline_states = ["files missing", "not_started", "in_progress", "published"]


class Asset:
    def __init__(self, name: str, level, pipeline_dir=None, tags=None, asset_type="Model", comment=""):
        if tags is None:
            tags = []
        self.name = name
        self.level = level
        self.tags = tags
        self.asset_type = asset_type

        if pipeline_dir is None:
            self.pipeline_dir = Path()
        else:
            self.pipeline_dir = pipeline_dir

        if pipeline_dir is None:
            self.pipeline_progress = {}
        else:
            self.pipeline_progress = {}
            self.set_initial_pipeline_progress()

        self.comment = comment
        self.workfile_paths = {}

    def set_initial_pipeline_progress(self):
        pipeline = Pipeline()
        pipeline.load(self.pipeline_dir)
        for step in pipeline.pipeline_steps:
            outputs_info = {}
            for output in step.outputs:
                outputs_info[output.uid] = {"published": False,
                                            "version": 0}
            state = pipeline_states[0]
            if len(step.inputs) == 0:
                state = pipeline_states[1]
            step_asset_info = {"state": state,
                               "output_info": outputs_info,
                               "old_version": False}
            self.pipeline_progress[step.uid] = step_asset_info
            # {step_uid: {
            #       "state": "files missing", -> progress on step, indicates if a user can begin or is finished
            #       "output_info": {
            #           output_uid: {
            #               "published": False, -> whether output has been exported
            #               "version": 0 -> current version of published asset, increases with new publish
            #               }
            #           }
            #       "old_version": False -> user works with old version
            #       }
            # }

    def publish_step_file(self, step_uid: str, output_uid: str, export_suffix: str) -> Path:
        """
        Updates the pipeline progress and returns the
        export directory for the file to be published.
        :param step_uid: unique identifier of the pipeline step
        :param output_uid: unique identifier of the output
        :param export_suffix: export suffix without .
        :returns: relative path to the project directory the file should be saved in
        """

        # Set new Update and Old Version
        self.pipeline_progress[step_uid]["old_version"] = False

        # Check if all Outputs are exported
        outputs_info = dict(self.pipeline_progress[step_uid]["output_info"])
        output_info = outputs_info[output_uid]
        output_info["published"] = True
        output_version = output_info["version"] + 1
        output_info["version"] = output_version
        print(output_info)
        all_exported = True
        for i in list(outputs_info.values()):
            if i["published"] is False:
                all_exported = False
                break
        if all_exported is True:
            self.pipeline_progress[step_uid]["state"] = pipeline_states[3]
        else:
            self.pipeline_progress[step_uid]["state"] = pipeline_states[2]

        # Update next steps that they use an old version
        pipeline = Pipeline()
        pipeline.load(self.pipeline_dir)

        # Update Pipeline Progress
        # TODO(Asset): Update based on connected inputs
        # Check to which inputs the output is connected
        outputs = list(pipeline.io_connections.values())
        output_indices = []
        for i in range(len(outputs)):
            if outputs[i] == output_uid:
                output_indices.append(i)
        inputs = list(pipeline.io_connections.keys())
        connected_inputs = []
        affected_steps = set()
        for i in output_indices:
            connected_inputs.append(inputs[i])
            # get all steps of inputs
            affected_steps.add(pipeline.get_step_uid_from_io(inputs[i]))

        # For steps of connected inputs see if all inputs have outputs that have published files
        for a_step_uid in affected_steps:
            if self.pipeline_progress[a_step_uid]["state"] == pipeline_states[0]:
                a_step_index = pipeline.get_step_index_by_uid(a_step_uid)
                has_all_files = True
                for i in pipeline.pipeline_steps[a_step_index].inputs:
                    connected_output_uid = pipeline.io_connections.get(i.uid)
                    if connected_output_uid is None:
                        continue
                    output_step_uid = pipeline.get_step_uid_from_io(connected_output_uid)

                    #   look up states of other inputs of step
                    output_published = self.pipeline_progress[output_step_uid]["output_info"][connected_output_uid]["published"]
                    if not output_published:
                        has_all_files = False

                # check if all inputs have files
                if has_all_files:
                    # if so set pipeline state to not_started
                    self.pipeline_progress[a_step_uid]["state"] = pipeline_states[1]
            else:
                self.pipeline_progress[a_step_uid]["old_version"] = True

        # Generate File Path
        step_index = pipeline.get_step_index_by_uid(step_uid)
        output_index = pipeline.pipeline_steps[step_index].get_io_index_by_uid(output_uid)
        if output_index == -1:
            raise Exception("[GAPA] -1 is no Valid output index")
        step_folder_name = pipeline.pipeline_steps[step_index].get_folder_name()
        print(f"[GAPA] step index of {step_uid}: {step_index}\n       output index of {output_uid}: {output_index}")
        file_name = pipeline.pipeline_steps[step_index].outputs[output_index].get_file_name()
        save_dir = Path() / self.level / self.name / step_folder_name / "export" / f"{file_name}.{output_version}.{export_suffix}"
        return save_dir

    def import_assets(self, step_index: int) -> list[Path]:
        """
        :param step_uid: unique id of step
        :returns: list of filepaths for assets to import
        """
        pipeline = Pipeline()
        pipeline.load(self.pipeline_dir)
        rel_asset_dir = Path() / self.level / self.name
        filetype = "fbx"  # TODO(Blender Addon): implement file type
        filepaths = []
        for i in pipeline.pipeline_steps[step_index].inputs:
            # get connected output
            output_uid = pipeline.io_connections[i.uid]
            # reconstruct relative file path
            #   get step folder
            output_step_uid = pipeline.get_step_uid_from_io(output_uid)
            output_step_index = pipeline.get_step_index_by_uid(output_step_uid)
            folder_name = pipeline.pipeline_steps[output_step_index].get_folder_name()
            #   get file name of output
            output_index = pipeline.pipeline_steps[output_step_index].get_io_index_by_uid(output_uid)
            file_name = pipeline.pipeline_steps[output_step_index].outputs[output_index].get_file_name()
            version = self.pipeline_progress[output_step_uid]["output_info"][output_uid]["version"]
            filepaths.append(rel_asset_dir / folder_name / "export" / f"{file_name}.{version}.{filetype}")
        return filepaths

    def save_work_file(self, step_uid: str, workfile_path: str) -> None:
        self.pipeline_progress[step_uid]["state"] = pipeline_states[2]
        self.workfile_paths[step_uid] = workfile_path

    def save(self, project_dir: Path) -> None:
        asset_dir = project_dir / self.level / self.name

        # Create Folder structure

        if not asset_dir.exists():
            pipeline = Pipeline()
            pipeline.load(self.pipeline_dir)

            # Create Asset Directories
            # Structure:
            #    Asset
            #        step
            #            workfiles
            #            export

            for step in pipeline.pipeline_steps:
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
            self.pipeline_progress = asset_data["pipeline_progress"]
            self.tags = asset_data["tags"]
            self.comment = asset_data["comment"]
            self.workfile_paths = asset_data["workfile_paths"]
