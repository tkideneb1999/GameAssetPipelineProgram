import os
from pathlib import Path

from . import xNormalPlugin
import pluginAPI


def run(paths: list, settings: dict, config_name: str) -> None:
    print("[xNormal Plugin] Running xNormal")


def register_settings() -> pluginAPI.PluginSettings:
    config_path = Path(os.path.abspath(__file__)).parent / "Configs"
    config_folder_exists = config_path.exists()
    print(f"ConfigPath exists: {config_folder_exists}, at: {config_path}")
    settings = pluginAPI.PluginSettings(config_dir=config_path)
    settings.add_lineedit("exe path", pluginAPI.SettingsEnum.GLOBAL)
    settings.add_combobox("testCombo", pluginAPI.SettingsEnum.GLOBAL, ["test1", "test2", "test3"])
    settings.add_checkbox("woahCheckbox", pluginAPI.SettingsEnum.GLOBAL)

    settings.add_combobox("Wup", pluginAPI.SettingsEnum.PIPELINE, ["w", "a", "s", "d"])

    settings.add_combobox("Wop", pluginAPI.SettingsEnum.ASSET, ["w", "o", "s"])

    return settings
