class PipelineSettingsCreator:
    def __init__(self):
        self.settings: dict[str, dict[str, list[tuple[str, str]]]] = {}
        # {configName
        #   inputs
        #       name, type
        #   outputs
        #       name, type
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
        self.settings[name] = io_dict
