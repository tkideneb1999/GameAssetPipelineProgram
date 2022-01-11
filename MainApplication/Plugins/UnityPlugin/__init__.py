import os
import shutil
from pathlib import Path

import pluginAPI


def get_file_path() -> Path:
    return Path(os.path.abspath(__file__))


def run(import_data: dict, export_data: dict, settings: dict, config_name: str) -> None:
    unity_assets_path = Path(settings["project"]["Project Directory"]) / "Assets"
    asset_dir = unity_assets_path / settings["asset_info"]["level"] / settings["asset_info"]["name"]
    print(f"Import Data: \n{import_data}")
    if not asset_dir.exists():
        asset_dir.mkdir(parents=True)
    for output_set in import_data:
        for output in import_data[output_set]:
            # Get import file path
            src_file_path: Path = import_data[output_set][output][1]

            # Get name of file without last suffix
            file_name = src_file_path.stem
            print(f"[UnityPlugin] importing file to Unity: {file_name}")
            # Strip version information
            filename_parts = file_name.split(".")
            del filename_parts[-1]
            file_name = "".join(filename_parts)
            # Strip output uid
            filename_parts = file_name.split("_")
            del filename_parts[0]
            file_name = "".join(filename_parts)
            file_name = settings["asset_info"]["name"] + "_" + file_name

            # Construct dst file path
            if output_set == "None":
                dst_file_path = asset_dir / f"{file_name}{src_file_path.suffix}"
            else:
                dst_file_path = asset_dir / output_set
                if not dst_file_path.exists():
                    dst_file_path.mkdir()
                dst_file_path = dst_file_path / f"{file_name}{src_file_path.suffix}"
            print(f"[UnityPlugin] dst_path: {str(dst_file_path)}")
            shutil.copyfile(src_file_path, dst_file_path)
    pass


def register_settings() -> pluginAPI.PluginSettings:
    settings = pluginAPI.PluginSettings()
    settings.add_lineedit("Project Directory", pluginAPI.SettingsEnum.PROJECT)
    return settings
