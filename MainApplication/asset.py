from pathlib import Path
import json

from pipeline import Pipeline


class Asset:
    def __init__(self, name: str, pipeline_dir=Path(), level="lvl01", tags=None, asset_type="Model", comment=""):
        if tags is None:
            tags = []
        self.name = name
        self.level = level
        self.tags = tags
        self.asset_type = asset_type
        self.pipeline_dir = pipeline_dir
        self.comment = comment

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
            "tags": self.tags,
            "comment": self.comment
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
            self.pipeline_dir = asset_data["pipeline_dir"]
            self.tags = asset_data["tags"]
            self.comment = asset_data["comment"]
