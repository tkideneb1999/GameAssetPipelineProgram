import functools

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .nodegraph.nodes.base_node import BaseNode

from ..localSettingsView import LocalSettingsView
from .properties_bin_port_GUI import Ui_Port
from . import node_factory

NO_NODE_SELECTED_TEXT = "--No Node selected--"


class PropertiesBin(qtw.QWidget):
    
    def __init__(self, parent=None):
        super(PropertiesBin, self).__init__(parent)
        self.setMinimumSize(300, 300)
        self.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        self.scroll_area = qtw.QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.v_Layout = qtw.QVBoxLayout(self)
        self.v_Layout.setContentsMargins(0, 0, 0, 0)
        self.v_Layout.addWidget(self.scroll_area)
        self.setLayout(self.v_Layout)

        self.scrollable_widget = qtw.QWidget()

        self.s_layout = qtw.QVBoxLayout(self.scrollable_widget)
        self.s_layout.addStretch()
        self.scrollable_widget.setLayout(self.s_layout)
        self.scroll_area.setWidget(self.scrollable_widget)

        self.node_selected_label = qtw.QLabel(NO_NODE_SELECTED_TEXT)
        self.node_name_label = qtw.QLineEdit(self)
        self.node_name_label.editingFinished.connect(self.on_name_changed)
        self.node_name_label.hide()

        self.config_combo_box = qtw.QComboBox()
        self.config_combo_box.currentTextChanged.connect(self.on_config_changed)
        self.config_combo_box.hide()

        # Header
        self.s_layout.insertWidget(self.__next_to_last(), self.node_selected_label)
        self.s_layout.insertWidget(self.__next_to_last(), self.node_name_label)
        self.s_layout.insertWidget(self.__next_to_last(), self.config_combo_box)

        self.settings_view: LocalSettingsView = None
        self.ports_view: PortsView = None
        self.current_node: node_factory.PipelineNodeBase = None

    def node_selected(self, node: node_factory.PipelineNodeBase):
        if self.current_node is not None:
            if node.id == self.current_node.id:
                return
        self.node_selected_label.hide()
        self.node_name_label.setText(node.name())
        self.node_name_label.show()
        self.config_combo_box.clear()

        identifier = node.__identifier__
        node_group = identifier.split(".")[0]
        if not node_group == 'pipeline':
            return
        if self.current_node is not None:
            self.current_node.settings_values = self.settings_view.get_settings()
        self.current_node = node
        uses_configs = False
        if not node.configs == {}:
            self.config_combo_box.setEnabled(True)
            self.config_combo_box.blockSignals(True)
            self.config_combo_box.addItems(list(node.configs.keys()))
            self.config_combo_box.setCurrentText(node.current_config)
            self.config_combo_box.blockSignals(False)
            self.config_combo_box.show()
            uses_configs = True
        else:
            self.config_combo_box.setEnabled(False)

        # Settings View
        if self.settings_view is not None:
            self.settings_view.deleteLater()
        self.settings_view = LocalSettingsView(node.settings_template,
                                               saved_settings=node.settings_values,
                                               tab_side=qtw.QTabWidget.North,
                                               parent=self)
        self.node_name_label.setText(node.name())
        self.s_layout.insertWidget(self.__next_to_last(), self.settings_view)

        # Ports View
        if self.ports_view is not None:
            self.ports_view.deleteLater()
        self.ports_view = PortsView(config_used=uses_configs,
                                    data_types=node.export_data_types,
                                    node=self.current_node,
                                    parent=self)
        # TODO: Save Port data in Node
        config_data = self.current_node.get_config_data(node.current_config)
        # self.ports_view.on_config_selected(config_data)
        self.s_layout.insertWidget(self.__next_to_last(), self.ports_view)

    def node_deleted(self, nodes):
        for n in nodes:
            if n == self.current_node.id:
                # Settings View
                self.settings_view.deleteLater()
                self.settings_view = None

                # Ports View
                self.ports_view.deleteLater()
                self.ports_view = None

                # Node
                self.current_node = None

                self.node_name_label.hide()
                self.node_selected_label.show()
                self.config_combo_box.clear()
                self.config_combo_box.hide()
                break

    def on_name_changed(self):
        if self.current_node is None:
            return
        name = self.node_name_label.text()
        self.current_node.set_name(name)

    def on_config_changed(self, name):
        if self.current_node is None:
            return
        result = self.current_node.config_selected(name)
        if not result:
            return
        self.ports_view.on_config_selected()

    def __next_to_last(self) -> int:
        return self.s_layout.count() - 1

    def __before_ports(self) -> int:
        return self.s_layout.count() - 2


