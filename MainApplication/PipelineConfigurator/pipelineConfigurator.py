from pathlib import Path
import importlib.util

from ..Common.qtpy import QtWidgets as qtw
from ..Common.qtpy import QtCore as qtc

from .nodegraph.base import graph as ng
from .nodegraph import constants

from ..Common.Core.settings import Settings
from ..Common.Core.pipeline import Pipeline
from . import node_factory
from .propertiesBin import PropertiesBin
from ..Plugins import pluginAPI

from .pipeline_publish_dialog_GUI import Ui_PublishDialog


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
        self.graph.s_publish_pipeline.connect(self.publish_pipeline)

        self.uid_counter = 0

        # Register Program Nodes
        program_names = self.settings.program_registration.get_program_list()
        for p_name in program_names:
            addon_path = self.settings.program_registration.get_program_addon_path(p_name)
            spec = importlib.util.spec_from_file_location(addon_path.stem, str(addon_path))
            step_settings_registration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(step_settings_registration)
            program_settings: pluginAPI.PluginSettings = step_settings_registration.create_pipeline_settings()
            node_class = node_factory.create_node_class(name=p_name,
                                                        in_is_plugin=False,
                                                        settings=program_settings.pipeline_settings,
                                                        in_configs=program_settings.configs,
                                                        in_export_all=program_settings.export_all,
                                                        in_has_set_outputs=program_settings.has_set_outputs,
                                                        in_export_data_types=program_settings.export_data_types)
            self.graph.register_node(node_class, alias=p_name)

        # Register Plugin Nodes
        plugin_names = self.settings.plugin_registration.get_plugin_list()
        for p_name in plugin_names:
            plugin_module = self.settings.plugin_registration.get_plugin(p_name)
            plugin_settings: pluginAPI.PluginSettings = plugin_module.register_settings()
            node_class = node_factory.create_node_class(name=p_name,
                                                        in_is_plugin=True,
                                                        settings=plugin_settings.pipeline_settings,
                                                        in_configs=plugin_settings.configs,
                                                        in_export_all=plugin_settings.export_all,
                                                        in_has_set_outputs=plugin_settings.has_set_outputs,
                                                        in_export_data_types=plugin_settings.export_data_types)
            self.graph.register_node(node_class, alias=p_name)

        self.h_Layout = qtw.QHBoxLayout(self)
        self.h_Layout.setContentsMargins(0, 0, 0, 0)
        self.h_Layout.addWidget(self.graph.widget)
        self.graph.widget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.MinimumExpanding)

        self.property_bin = PropertiesBin(self)
        self.h_Layout.addWidget(self.property_bin)

        self.setLayout(self.h_Layout)

        self.project_dir: Path = Path()
        self.registered_pipelines: dict = {}

    def set_project_data(self, project_dir: Path, registered_pipelines=None) -> None:
        if registered_pipelines is None:
            registered_pipelines = {}
        self.project_dir = project_dir
        self.registered_pipelines = registered_pipelines

    def node_selected(self, node):
        self.property_bin.node_selected(node)

    def node_created(self, node: node_factory.PipelineNodeBase):
        self.property_bin.node_selected(node)
        node.set_uid(f"s{self.uid_counter}")
        self.uid_counter += 1
        if not(node.configs == {}):
            node.config_selected(list(node.configs.keys())[0])

    def node_deleted(self, node):
        self.property_bin.node_deleted(node)

    def publish_pipeline(self):
        print("[GAPA] Publishing Pipeline")
        publish_dialog = PublishDialog(list(self.registered_pipelines.keys()), self)
        if publish_dialog.exec_() == 0:
            return

        pipeline = Pipeline()
        pipeline.name = publish_dialog.get_name()
        nodes = self.graph.model.nodes
        io_connections = {}
        for node_id in nodes:
            identifier = nodes[node_id].__identifier__
            group_type = identifier.split(".")[0]
            if group_type == "pipeline":
                step_data = nodes[node_id].to_pipeline_data()
                pipeline.pipeline_steps.append(step_data[0])
                io_connections = {**io_connections, **step_data[1]}
        pipeline.io_connections = io_connections
        path = pipeline.save(self.project_dir / "pipelines")
        self.s_pipeline_saved.emit(path, pipeline.name)


class PublishDialog(qtw.QDialog):
    def __init__(self, registered_pipelines: list, parent=None):
        super(PublishDialog, self).__init__(parent)
        self.ui = Ui_PublishDialog()
        self.ui.setupUi(self)
        self.ui.registered_pipelines_list.addItems(registered_pipelines)
        self.registered_pipelines = registered_pipelines

        self.ui.name_line_edit.editingFinished.connect(self.on_editing_finished)

    def on_editing_finished(self):
        name = self.ui.name_line_edit.text()
        if name in self.registered_pipelines:
            self.ui.error_msg_label.setText("Pipeline Already exists!")
            self.ui.name_line_edit.setText("")
            return
        self.ui.ok_button.setEnabled(True)

    def get_name(self) -> str:
        return self.ui.name_line_edit.text()