from . import xNormalPlugin
import pluginAPI


def run(settings: dict) -> None:
    pass


def register_settings() -> pluginAPI.PluginSettings:
    settings = pluginAPI.PluginSettings()
    settings.add_lineedit("exe path", pluginAPI.SettingsEnum.GLOBAL)
    settings.add_combobox("testCombo", pluginAPI.SettingsEnum.GLOBAL, ["test1", "test2", "test3"])
    settings.add_checkbox("woahCheckbox", pluginAPI.SettingsEnum.GLOBAL)

    settings.add_combobox("Wup", pluginAPI.SettingsEnum.PIPELINE, ["w", "a", "s", "d"])

    return settings
