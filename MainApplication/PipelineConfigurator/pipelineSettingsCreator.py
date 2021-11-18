class PipelineSettingsCreator:
    def __init__(self):
        self.configs: dict[str, dict[str, list[tuple[str, str]]]] = {}
        # {configName
        #   inputs
        #       name, type
        #   outputs
        #       name, type
        # }
        self.settings: dict[str, dict] = {}
        # {additional GUI Name
        #   {"type": type
        #    "data": data
        #   }
        # }

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

    def add_configuration(self, name: str, inputs: list[tuple[str, str]], outputs: list[tuple[str, str]]) -> None:
        """
        Adds a configuration to the settings
        :param name: name of the configuration
        :param inputs: list of tuples containing name[0] of the input and type[1]
        :param outputs: list of tuples containing name[0] of the output and type[1]
        """
        io_dict = {"inputs": inputs, "outputs": outputs}
        self.configs[name] = io_dict

    def add_combobox_selection(self, name: str, entries: list[str]) -> None:
        """
        Adds an additional combobox to the pipeline step GUI
        :param name: name of the combobox
        :param entries: entries added to the combobox
        """
        combobox_dict = {"type": "combobox",
                         "data": entries}
        self.settings[name] = combobox_dict

    def add_checkbox(self, name: str, default_value=False) -> None:
        """
        Adds an additional checkbox to the pipeline step GUI
        :param name: name of the checkbox
        :param default_value: default value of the combobox
        """
        checkbox_dict = {"type": "checkbox",
                         "data": default_value}
        self.settings[name] = checkbox_dict
