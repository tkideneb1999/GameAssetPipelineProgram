import functools

from PyQt5.QtWidgets import QWidget, QMenu
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore as qtc

from MainApplication.PipelineViewerView.pipelineViewer_GUI import Ui_pipeline_viewer
from MainApplication.PipelineViewerView.pipelineStepViewer_GUI import Ui_pipeline_step_viewer

from MainApplication.Core.asset import Asset


class PipelineViewerView(QWidget):
    s_step_selected = qtc.pyqtSignal(int)
    s_open_file_explorer = qtc.pyqtSignal(int)  # step index

    def __init__(self, current_program="standalone", parent=None):
        super(PipelineViewerView, self).__init__(parent)
        self.ui = Ui_pipeline_viewer()
        self.ui.setupUi(self)
        self.ui.pipeline_list.currentRowChanged.connect(self.step_selected)
        self.ui.pipeline_list.installEventFilter(self)

        self.current_program = current_program

    def update_view(self, asset: Asset) -> None:
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

    def eventFilter(self, source, event) -> bool:
        if event.type() == qtc.QEvent.ContextMenu and source is self.ui.pipeline_list:
            print("[GAPA] launching context menu")
            item = source.itemAt(event.pos())
            if item is None:
                return True
            index = source.indexFromItem(item)
            func = functools.partial(self.s_open_file_explorer.emit, index.row())
            menu = QMenu(self)
            open_action = menu.addAction("Open in Explorer")
            open_action.triggered.connect(func)
            menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)

    def step_selected(self, index: int) -> None:
        self.s_step_selected.emit(index)

    def get_selected_index(self) -> int:
        return self.ui.pipeline_list.currentRow()

    def set_current_program(self, program: str) -> None:
        self.current_program = program


class PipelineStepViewerView(QWidget):
    def __init__(self, step_name: str, step_program: str, step_state: str, parent=None):
        super(PipelineStepViewerView, self).__init__(parent)
        self.ui = Ui_pipeline_step_viewer()
        self.ui.setupUi(self)
        self.update_view(step_name, step_program, step_state)

    def update_view(self, step_name: str, step_program: str, step_state: str) -> None:
        self.ui.name_label.setText(step_name)
        self.ui.program_label.setText(step_program)
        self.ui.state_label.setText(step_state)
