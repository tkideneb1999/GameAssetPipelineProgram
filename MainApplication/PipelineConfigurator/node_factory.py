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

    def config_selected(self, config_name: str) -> bool:
        if config_name not in list(self.configs.keys()):
            print(f"[GAPA] Config does not exist")
            return False

        self.current_config = config_name
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
            draw_square_func = PORT_DATA_TYPE_MAP.get(i[1])
            self.add_input(i[0], painter_func=draw_square_func)
        for o in config["outputs"]:
            draw_tri_func = PORT_DATA_TYPE_MAP.get(o[1])
            self.add_output(o[0], painter_func=draw_tri_func)
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
