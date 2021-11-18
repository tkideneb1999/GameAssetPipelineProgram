import importlib

from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QListWidgetItem
from PySide2 import QtCore as qtc

from . import pipelineViewer_GUI
from . import pipelineStepViewer_GUI

from ... import asset as assetModule

importlib.reload(pipelineViewer_GUI)
importlib.reload(pipelineStepViewer_GUI)
importlib.reload(assetModule)


class PipelineViewerView(QWidget):
    s_step_selected = qtc.Signal(int)

    def __init__(self, current_program="standalone", parent=None):
        super(PipelineViewerView, self).__init__(parent)
        self.ui = pipelineViewer_GUI.Ui_pipeline_viewer()
        self.ui.setupUi(self)
        self.ui.pipeline_list.currentRowChanged.connect(self.step_selected)

        self.current_program = current_program

    def update_view(self, asset) -> None:
        # asset: Asset
        self.ui.pipeline_list.clear()
        for step in asset.pipeline.pipeline_steps:
            state = asset.pipeline_progress[step.uid]["state"]
            step_widget = PipelineStepViewerView(step.name, step.program, state, parent=self.ui.pipeline_list)
            step_item = QListWidgetItem(parent=self.ui.pipeline_list)
            step_item.setSizeHint(step_widget.sizeHint())

            files_missing = asset.pipeline_progress[step.uid]["state"] == "files missing"
            not_current_program = self.current_program != step.program
            if files_missing or not_current_program:
                step_item.setFlags(qtc.Qt.NoItemFlags)

            self.ui.pipeline_list.addItem(step_item)
            self.ui.pipeline_list.setItemWidget(step_item, step_widget)

    def step_selected(self, index) -> None:
        # index: int
        self.s_step_selected.emit(index)

    def get_selected_index(self) -> int:
        return self.ui.pipeline_list.currentRow()

    def set_current_program(self, program) -> None:
        # program: str
        self.current_program = program


class PipelineStepViewerView(QWidget):
    def __init__(self, step_name, step_program, step_state, parent=None):
        # step_name: str, step_program: str, step_state: str
        super(PipelineStepViewerView, self).__init__(parent)
        self.ui = pipelineStepViewer_GUI.Ui_pipeline_step_viewer()
        self.ui.setupUi(self)
        self.update_view(step_name, step_program, step_state)

    def update_view(self, step_name, step_program, step_state) -> None:
        # step_name: str, step_program: str, step_state: str
        self.ui.name_label.setText(step_name)
        self.ui.program_label.setText(step_program)
        self.ui.state_label.setText(step_state)
