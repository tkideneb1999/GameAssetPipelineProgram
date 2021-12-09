from . import xNormalPlugin
import pluginAPI


def run(settings: dict) -> None:
    print("[xNormal Plugin] Running xNormal")
    pass


def register_settings() -> pluginAPI.PluginSettings:
    settings = pluginAPI.PluginSettings()
    settings.add_lineedit("exe path", pluginAPI.SettingsEnum.GLOBAL)
    settings.add_combobox("testCombo", pluginAPI.SettingsEnum.GLOBAL, ["test1", "test2", "test3"])
    settings.add_checkbox("woahCheckbox", pluginAPI.SettingsEnum.GLOBAL)

    settings.add_combobox("Wup", pluginAPI.SettingsEnum.PIPELINE, ["w", "a", "s", "d"])

    settings.add_combobox("Wop", pluginAPI.SettingsEnum.ASSET, ["w", "o", "s"])

    return settings
