from pathlib import Path
import json

from .pipeline import Pipeline

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
                               "new_update": False,
                               "old_version": False}
            self.pipeline_progress[step.uid] = step_asset_info

    def publish_step_file(self, step_uid: str, output_uid: str) -> None:
        # Set new Update and Old Version
        self.pipeline_progress[step_uid]["new_update"] = True
        self.pipeline_progress[step_uid]["old_version"] = False

        # Check if all Outputs are exported
        outputs_info = dict(self.pipeline_progress[step_uid]["output_info"])
        output_info = outputs_info[output_uid]
        output_info["published"] = True
        output_info["version"] += 1
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
        self.update_next_steps(pipeline, step_uid, "old_version", True)

    # Recursively update next steps
    def update_next_steps(self, pipeline: Pipeline, step_uid: str, data_type: str, value) -> None:
        next_step = pipeline.get_next_step_uid(step_uid)
        if next_step == "":
            return
        self.pipeline_progress[next_step][data_type] = value
        self.update_next_steps(pipeline, next_step, data_type, value)

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
                step_dir = asset_dir / f"{step.uid}_{step.name}"
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
