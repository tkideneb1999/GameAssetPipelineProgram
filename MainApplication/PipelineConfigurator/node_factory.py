from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from .nodegraph import BaseNode


def draw_square_port(painter, rect, info):
    painter.save()

    # mouse over port color.
    if info['hovered']:
        color = qtg.QColor(14, 45, 59)
        border_color = qtg.QColor(136, 255, 35, 255)
    # port connected color.
    elif info['connected']:
        color = qtg.QColor(195, 60, 60)
        border_color = qtg.QColor(200, 130, 70)
    # default port color
    else:
        color = qtg.QColor(*info['color'])
        border_color = qtg.QColor(*info['border_color'])

    pen = qtg.QPen(border_color, 1.8)
    pen.setJoinStyle(qtc.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()


def draw_triangle_port(painter, rect, info):
    painter.save()

    size = int(rect.height() / 2)
    triangle = qtg.QPolygonF()
    triangle.append(qtc.QPointF(-size, size))
    triangle.append(qtc.QPointF(0.0, -size))
    triangle.append(qtc.QPointF(size, size))

    transform = qtg.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info['hovered']:
        color = qtg.QColor(14, 45, 59)
        border_color = qtg.QColor(136, 255, 35)
    # port connected color.
    elif info['connected']:
        color = qtg.QColor(195, 60, 60)
        border_color = qtg.QColor(200, 130, 70)
    # default port color
    else:
        color = qtg.QColor(*info['color'])
        border_color = qtg.QColor(*info['border_color'])

    pen = qtg.QPen(border_color, 1.8)
    pen.setJoinStyle(qtc.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()


PORT_DATA_TYPE_MAP = {
    "texture": draw_square_port,
    "tga": draw_square_port,
    "tiff": draw_square_port,
    "png": draw_square_port,
    "jpg": draw_square_port,
    "mesh": draw_triangle_port,
    "fbx": draw_triangle_port,
    "obj": draw_triangle_port,
}


class PipelineNodeBase(BaseNode):
    settings_template = {}
    configs = {}
    export_all = False
    has_set_outputs = False
    program = "Program"
    export_data_types = []

    def __init__(self):
        super(PipelineNodeBase, self).__init__()
        self.set_port_deletion_allowed(True)

        self.input_uid_counter = 0
        self.output_uid_counter = 0
        self.settings_values = {}
        self.current_config = None

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
            self.current_config = list(self.configs.keys())[0]
            self.config_selected(self.current_config)

    def get_settings(self):
        return self.settings_values

    def get_settings_template(self):
        return self.settings_template

    def get_config_names(self):
        return list(self.configs.keys())

    def get_config_data(self, config_name: str) -> dict:
        return self.configs.get(config_name)

    def get_current_config_data(self) -> dict:
        return self.configs.get(self.current_config)

    def get_uid(self):
        return self.model.uid

    def set_uid(self, uid: str):
        self.model.uid = uid

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
        self.delete_all_inputs()
        self.delete_all_outputs()
        for i in config_data["inputs"]:
            if not self.export_data_types:
                painter_func = None
            else:
                painter_func = PORT_DATA_TYPE_MAP.get(i[1])
            port = self.add_input(i[0], painter_func=painter_func)
            port.data_type = i[1]
        for o in config_data["outputs"]:
            if not self.export_data_types:
                painter_func = None
            else:
                painter_func = PORT_DATA_TYPE_MAP.get(o[1])
            port = self.add_output(o[0], painter_func=painter_func)
            port.data_type = o[1]
        return True


def create_node_class(name: str,
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
        export_data_types = in_export_data_types

    return PipelineNode
