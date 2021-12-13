from enum import Enum
from pathlib import Path
import json


class SettingsEnum(Enum):
    GLOBAL = 0
    PIPELINE = 1
    ASSET = 2


class PluginSettings:
    def __init__(self, config_dir=None):
        self.configs = {}
        if config_dir is not None:
            self.load_configs(config_dir)
        self.global_settings = {}
        self.pipeline_settings = {}
        self.asset_settings = {}
        self.has_set_outputs = False
        self.export_all = True

    def add_lineedit(self, name: str, space: SettingsEnum, default_value=None):
        """
        Adds a line edit field to the specified space
        :param name: name of the line edit field
        :param space: where the line edit will be used (SettingsEnum.GLOBAL, SettingsEnum.PIPELINE, SettingsEnum.ASSET
         available)
         will be either put in the settings tab, when configuring the pipeline or when the pipeline step is activated
        :param default_value: default value of the line edit
        """
        settings_data = {"type": "lineedit", "data": default_value}
        self.add_settings(name, space, settings_data)

    def add_combobox(self, name: str, space: SettingsEnum, data: list):
        """
        Adds a line edit field to the specified space
        :param name: name of the combobox field
        :param space: where the combobox will be used (SettingsEnum.GLOBAL, SettingsEnum.PIPELINE, SettingsEnum.ASSET
         available)
         will be either put in the settings tab, when configuring the pipeline or when the pipeline step is activated
        :param data: individual entries as a list first one will be the default
        """
        settings_data = {"type": "combobox", "data": data}
        self.add_settings(name, space, settings_data)

    def add_checkbox(self, name: str, space: SettingsEnum, default_value=False):
        """
        Adds a line edit field to the specified space
        :param name: name of the checkbox field
        :param space: where the checkbox will be used (SettingsEnum.GLOBAL, SettingsEnum.PIPELINE, SettingsEnum.ASSET
         available)
         will be either put in the settings tab, when configuring the pipeline or when the pipeline step is activated
        :param default_value: default value of the checkbox
        """
        settings_data = {"type": "checkbox", "data": default_value}
        self.add_settings(name, space, settings_data)

    def load_configs(self, config_dir: Path):
        print(f"[GAPA] searching for configs at: {str(config_dir)}")
        config_paths = list(config_dir.glob("*.json"))
        for config_path in config_paths:
            data = {}
            with config_path.open("r", encoding="utf-8") as f:
                data = json.loads(f.read())
            inputs = []
            for i in data["input"]["inputs"]:
                inputs.append((i["inputName"], i["type"]))
            outputs = []
            for o in data["output"]["outputs"]:
                outputs.append((o["outputName"], o["type"]))
            self.add_configuration(data["name"], inputs, outputs)
            # TODO: Add ability to set default settings for Pipeline and asset settings

    def add_configuration(self, name, inputs, outputs) -> None:
        # name: str, inputs: list[tuple[str, IOType]], outputs: list[tuple[str, IOType]]
        """
        Adds a configuration to the settings
        :param name: name of the configuration
        :param inputs: list of tuples containing name[0] of the input and type[1]
        :param outputs: list of tuples containing name[0] of the output and type[1]
        """

        for i in range(len(inputs)):
            inputs[i] = (inputs[i][0], inputs[i][1])
            print(f"[GAPA] Added Input {inputs[i][0]} with type {inputs[i][1]} to config")
        for o in range(len(outputs)):
            outputs[o] = (outputs[o][0], outputs[o][1])
            print(f"[GAPA] Added Input {outputs[o][0]} with type {outputs[o][1]} to config")
        io_dict = {"inputs": inputs, "outputs": outputs}
        self.configs[name] = io_dict

    def add_settings(self, name: str, space: SettingsEnum, settings_data: dict):
        if space == SettingsEnum.GLOBAL:
            self.global_settings[name] = settings_data
        elif space == SettingsEnum.PIPELINE:
            self.pipeline_settings[name] = settings_data
        elif space == SettingsEnum.ASSET:
            self.asset_settings[name] = settings_data
