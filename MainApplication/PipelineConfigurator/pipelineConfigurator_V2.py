from pathlib import Path
from enum import Enum

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from MainApplication.Core.pipeline import Pipeline
from MainApplication.Core.settings import Settings
from MainApplication.PipelineConfigurator.pipeline_step_GUI import Ui_pipeline_step
from MainApplication.PipelineConfigurator.pipeline_step_input_GUI import Ui_pipeline_step_input
from MainApplication.PipelineConfigurator.pipeline_step_output_GUI import Ui_pipeline_step_output


class IODataEnum(Enum):
    NAME = 0
    DATATYPE = 1
    SELECTEDOUTPUT = 2


class PipelineConfigurator(qtw.QWidget):

    s_pipeline_saved = qtc.pyqtSignal(Path, str)

    def __init__(self, parent=None):
        super(PipelineConfigurator, self).__init__(parent)

        # Data
        self.current_pipeline: Pipeline = Pipeline()
        self.project_dir: Path = Path()
        self.settings = Settings()
        self.settings.load()

        layout = qtw.QVBoxLayout()
        self.name_line_edit = qtw.QLineEdit("Pipeline_Name")
        self.name_line_edit.setText(self.current_pipeline.name)
        self.name_line_edit.editingFinished.connect(self.pipeline_name_changed)
        layout.addWidget(self.name_line_edit)

        layout_1 = qtw.QHBoxLayout()
        self.scrollbar = qtw.QScrollArea(self)
        self.scrollbar.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scrollbar.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scrollbar.setWidgetResizable(True)

        self.scrollbar_layout = qtw.QHBoxLayout()
        self.scrollbar_layout.addStretch()
        self.scrollable_widget = qtw.QWidget()
        self.scrollable_widget.setLayout(self.scrollbar_layout)
        self.scrollbar.setWidget(self.scrollable_widget)

        layout_1.addWidget(self.scrollbar)

        self.step_widgets: list[PipelineStepView] = []

        # Buttons
        button_layout = qtw.QVBoxLayout()

        # Add Step Button
        add_step_button = qtw.QPushButton("Add Step")
        add_step_button.setMinimumSize(100, 100)
        add_step_button.clicked.connect
        button_layout.addWidget(add_step_button)

        # Save Pipeline Button
        save_pipeline_button = qtw.QPushButton("Save")
        save_pipeline_button.setMinimumSize(100, 100)
        save_pipeline_button.clicked.connect
        button_layout.addWidget(save_pipeline_button)

        # Load Pipeline Button
        load_pipeline_button = qtw.QPushButton("Load")
        load_pipeline_button.setMinimumSize(100, 100)
        load_pipeline_button.clicked.connect
        button_layout.addWidget(load_pipeline_button)

        layout_1.addLayout(button_layout)
        layout.addLayout(layout_1)
        self.setLayout(layout)

    def set_project_dir(self, project_dir: Path) -> None:
        self.project_dir = project_dir

    def pipeline_name_changed(self) -> None:
        text = self.name_line_edit.text()
        if " " in text:
            print(f"[GAPA] Pipeline Name contains spaces: {text}")
            return
        self.current_pipeline.name = text

    def load_pipeline_dialog(self) -> None:
        file_dialog = qtw.QFileDialog(self)
        file_dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Pipeline File (*.json)")
        file_dialog.setViewMode(qtw.QFileDialog.Detail)
        result = file_dialog.exec_()
        if result == 0:
            return
        path = Path(file_dialog.selectedFiles()[0])
        self.load