class PortsView(qtw.QWidget):

    def __init__(self, config_used: bool, data_types: list, node: node_factory.PipelineNodeBase, parent=None):
        super(PortsView, self).__init__(parent=parent)

        # Data
        self._config_used = config_used
        self._data_types = data_types
        self.current_node: node_factory.PipelineNodeBase = node
        self._i_port_widgets: list[SinglePortView] = []
        self._o_port_widgets: list[SinglePortView] = []

        self.io_layout = qtw.QHBoxLayout(self)
        self.io_layout.setContentsMargins(0, 0, 0, 0)

        # Inputs
        self.i_layout = qtw.QVBoxLayout(self)
        self.io_layout.addLayout(self.i_layout)
        self.add_input_button = qtw.QPushButton("Add Input")
        self.add_input_button.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.i_layout.addWidget(self.add_input_button)
        self.i_layout.addStretch()

        self.line = qtw.QFrame(self)
        self.line.setFrameShape(qtw.QFrame.VLine)
        self.io_layout.addWidget(self.line)

        # Outputs
        self.o_layout = qtw.QVBoxLayout(self)
        self.io_layout.addLayout(self.o_layout)
        self.add_output_button = qtw.QPushButton("Add Output")
        self.add_output_button.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.o_layout.addWidget(self.add_output_button)
        self.o_layout.addStretch()

        # Signal Wiring
        self.add_input_button.clicked.connect(functools.partial(self.add_input))
        self.add_output_button.clicked.connect(functools.partial(self.add_output))

        # On Config Used
        if config_used:
            self.add_input_button.setEnabled(False)
            self.add_output_button.setEnabled(False)

        self.setLayout(self.io_layout)

        current_config = self.current_node.get_current_config_data()
        # Mirror IO
        self.mirror_io()

    def on_config_selected(self):
        # Delete all previous Port Widgets
        for i in reversed(range(len(self._i_port_widgets))):
            self._i_port_widgets[i].deleteLater()
            del self._i_port_widgets[i]
        for o in reversed(range(len(self._o_port_widgets))):
            self._o_port_widgets[o].deleteLater()
            del self._o_port_widgets[o]
        # Add new Port Widgets
        self.mirror_io()

    def mirror_io(self):
        inputs = self.current_node.input_ports()
        for p in inputs:
            self._add_input_widget(p, self._config_used)

        outputs = self.current_node.output_ports()
        for p in outputs:
            self._add_output_widget(p, self._config_used)

    def add_input(self, config_data=None):
        if config_data is None:
            name = self._generate_name(True)
            if not self._data_types:
                painter_func = node_factory.PORT_DATA_TYPE_MAP.get(None)
            else:
                painter_func = node_factory.PORT_DATA_TYPE_MAP.get(self._data_types[0])
        else:
            name = config_data[0]
            painter_func = node_factory.PORT_DATA_TYPE_MAP.get(config_data[1])
        port = self.current_node.add_input(name, painter_func=painter_func)
        self._add_input_widget(port, config_data)

    def add_output(self, config_data=None):
        if config_data is None:
            name = self._generate_name(False)
            if not self._data_types:
                painter_func = node_factory.PORT_DATA_TYPE_MAP.get(None)
            else:
                painter_func = node_factory.PORT_DATA_TYPE_MAP.get(self._data_types[0])
        else:
            name = config_data[0]
            painter_func = node_factory.PORT_DATA_TYPE_MAP.get(config_data[1])
        port = self.current_node.add_output(name, painter_func=painter_func)
        self._add_output_widget(port, config_data)

    def _generate_name(self, is_input: bool, name="input", count=0) -> str:
        gen_name = f"{name}_{count}"
        if is_input:
            port = self.current_node.get_input(gen_name)
        else:
            port = self.current_node.get_output(gen_name)
        if port is None:
            return gen_name
        else:
            return self._generate_name(is_input, name, count + 1)

    def _add_input_widget(self, port, uses_config):
        port_widget = SinglePortView(port=port,
                                     data_types=self._data_types,
                                     is_input=True,
                                     uses_config=uses_config,
                                     index=len(self._o_port_widgets),
                                     parent=self)

        self._i_port_widgets.append(port_widget)
        self.i_layout.insertWidget(self.i_layout.count() - 1, port_widget)
        port_widget.s_port_name_changed.connect(self.current_node.rename_input)
        port_widget.s_delete_port.connect(self._on_delete_input)

    def _add_output_widget(self, port, uses_config):
        port_widget = SinglePortView(port=port,
                                     data_types=self._data_types,
                                     is_input=False,
                                     uses_config=uses_config,
                                     index=len(self._o_port_widgets),
                                     parent=self)

        self._o_port_widgets.append(port_widget)
        self.o_layout.insertWidget(self.o_layout.count() - 1, port_widget)
        port_widget.s_port_name_changed.connect(self.current_node.rename_output)
        port_widget.s_delete_port.connect(self._on_delete_output)

    def _on_delete_input(self, name: str, index: int):
        self.current_node.delete_input(name)
        self._i_port_widgets[index].deleteLater()
        del self._i_port_widgets[index]

    def _on_delete_output(self, name: str, index: int):
        self.current_node.delete_output(name)
        self._o_port_widgets[index].deleteLater()
        del self._o_port_widgets[index]


