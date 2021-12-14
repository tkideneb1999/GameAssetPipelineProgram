from enum import Enum
import json


class IOType(Enum):
    Mesh = 0
    Texture = 1
    Animation = 2


IOType_string_list = ["Mesh", "Texture", "Animation"]


class PipelineSettingsCreator:
    def __init__(self, configs_dir=None):
        self.configs = {}  # dict[str, dict[str, list[tuple[str, str]]]]
        # {configName
        #   inputs
        #       name, type
        #   outputs
        #       name, type
        # }
        self.export_data_types = []
        if configs_dir is not None:
            print(f"[GAPA] searching for configs at: {str(configs_dir)}")
            config_paths = list(configs_dir.glob("*.json"))
            for config_path in config_paths:
                data = self.load_config(config_path)
                inputs = []
                for i in data["input"]["inputs"]:
                    inputs.append((i["inputName"], i["type"]))
                outputs = []
                for o in data["output"]["outputs"]:
                    outputs.append((o["outputName"], o["type"]))
                print(f"[GAPA] Inputs: {inputs}")
                print(f"[GAPA] Outputs: {outputs}")
                self.add_configuration(data["name"], inputs, outputs)

        # Additional settings to be processed by the DCC Application
        self.settings = {}  # dict[str, dict]
        # {additional GUI Name
        #   {"type": type
        #    "data": data
        #   }
        # }
        self.has_set_outputs = False
        self.export_all = False

    def load_config(self, file_path) -> dict:
        """
        :param file_path: Path object to config file
        :return: data read from config file
        """
        data = {}
        with file_path.open("r", encoding="utf-8") as f:
            data = json.loads(f.read())
        return data


    # def add_output_config(self, name: str, outputs: list[tuple[str, str]]) -> None:
    #     """
    #     Add an output configuration for the pipeline step the program is part of
    #     :param name: name of the configuration
    #     :param outputs: list of tuples containing name[0] of the output and type[1]
    #     """
    #     self.settings["outputConfigs"][name] = outputs

    # def add_input_config(self, name: str, inputs: list[tuple[str, str]]) -> None:
    #     """
    #     Add an input configuration for the pipeline step the program is part of
    #     :param name: name of the configuration
    #     :param inputs: list of tuples containing name[0] of the input and type[1]
    #     """
    #     self.settings["inputConfigs"][name] = inputs

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

    def add_combobox_selection(self, name, entries) -> None:
        # name: str, entries: list[str]
        """
        Adds an additional combobox to the pipeline step GUI
        :param name: name of the combobox
        :param entries: entries added to the combobox
        """
        combobox_dict = {"type": "combobox",
                         "data": entries}
        self.settings[name] = combobox_dict

    def add_checkbox(self, name, default_value=False) -> None:
        # name: str, default_value=False
        """
        Adds an additional checkbox to the pipeline step GUI
        :param name: name of the checkbox
        :param default_value: default value of the combobox
        """
        checkbox_dict = {"type": "checkbox",
                         "data": default_value}
        self.settings[name] = checkbox_dict
