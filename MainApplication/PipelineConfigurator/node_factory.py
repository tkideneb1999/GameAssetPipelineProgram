from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from .nodegraph import BaseNode

from ..Core.pipeline import (PipelineStep, PipelineInput, PipelineOutput)
from . import port_draw_functions


class PipelineNodeBase(BaseNode):
    settings_template = {}
    configs = {}
    export_all = False
    has_set_outputs = False
    program = "Program"
    is_plugin = False
    export_data_types = []

    def __init__(self):
        super(PipelineNodeBase, self).__init__()
        self.set_port_deletion_allowed(True)

        self.input_uid_counter = 0
        self.output_uid_counter = 0

        self.current_config = None

        settings_values = {}

        for settings_name in self.settings_template:
            data = self.settings_template[settings_name]["data"]
            data_type = type(data)
            if data_type is list:
                default_value = data[0]
            elif data_type is None:
                default_value = ""
            else:
                default_value = data
            settings_values[settings_name] = default_value

        # Set Correct Static Model Data
        self.settings = settings_values
        self.model.program = self.program
        self.model.is_plugin = self.is_plugin
        self.model.has_set_outputs = self.has_set_outputs
        self.model.export_all = self.export_all

    def get_settings_template(self):
        return self.settings_template

    def get_config_names(self):
        return list(self.configs.keys())

    def get_config_data(self, config_name: str) -> dict:
        return self.configs.get(config_name)

    def get_current_config_data(self) -> dict:
        return self.configs.get(self.model.config)

    def get_current_config_name(self) -> str:
        return self.model.config

    def get_uid(self):
        return self.model.uid

    def set_uid(self, uid: str):
        self.model.uid = uid

    @property
    def settings(self) -> dict:
        return self.model.settings

    @settings.setter
    def settings(self, settings: dict):
        self.model.settings = settings

    def delete_input(self, port):
        port_obj = self.get_input(port)
        port_obj.clear_connections()
        super(PipelineNodeBase, self).delete_input(port)

    def delete_output(self, port):
        port_obj = self.get_output(port)
        port_obj.clear_connections()
        super(PipelineNodeBase, self).delete_output(port)

    def add_input(self, name='input', multi_input=False, display_name=True,
                  color=None, locked=False, painter_func=None):
        port = super(PipelineNodeBase, self).add_input(name=name,
                                                       multi_input=multi_input,
                                                       display_name=display_name,
                                                       color=color,
                                                       locked=locked,
                                                       painter_func=painter_func)
        port.set_uid(f"{self.get_uid()}.i{self.input_uid_counter}")
        self.input_uid_counter += 1
        return port

    def add_output(self, name='output', multi_output=True, display_name=True,
                   color=None, locked=False, painter_func=None):
        port = super(PipelineNodeBase, self).add_output(name=name,
                                                        multi_output=multi_output,
                                                        display_name=display_name,
                                                        color=color,
                                                        locked=locked,
                                                        painter_func=painter_func)
        port.set_uid(f"{self.get_uid()}.o{self.output_uid_counter}")
        if self.export_data_types:
            port.data_type = self.export_data_types[0]
        self.output_uid_counter += 1
        return port

    def rename_input(self, old_name, new_name):
        # Get all port names and connections of ports
        ports = self.inputs()
        if new_name in ports:
            return False
        data = {}
        for p in ports:
            painter_func = None
            if hasattr(ports[p].view, '_port_painter'):
                painter_func = ports[p].view._port_painter
            data[p] = {"connections": ports[p].connected_ports(),
                       "painter_func": painter_func}
            # Delete all ports
            self.delete_input(p)
        # Create new ports with names corresponding to previous order
        for p in data:
            name = p
            if name == old_name:
                name = new_name

            port = self.add_input(name, painter_func=data[p]["painter_func"])
            for c in data[p]["connections"]:
                port.connect_to(c)
        return True

    def rename_output(self, old_name, new_name):
        # Get all port names and connections of ports
        ports = self.outputs()
        if new_name in ports:
            return False
        data = {}
        for p in ports:
            painter_func = None
            if hasattr(ports[p].view, '_port_painter'):
                painter_func = ports[p].view._port_painter
            data[p] = {"connections": ports[p].connected_ports(),
                       "painter_func": painter_func}
            # Delete all ports
            self.delete_output(p)
        # Create new ports with names corresponding to previous order
        for p in data:
            name = p
            if name == old_name:
                name = new_name
            port = self.add_output(name, painter_func=data[p]["painter_func"])
            for c in data[p]["connections"]:
                port.connect_to(c)
        return True

    def delete_all_inputs(self):
        inputs = self.inputs()
        for ip in inputs:
            self.delete_input(ip)

    def delete_all_outputs(self):
        outputs = self.outputs()
        for op in outputs:
            self.delete_output(op)

    def config_selected(self, config_name: str) -> bool:
        config_data = self.configs.get(config_name)
        if config_data is None:
            return False
        self.model.config = config_name
        self.delete_all_inputs()
        self.delete_all_outputs()
        for i in config_data["inputs"]:
            if not self.export_data_types:
                painter_func = None
            else:
                painter_func = port_draw_functions.PORT_DATA_TYPE_MAP.get(i[1])
            port = self.add_input(i[0], painter_func=painter_func)
            port.data_type = i[1]
        for o in config_data["outputs"]:
            if not self.export_data_types:
                painter_func = None
            else:
                painter_func = port_draw_functions.PORT_DATA_TYPE_MAP.get(o[1])
            port = self.add_output(o[0], painter_func=painter_func)
            if not self.export_data_types:
                port.data_type = o[1]
        return True

    def to_pipeline_data(self):
        step = PipelineStep(self.model.uid)
        step.name = self.name()
        step.program = self.program
        step.config = self.model.config
        step.is_plugin = self.is_plugin
        step.has_set_outputs = self.has_set_outputs
        step.export_all = self.export_all
        step.additional_settings = self.settings

        connections = {}
        for i in self.input_ports():
            step_input = PipelineInput(i.model.uid)
            step_input.name = i.model.name
            step.inputs.append(step_input)
            if not i.connected_ports():
                continue
            connected_port = i.connected_ports()[0]
            connections[i.model.uid] = connected_port.model.uid
        for o in self.model.output_ports:
            step_output = PipelineOutput(self.model.output_ports[o].uid)
            step_output.name = o
            step_output.data_type = self.model.output_ports[o].data_type
            step.outputs.append(step_output)

        return step, connections


def create_node_class(name: str,
                      in_is_plugin: bool,
                      settings: dict,
                      in_configs: dict,
                      in_export_all: bool,
                      in_has_set_outputs: bool,
                      in_export_data_types: list):
    class PipelineNode(PipelineNodeBase):
        __identifier__ = f'pipeline.{name.strip(" ")}'
        NODE_NAME = name
        settings_template = settings
        configs = in_configs
        export_all = in_export_all
        has_set_outputs = in_has_set_outputs
        program = name
        is_plugin = in_is_plugin
        export_data_types = in_export_data_types

    return PipelineNode