class SinglePortView(qtw.QWidget):
    s_data_type_changed = qtc.Signal()  # id, type
    s_port_name_changed = qtc.Signal(str, str)  # old name, new name
    s_delete_port = qtc.Signal(str, int)  # Name, is input, index

    def __init__(self, port, data_types: list, is_input: bool, uses_config: bool, index: int, parent=None):
        super(SinglePortView, self).__init__(parent)

        self.ui = Ui_Port()
        self.ui.setupUi(self)
        self.index = index

        self.port = port
        if not is_input and data_types is not None:
            self.ui.data_type_menu.addItems(data_types)

        if uses_config:
            self.ui.port_name_edit.setEnabled(False)
            self.ui.remove_port_button.setEnabled(False)
            if is_input:
                self.ui.data_type_menu.setEnabled(False)
                self.ui.data_type_menu.addItem(port.data_type)
        self.ui.port_name_edit.setText(port.name())
        if data_types is not None:
            self.ui.data_type_menu.setCurrentText(port.data_type)

        self.ui.data_type_menu.currentTextChanged.connect(self.on_data_type_changed)
        self.ui.port_name_edit.editingFinished.connect(self.on_port_name_changed)
        self.ui.remove_port_button.clicked.connect(self.on_delete_port)

    def set_name(self, new_name):
        self.ui.port_name_edit.setText(new_name)

    def set_data_type(self, new_data_type):
        self.ui.data_type_menu.setCurrentText(new_data_type)

    def on_port_name_changed(self):
        # Check if Port name already exists
        self.s_port_name_changed.emit(self.port.name(), self.ui.port_name_edit.text())

    def on_data_type_changed(self, text):
        self.port.data_type = text

    def on_delete_port(self):
        self.s_delete_port.emit(self.port.name(), self.index)
