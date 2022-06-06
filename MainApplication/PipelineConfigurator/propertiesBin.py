from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .nodegraph.nodes.base_node import BaseNode

from ..localSettingsView import LocalSettingsView

NO_NODE_SELECTED_TEXT = "--No Node selected--"


class PropertiesBin(qtw.QWidget):
    
    def __init__(self, parent=None):
        super(PropertiesBin, self).__init__(parent)
        self.setMinimumSize(300, 300)
        self.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        self.frame = qtw.QFrame(self)
        self.frame.setFrameShape(qtw.QFrame.Box)
        self.frame.setFrameShadow(qtw.QFrame.Plain)

        self.f_layout = qtw.QVBoxLayout(self.frame)
        self.frame.setLayout(self.f_layout)

        self.node_selected_label = qtw.QLabel(NO_NODE_SELECTED_TEXT)
        self.node_name_label = qtw.QLineEdit(self)
        self.node_name_label.editingFinished.connect(self.on_name_changed)
        self.node_name_label.hide()

        self.config_combo_box = qtw.QComboBox()
        self.config_combo_box.currentTextChanged.connect(self.on_config_changed)
        self.config_combo_box.hide()

        self.f_layout.addWidget(self.node_selected_label)
        self.f_layout.addWidget(self.node_name_label)
        self.f_layout.addWidget(self.config_combo_box)

        self.v_Layout = qtw.QVBoxLayout(self)
        self.v_Layout.addWidget(self.frame)
        self.setLayout(self.v_Layout)

        self.settings_view: LocalSettingsView = None
        self.current_node: BaseNode = None

    def node_selected(self, node: BaseNode):
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

        if not node.configs == {}:
            self.config_combo_box.blockSignals(True)
            self.config_combo_box.addItems(list(node.configs.keys()))
            self.config_combo_box.setCurrentText(node.current_config)
            self.config_combo_box.blockSignals(False)
            self.config_combo_box.show()

        if self.settings_view is not None:
            self.settings_view.deleteLater()
        self.settings_view = LocalSettingsView(node.settings_template, node.settings_values, self)
        self.node_name_label.setText(node.name())
        self.f_layout.addWidget(self.settings_view)

    def node_deleted(self, nodes):
        print("Node Deleted")
        for n in nodes:
            if n == self.current_node.id:
                print("Node was being displayed")
                self.settings_view.deleteLater()
                self.settings_view = None
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
        self.current_node.config_selected(name)
