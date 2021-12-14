import json
import os
from pathlib import Path

import pluginAPI

import xNormal


def get_file_path() -> Path:
    return Path(os.path.abspath(__file__))


def run(import_data: dict, export_data: dict, settings: dict, config_name: str) -> None:

    # Set xNormal Path
    xNormal_path = Path(settings["global_settings"]["exe path"])
    if not xNormal_path.exists():
        print(f"[xNormal Plugin] exe Path does not exist: {str(xNormal_path)}")
        return
    if not xNormal_path.is_file():
        print(f"[xNormal Plugin] exe Path is not a file: {str(xNormal_path)}")

    xNormal.path = str(xNormal_path)

    # Load Config
    config_path = get_file_path().parent / "Configs" / f"{config_name}.json"
    config_data = {}
    with config_path.open("r", encoding="utf-8") as f:
        config_data = json.loads(f.read())

    gen_opts = {
        "width": settings["asset_settings"]["Width"],
        "height": settings["asset_settings"]["height"],
        "edge_padding": settings["asset_settings"]["edge_padding"],
        "bucket_size": settings["asset_settings"]["Bucket Size"],

        "aa": settings["asset_settings"]["Antialiasing"]
    }

    for output_set in export_data:
        for uid in export_data[output_set]:
            output_name = export_data[output_set][uid][0]
            file_path = export_data[output_set][uid][1]
            # TODO: enable different map generators based on output name

    print("[xNormal Plugin] Running xNormal")

    # TODO: When finished rename generated files according to naming convention


def register_settings() -> pluginAPI.PluginSettings:
    config_path = get_file_path().parent / "Configs"
    config_folder_exists = config_path.exists()
    print(f"ConfigPath exists: {config_folder_exists}, at: {config_path}")
    settings = pluginAPI.PluginSettings(config_dir=config_path)
    settings.set_export_data_types(["tga", "png", "exr"])

    # Global Settings
    settings.add_lineedit("exe path", pluginAPI.SettingsEnum.GLOBAL)

    # Pipeline Settings


    # Asset Settings
    settings.add_combobox("Width", pluginAPI.SettingsEnum.ASSET, ["16", "32", "64", "128", "256", "512", "1024", "2048",
                                                                  "4096"])
    settings.add_combobox("Height", pluginAPI.SettingsEnum.ASSET, ["16", "32", "64", "128", "256", "512", "1024",
                                                                   "2048", "4096"])
    settings.add_combobox("Antialiasing", pluginAPI.SettingsEnum.ASSET, ["1x", "2x", "4x"])
    settings.add_combobox("Bucket Size", pluginAPI.SettingsEnum.ASSET, ["16", "32", "64", "128", "256", "512"])
    settings.add_lineedit("Edge Padding", pluginAPI.SettingsEnum.ASSET, default_value="1")
    settings.add_lineedit("Max Ray Distance Front", pluginAPI.SettingsEnum.ASSET, "50")
    settings.add_lineedit("Max Ray Distance Back", pluginAPI.SettingsEnum.ASSET, "50")

    return settings