class PipelineStepView(qtw.QWidget):
    # Step Signals
    s_step_deleted = qtc.pyqtSignal(int)  # Step Index

    def __init__(self, index: int, parent=None):
        super(PipelineStepView, self).__init__(parent)
        self.ui = Ui_pipeline_step()
        self.ui.setupUi(self)

        # Data
        self.index: int = index
        self.inputs: list[PipelineInputView] = []
        self.outputs: list[PipelineOutputView] = []

        # Add IO Buttons
        self.ui.add_input_button.clicked.connect
        self.ui.add_output_button.clicked.connect

        # Program Combobox
        settings = Settings()
        self.ui.program_combobox.addItems(settings.program_registration.get_program_list())
        self.ui.program_combobox.addItems(settings.plugin_registration.get_plugin_list())
        self.ui.program_combobox.currentTextChanged.connect

        # Program Settings
        config_available = self.ui.program_settings.program_changed(self.ui.program_combobox.currentText())
        self.set_io_button_interactivity(not config_available)
        self.ui.program_settings.s_selected_config.connect

        # Context Menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.launch_context_menu)

    def launch_context_menu(self, pos) -> None:
        menu = qtw.QMenu(self)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_step)
        menu.exec_(self.mapToGlobal(pos))

    def delete_step(self) -> None:
        self.s_step_deleted.emit(self.index)
        self.deleteLater()

    # Helpers
    def set_io_button_interactivity(self, is_active: bool) -> None:
        print(f"[GAPA] Setting add buttons enabled status to: {is_active}")
        self.ui.add_input_button.setEnabled(is_active)
        self.ui.add_output_button.setEnabled(is_active)


class PipelineInputView(qtw.QWidget):
    s_remove = qtc.pyqtSignal(int)  # Input Index
    s_modified = qtc.pyqtSignal(int, IODataEnum, str)  # Input Index, Data Type, Data

    def __init__(self, index: int, uid: str, parent=None):
        super(PipelineInputView, self).__init__(parent)
        self.ui = Ui_pipeline_step_input()
        self.ui.setupUi(self)
        self.ui.remove_input_button.clicked.connect(self.remove)

        self.index = index
        self.uid = uid
        self.name = ""
        self.possible_outputs: list[tuple[str, str]]

    def remove(self) -> None:
        self.s_remove.emit(self.index)
        self.deleteLater()

    def set_uid_label(self, name):
        self.name = name
        self.ui.id_label.setText(f"{name} - {self.uid}")

    def set_possible_outputs(self, outputs: list[tuple[str, str]]) -> None:
        self.possible_outputs = outputs
        combobox_list = [f"{o[0]} - {o[1]}" for o in outputs]
        self.ui.input_name_combobox.clear()
        self.ui.input_name_combobox.addItem("----")
        self.ui.input_name_combobox.model().item(0).setEnabled(False)
        self.ui.input_name_combobox.addItems(combobox_list)

    def disable_customization(self, disabled: bool) -> None:
        self.ui.remove_input_button.setDisabled(disabled)
        self.ui.input_type_combo_box.setDisabled(disabled)

    def get_data(self) -> tuple[str, str, tuple[str, str]]:
        output_index = self.ui.input_name_combobox.currentIndex()
        if output_index == 0:
            selected_output = None
        else:
            selected_output = self.possible_outputs[output_index - 1]
        return self.uid, self.name, selected_output


class PipelineOutputView(qtw.QWidget):
    s_remove = qtc.pyqtSignal(int)  # Output Index
    s_modified = qtc.pyqtSignal(int, IODataEnum, str)  # Output Index, Data Type, Data

    def __init__(self, index: int, uid: str, parent=None):
        super(PipelineOutputView, self).__init__(parent)
        self.ui = Ui_pipeline_step_output()
        self.ui.setupUi(self)
        self.ui.remove_output_button.clicked.connect(self.remove)

        self.index = index
        self.uid = uid

    def remove(self) -> None:
        self.s_remove.emit(self.index)
        self.deleteLater()

    def set_data_type_combobox(self, data_types: list[str], current_data_type: str) -> None:
        self.ui.output_type_combobox.clear()
        self.ui.output_type_combobox.addItems(data_types)
        self.ui.output_type_combobox.setCurrentText(current_data_type)

    def disable_customization(self, disabled: bool) -> None:
        self.ui.output_name_lineedit.setReadOnly(disabled)
        self.ui.output_type_combobox.setDisabled(disabled)

    def get_data(self) -> tuple[str, str, str]:
        name = self.ui.output_name_lineedit.text()
        output_type = self.ui.output_type_combobox.currentText()
        return self.uid, name, output_type
