from pathlib import Path
import importlib.util

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .nodegraph.base import graph as ng
from .nodegraph import constants

from ..Core.settings import Settings
from . import node_factory
from .propertiesBin import PropertiesBin
from ..Plugins import pluginAPI


class PipelineConfigurator(qtw.QWidget):
    s_pipeline_saved = qtc.Signal(Path, str)

    def __init__(self, parent=None):
        super(PipelineConfigurator, self).__init__(parent)

        # Init Settings
        self.settings = Settings()
        self.settings.load()

        # Node Graph
        self.graph = ng.NodeGraph(self)
        self.graph.set_grid_mode(constants.VIEWER_GRID_MODE_DOTS)
        self.graph.node_selected.connect(self.node_selected)
        self.graph.node_created.connect(self.node_created)
        self.graph.nodes_deleted.connect(self.node_deleted)

        program_names = self.settings.program_registration.get_program_list()
        for p_name in program_names:
            addon_path = self.settings.program_registration.get_program_addon_path(p_name)
            spec = importlib.util.spec_from_file_location(addon_path.stem, str(addon_path))
            step_settings_registration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(step_settings_registration)
            program_settings: pluginAPI.PluginSettings = step_settings_registration.create_pipeline_settings()
            node_class = node_factory.create_node_class(p_name,
                                                        program_settings.pipeline_settings,
                                                        program_settings.configs,
                                                        program_settings.export_all,
                                                        program_settings.has_set_outputs)
            self.graph.register_node(node_class, alias=p_name)

        # Register Plugin Nodes
        plugin_names = self.settings.plugin_registration.get_plugin_list()
        for p_name in plugin_names:
            plugin_module = self.settings.plugin_registration.get_plugin(p_name)
            plugin_settings: pluginAPI.PluginSettings = plugin_module.register_settings()
            node_class = node_factory.create_node_class(p_name,
                                                        plugin_settings.pipeline_settings,
                                                        plugin_settings.configs,
                                                        plugin_settings.export_all,
                                                        plugin_settings.has_set_outputs)
            self.graph.register_node(node_class, alias=p_name)

        self.h_Layout = qtw.QHBoxLayout(self)
        self.h_Layout.setContentsMargins(0, 0, 0, 0)
        self.h_Layout.addWidget(self.graph.widget)

        self.property_bin = PropertiesBin(self)
        self.h_Layout.addWidget(self.property_bin)

        self.setLayout(self.h_Layout)

        self.project_dir: Path = Path()

    def set_project_dir(self, project_dir: Path) -> None:
        self.project_dir = project_dir

    def node_selected(self, node):
        self.property_bin.node_selected(node)

    def node_created(self, node):
        self.property_bin.node_selected(node)

    def node_deleted(self, node):
        self.property_bin.node_deleted(node)
