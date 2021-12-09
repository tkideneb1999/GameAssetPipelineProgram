import pluginAPI


def run(settings: dict) -> None:
    pass


def register_settings() -> pluginAPI.PluginSettings:
    settings = pluginAPI.PluginSettings()
    settings.add_lineedit("exe path", pluginAPI.SettingsEnum.GLOBAL)
    settings.add_combobox("testCombo2sda", pluginAPI.SettingsEnum.GLOBAL, ["test1", "test2", "test3"])
    settings.add_checkbox("woahCheckboxasdas", pluginAPI.SettingsEnum.GLOBAL)
    return settings