from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .nodegraph import BaseNode


def create_node_class(name: str, settings: dict, in_configs: dict, in_export_all: bool, in_has_set_outputs: bool):
    class PipelineNode(BaseNode):
        __identifier__ = f'pipeline.{name}'
        NODE_NAME = name
        settings_template = settings
        configs = in_configs
        export_all = in_export_all
        has_set_outputs = in_has_set_outputs

        def __init__(self):
            super(PipelineNode, self).__init__()
            self.set_port_deletion_allowed(True)
            self.settings_values = {}
            for settings_name in self.settings_template:
                data = self.settings_template[settings_name]["data"]
                data_type = type(data)
                if data_type is list:
                    default_value = data[0]
                elif data_type is None:
                    default_value = ""
                else:
                    default_value = data
                self.settings_values[settings_name] = default_value
            if not (self.configs == {}):
                first_config = list(self.configs.values())[0]
                for i in first_config["inputs"]:
                    self.add_input(i[0])
                for o in first_config["outputs"]:
                    self.add_output(o[0])

        def get_settings(self):
            return self.settings_values

        def get_settings_template(self):
            return self.settings_template

        def get_config_names(self):
            return list(self.configs.keys())

        def config_selected(self, config_name: str):
            if config_name not in list(self.configs.keys()):
                print(f"[GAPA] Config does not exist")
                return

            print(f"[GAPA] Changing IO for Node {self.name()}")
            inputs = self.inputs()
            for ip in inputs:
                inputs[ip].clear_connections()
                self.delete_input(ip)
            outputs = self.outputs()
            for op in outputs:
                outputs[op].clear_connections()
                self.delete_output(op)

            config = self.configs[config_name]

            for i in config["inputs"]:
                self.add_input(i[0])
            for o in config["outputs"]:
                self.add_output(o[0])

    return PipelineNode
