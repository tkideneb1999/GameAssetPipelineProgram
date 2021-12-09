import functools

from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore as qtc

from MainApplication.PipelineViewerView.pipelineViewer_GUI import Ui_pipeline_viewer
from MainApplication.PipelineViewerView.pipelineStepViewer_GUI import Ui_pipeline_step_viewer

from MainApplication.Core.asset import Asset


def clickable(widget: qtw.QWidget):
    class Filter(qtc.QObject):

        s_clicked = qtc.pyqtSignal()
        s_context_menu_requested = qtc.pyqtSignal(qtc.QPoint)

        def eventFilter(self, source: qtc.QObject, event: qtc.QEvent) -> bool:
            if source == widget:
                clicked = False
                if event.type() == qtc.QEvent.MouseButtonRelease:
                    if source.rect().contains(event.pos()):
                        self.s_clicked.emit()
                        clicked = True
                if event.type() == qtc.QEvent.ContextMenu:
                    if source.rect().contains(event.pos()):
                        self.s_context_menu_requested.emit(event.globalPos())
                        clicked = True
                return clicked or super().eventFilter(source, event)

            return super().eventFilter(source, event)

    event_filter = Filter(widget)
    widget.installEventFilter(event_filter)
    return event_filter.s_clicked, event_filter.s_context_menu_requested


class PipelineViewerView(qtw.QWidget):
    s_step_selected = qtc.pyqtSignal(int)
    s_open_file_explorer = qtc.pyqtSignal(int)  # step index
    s_run_plugin = qtc.pyqtSignal(int)

    def __init__(self, current_program="standalone", parent=None):
        super(PipelineViewerView, self).__init__(parent)
        self.ui = Ui_pipeline_viewer()
        self.ui.setupUi(self)

        self.scrollbar_layout = qtw.QHBoxLayout(self)
        self.scrollbar_layout.addStretch()
        self.scrollable_widget = qtw.QWidget(self)
        self.scrollable_widget.setLayout(self.scrollbar_layout)
        self.ui.pipeline_scrollbar.setWidget(self.scrollable_widget)

        self.current_program = current_program
        self.step_widget_list: list[PipelineStepViewerView] = []
        self.selected_step = -1

    def update_view(self, asset: Asset) -> None:
        for step_widget in self.step_widget_list:
            step_widget.deleteLater()
        for index in range(len(asset.pipeline.pipeline_steps)):
            step = asset.pipeline.pipeline_steps[index]
            state = asset.pipeline_progress[step.uid]["state"]
            is_current_program = step.program == self.current_program
            self.step_widget_list.append(PipelineStepViewerView(index, step.name,
                                                                step.program, state,
                                                                is_current_program, step.is_plugin,
                                                                state == "files missing",
                                                                parent=self.scrollable_widget))
            self.step_widget_list[-1].s_clicked.connect(self.step_selected)
            self.step_widget_list[-1].s_open_file_explorer.connect(self.s_open_file_explorer.emit)
            self.step_widget_list[-1].s_run_plugin.connect(self.s_run_plugin.emit)
            self.scrollbar_layout.insertWidget(self.scrollbar_layout.count() - 1, self.step_widget_list[-1])

    def step_selected(self, index: int) -> None:
        self.selected_step = index
        self.s_step_selected.emit(index)

    def get_selected_index(self) -> int:
        return self.selected_step

    def set_current_program(self, program: str) -> None:
        self.current_program = program


class PipelineStepViewerView(qtw.QWidget):
    s_clicked = qtc.pyqtSignal(int)
    s_open_file_explorer = qtc.pyqtSignal(int)
    s_run_plugin = qtc.pyqtSignal(int)

    def __init__(self, step_index: int, step_name: str, step_program: str,
                 step_state: str, uses_current_program: bool,
                 is_plugin: bool, files_missing: bool, parent=None):
        super(PipelineStepViewerView, self).__init__(parent)
        self.ui = Ui_pipeline_step_viewer()
        self.ui.setupUi(self)
        self.index = step_index
        self.update_view(step_name, step_program, step_state)
        self.uses_current_program = uses_current_program
        self.is_plugin = is_plugin
        self.files_missing = files_missing
        signals = clickable(self)
        signals[0].connect(self.clicked)
        signals[1].connect(self.contextMenuRequested)

    def update_view(self, step_name: str, step_program: str, step_state: str) -> None:
        self.ui.name_label.setText(step_name)
        self.ui.program_label.setText(step_program)
        self.ui.state_label.setText(step_state)

    def contextMenuRequested(self, global_pos: qtc.QPoint):
        print(f"[GAPA] Context Menu for {self.index}")
        menu = qtw.QMenu(self)
        open_action = menu.addAction("Open in Explorer")
        open_explorer_func = functools.partial(self.s_open_file_explorer.emit, self.index)
        open_action.triggered.connect(open_explorer_func)
        print(f"[GAPA] {self.index} is plugin: {self.is_plugin}")
        if self.is_plugin:
            run_action = menu.addAction("Run Plugin...")
            if self.files_missing:
                run_action.setEnabled(False)
            run_func = functools.partial(self.s_run_plugin.emit, self.index)
            run_action.triggered.connect(run_func)

        menu.exec_(global_pos)

    def clicked(self):
        if self.files_missing:
            return
        if not self.uses_current_program:
            return
        print(f"[GAPA] clicked on {self.index}")
        self.s_clicked.emit(self.index)
