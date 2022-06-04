from pathlib import Path

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from .nodegraph.base import graph as ng
from .nodegraph import constants

from ..Core.settings import Settings
from . import nodes


class PipelineConfigurator(qtw.QWidget):
    s_pipeline_saved = qtc.Signal(Path, str)

    def __init__(self, parent=None):
        super(PipelineConfigurator, self).__init__(parent)

        # Node Graph
        self.graph = ng.NodeGraph(self)
        self.graph.set_grid_mode(constants.VIEWER_GRID_MODE_DOTS)
        self.graph.register_node(nodes.PipelineStepNode)
        self.graph.register_node(nodes.PipelineAssetImportNode)
        self.graph.register_node(nodes.PipelineEngineExportNode)

        self.vLayout = qtw.QVBoxLayout(self)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.addWidget(self.graph.widget)
        self.setLayout(self.vLayout)

        self.project_dir: Path = Path()

    def set_project_dir(self, project_dir: Path) -> None:
        self.project_dir = project_dir
