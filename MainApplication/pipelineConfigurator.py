import json
from pathlib import Path
from enum import Enum

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from pipeline import Pipeline
from pipeline_step_GUI import Ui_pipeline_step
from pipeline_step_input_GUI import Ui_pipeline_step_input
from pipeline_step_output_GUI import Ui_pipeline_step_output


class IODataEnum(Enum):
    Name = 0
    AssetType = 1
    SelectedOutput = 2


class PipelineConfigurator(qtw.QWidget):

    pipeline_saved_signal = qtc.pyqtSignal(Path, str)

    def __init__(self, parent):
        super().__init__(parent)

        # Data
        self.current_pipeline = Pipeline()
        self.project_dir = Path()

        # <editor-fold desc="GUI">
        layout = qtw.QVBoxLayout()
        # -Pipeline Name Line Edit
        self.name_line_edit = qtw.QLineEdit("Pipeline Name")
        self.name_line_edit.setText(self.current_pipeline.name)
        layout.addWidget(self.name_line_edit)

        layout_1 = qtw.QHBoxLayout()

        # -Scroll Area for Pipeline Steps
        self.scroll_bar = qtw.QScrollArea(self)
        self.scroll_bar.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll_bar.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scroll_bar.setWidgetResizable(True)

        self.scrollbar_layout = qtw.QHBoxLayout()
        self.scrollbar_layout.addStretch()
        self.scrollable_widget = qtw.QWidget()
        self.scrollable_widget.setLayout(self.scrollbar_layout)
        self.scroll_bar.setWidget(self.scrollable_widget)

        layout_1.addWidget(self.scroll_bar)

        self.step_widgets = []

        # -Edit Pipeline Buttons
        button_layout = qtw.QVBoxLayout()
        # --Add Step Button
        add_step_button = qtw.QPushButton("Add Step")
        add_step_button.setMinimumSize(100, 100)
        add_step_button.clicked.connect(self.add_step)
        button_layout.addWidget(add_step_button)
        # --Save Pipeline Button
        save_pipeline_button = qtw.QPushButton("Save")
        save_pipeline_button.setMinimumSize(100, 100)
        save_pipeline_button.clicked.connect(self.save)
        button_layout.addWidget(save_pipeline_button)
        # --Load Pipeline Button
        load_pipeline_button = qtw.QPushButton("Load")
        load_pipeline_button.setMinimumSize(100, 100)
        load_pipeline_button.clicked.connect(self.load_pipeline_dialog)
        button_layout.addWidget(load_pipeline_button)

        layout_1.addLayout(button_layout)
        layout.addLayout(layout_1)
        self.setLayout(layout)
        # </editor-fold>

    def set_project_dir(self, project_dir: Path):
        self.project_dir = project_dir

    def pipeline_name_changed(self):
        text = self.name_line_edit.text()
        if " " in text:
            print("name contains space")
            self.name_line_edit.setText(self.name)
            return
        self.current_pipeline.name = text

    def load_pipeline_dialog(self):
        file_dialog = qtw.QFileDialog(self)
        file_dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Pipeline File (*.json)")
        file_dialog.setViewMode(qtw.QFileDialog.Detail)
        result = file_dialog.exec_()
        if result == 0:
            return
        path = Path(file_dialog.selectedFiles()[0])
        self.load(path)

    # -------------------------
    # <editor-fold, desc="Pipeline Step Function Handlers">
    # Pipeline Step Function Handlers

    def add_step(self):
        name = self.current_pipeline.add_step()[1]
        self.step_widgets.append(PipelineStepGUI(len(self.step_widgets), self.scrollable_widget))
        self.scrollbar_layout.insertWidget(self.scrollbar_layout.count() - 1, self.step_widgets[-1])
        self.step_widgets[-1].set_name(name)
        self.step_widgets[-1].s_step_deleted.connect(self.remove_step)
        self.step_widgets[-1].s_step_renamed.connect(self.rename_step)

        self.step_widgets[-1].s_input_added.connect(self.input_added)
        self.step_widgets[-1].s_input_removed.connect(self.input_removed)
        self.step_widgets[-1].s_input_modified.connect(self.input_modified)

        self.step_widgets[-1].s_output_added.connect(self.output_added)
        self.step_widgets[-1].s_output_removed.connect(self.output_removed)
        self.step_widgets[-1].s_output_modified.connect(self.output_modified)

    def remove_step(self, index: int):
        self.current_pipeline.remove_step(index)
        for i in range(index + 1, len(self.step_widgets)):
            self.step_widgets[i].index -= 1
        del self.step_widgets[index]

    def rename_step(self, step_index: int, name: str):
        self.current_pipeline.pipeline_steps[step_index].name = name

    # </editor-fold>

    # -----------------------
    # <editor-fold, desc="Input/Output Function Handlers">
    # Input/Output Function Handlers

    def input_added(self, step_index: int):
        self.current_pipeline.add_input(step_index)
        self.update_possible_outputs(step_index - 1)

    def input_removed(self, step_index: int, input_index: int):
        self.current_pipeline.remove_input(step_index, input_index)

    def input_modified(self, step_index: int, input_index: int, data_field: IODataEnum, data: str):
        if data_field == IODataEnum.SelectedOutput:
            self.current_pipeline.connect_io(self.current_pipeline.get_uid(step_index, True, input_index), data)

    def output_added(self, step_index: int):
        name = self.current_pipeline.add_output(step_index)[1]
        self.step_widgets[step_index].outputs[-1].set_name(name)
        self.update_possible_outputs(step_index)

    def output_removed(self, step_index: int, output_index: int):
        self.current_pipeline.remove_output(step_index, output_index)
        self.update_possible_outputs(step_index)

    def output_modified(self, step_index: int, output_index: int, data_field: IODataEnum, data: str):
        if data_field == IODataEnum.Name:
            self.current_pipeline.pipeline_steps[step_index].outputs[output_index].name = data

    def update_possible_outputs(self, step_index: int, override_io=True):
        pipeline_outputs = []
        for k in range(len(self.step_widgets)):
            if k > step_index:
                for i in self.step_widgets[k].inputs:
                    i.set_possible_outputs(pipeline_outputs)
                    if override_io:
                        self.current_pipeline.delete_io_connection_if_exists(
                            self.current_pipeline.get_uid(k, True, i.index))
            for o in self.step_widgets[k].outputs:
                pipeline_outputs.append(self.current_pipeline.get_uid(k, False, o.index))

    # </editor-fold>

    # -----------------------------------
    # <editor-fold, desc="Serialization">
    # Serialization
    # -----------------------------------

    def save(self):
        path = self.project_dir / "pipelines"
        self.current_pipeline.save(path)

    def load(self, path: Path):
        for s in self.step_widgets:
            s.delete_step()
        self.current_pipeline.load(path)
        for k in range(len(self.current_pipeline.pipeline_steps)):
            # Create Step GUI
            self.step_widgets.append(PipelineStepGUI(k, self.scrollable_widget))
            self.scrollbar_layout.insertWidget(self.scrollbar_layout.count() - 1, self.step_widgets[-1])
            self.step_widgets[-1].set_name(self.current_pipeline.pipeline_steps[k].name)
            self.step_widgets[-1].s_step_deleted.connect(self.remove_step)
            self.step_widgets[-1].s_step_renamed.connect(self.rename_step)

            self.step_widgets[-1].s_input_added.connect(self.input_added)
            self.step_widgets[-1].s_input_removed.connect(self.input_removed)
            self.step_widgets[-1].s_input_modified.connect(self.input_modified)

            self.step_widgets[-1].s_output_added.connect(self.output_added)
            self.step_widgets[-1].s_output_removed.connect(self.output_removed)
            self.step_widgets[-1].s_output_modified.connect(self.output_modified)

            # Create Inputs for Step
            for i in range(len(self.current_pipeline.pipeline_steps[k].inputs)):
                self.step_widgets[-1].load_input("")  # TODO(Pipeline): Implement asset Type

            # Create Outputs for Step
            for o in range(len(self.current_pipeline.pipeline_steps[k].outputs)):
                self.step_widgets[-1].load_output("")  # TODO(Pipeline): Implement asset Type
                self.step_widgets[-1].outputs[-1].set_name(self.current_pipeline.pipeline_steps[k].outputs[o].name)

        # Update Input Selections
        self.update_possible_outputs(0, override_io=False)

        # Set correct selected output in Input Selection
        for iuid in self.current_pipeline.io_connections:
            for s in range(len(self.current_pipeline.pipeline_steps)):
                for i in range(len(self.current_pipeline.pipeline_steps[s].inputs)):
                    if iuid == self.current_pipeline.pipeline_steps[s].inputs[i].uid:
                        self.step_widgets[s].inputs[i].set_selection_with_text(
                            self.current_pipeline.io_connections[iuid])
        # TODO(Pipeline Configurator): Optimize search

    # </editor-fold>

    # -----------------------------
    # <editor-fold, desc="Helpers">
    # Helpers
    # -----------------------------

    def get_stepWidget_at_index(self, index: int):
        return self.scrollbar_layout.itemAt(index).widget()

    # </editor-fold>


class PipelineStepGUI(qtw.QWidget):
    # <editor-fold, desc="Signals">
    # Signals
    # -Pipeline Step Signals
    s_step_renamed = qtc.pyqtSignal(int, str)
    s_step_deleted = qtc.pyqtSignal(int)

    # -Pipeline Input Signals
    s_input_added = qtc.pyqtSignal(int)
    s_input_removed = qtc.pyqtSignal(int, int)
    s_input_modified = qtc.pyqtSignal(int, int, IODataEnum, str)

    # -Pipeline OutputSignals
    s_output_added = qtc.pyqtSignal(int)
    s_output_removed = qtc.pyqtSignal(int, int)
    s_output_modified = qtc.pyqtSignal(int, int, IODataEnum, str)
    # </editor-fold>

    def __init__(self, index: int, parent=None):
        # GUI
        super().__init__(parent)
        self.ui = Ui_pipeline_step()
        self.ui.setupUi(self)

        # Add Input Button
        self.ui.add_input_button.clicked.connect(self.add_input)

        # Add Output Button
        self.ui.add_output_button.clicked.connect(self.add_output)

        # Right-Click Menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.launch_context_menu)

        # Data
        self.index = index
        self.inputs = []
        self.outputs = []

    def launch_context_menu(self, pos):
        menu = qtw.QMenu(self)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_step)
        menu.exec_(self.mapToGlobal(pos))

    def rename_step(self):
        self.s_step_renamed.emit(self.index, self.ui.pipeline_step_name_lineedit.text())

    def set_name(self, new_name: str):
        self.ui.pipeline_step_name_lineedit.setText(new_name)

    def delete_step(self):
        print(f"Deleting Step at index: {self.index}")
        self.s_step_deleted.emit(self.index)
        self.deleteLater()

    # --------------
    # Inputs/Outputs

    # Input Handling
    def add_input(self):
        self.inputs.append(PipelineInputGUI(len(self.inputs), self))
        self.ui.inputs_layout.addWidget(self.inputs[-1])
        self.inputs[-1].s_remove.connect(self.remove_input)
        self.inputs[-1].s_modified.connect(self.modified_input)
        self.s_input_added.emit(self.index)

    def remove_input(self, input_index: int):
        self.s_input_removed.emit(self.index, input_index)
        for i in range(input_index + 1, len(self.inputs)):
            self.inputs[i].index -= 1
        del self.inputs[input_index]

    def modified_input(self, input_index: int, data_field: IODataEnum, data: str):
        self.s_input_modified.emit(self.index, input_index, data_field, data)

    # Output Handling
    def add_output(self):
        self.outputs.append(PipelineOutputGUI(len(self.outputs), self))
        self.ui.outputs_layout.addWidget(self.outputs[-1])
        self.outputs[-1].s_remove.connect(self.remove_output)
        self.outputs[-1].s_modified.connect(self.modified_output)
        self.s_output_added.emit(self.index)

    def remove_output(self, output_index: int):
        for i in range(output_index + 1, len(self.outputs)):
            self.outputs[i].index -= 1
        del self.outputs[output_index]
        self.s_output_removed.emit(self.index, output_index)

    def modified_output(self, output_index: int, data_field: IODataEnum, data: str):
        self.s_output_modified.emit(self.index, output_index, data_field, data)

    # Serialization
    def load_input(self, asset_type):
        self.inputs.append(PipelineInputGUI(len(self.inputs), self))
        self.ui.inputs_layout.addWidget(self.inputs[-1])
        self.inputs[-1].s_remove.connect(self.remove_input)
        self.inputs[-1].s_modified.connect(self.modified_input)

    def load_output(self, asset_type):
        self.outputs.append(PipelineOutputGUI(len(self.outputs), self))
        self.ui.outputs_layout.addWidget(self.outputs[-1])
        self.outputs[-1].s_remove.connect(self.remove_output)
        self.outputs[-1].s_modified.connect(self.modified_output)


class PipelineInputGUI(qtw.QWidget):
    s_remove = qtc.pyqtSignal(int) # input index
    s_modified = qtc.pyqtSignal(int, IODataEnum, str)  # input index, data type, data

    def __init__(self, index: int, parent=None):

        # GUI
        super().__init__(parent)
        self.ui = Ui_pipeline_step_input()
        self.ui.setupUi(self)
        self.ui.remove_input_button.clicked.connect(self.remove)
        self.ui.input_name_combobox.activated.connect(self.selected_output)

        # Data
        self.index = index

    def remove(self):
        self.s_remove.emit(self.index)
        self.deleteLater()

    def selected_output(self):
        self.s_modified.emit(self.index, IODataEnum.SelectedOutput, self.ui.input_name_combobox.currentText())

    def set_possible_outputs(self, outputs:list):
        self.ui.input_name_combobox.clear()
        self.ui.input_name_combobox.addItem("----")
        self.ui.input_name_combobox.model().item(0).setEnabled(False)
        self.ui.input_name_combobox.addItems(outputs)

    def set_selection_with_text(self, text: str):
        index = self.ui.input_name_combobox.findText(text)
        if index == -1:
            raise Exception("text not in combobox")
        self.ui.input_name_combobox.setCurrentIndex(index)


class PipelineOutputGUI(qtw.QWidget):
    s_remove = qtc.pyqtSignal(int) # output index
    s_modified = qtc.pyqtSignal(int, IODataEnum, str)  # output index, data type, data

    def __init__(self, index, parent=None):

        # GUI
        super().__init__(parent)
        self.ui = Ui_pipeline_step_output()
        self.ui.setupUi(self)
        self.ui.remove_output_button.clicked.connect(self.remove)
        self.ui.output_name_lineedit.editingFinished.connect(self.changed_name)

        # Data
        self.index = index

    def remove(self):
        self.s_remove.emit(self.index)
        self.deleteLater()

    def changed_name(self):
        self.s_modified.emit(self.index, IODataEnum.Name, self.ui.output_name_lineedit.text())

    def set_name(self, new_name: str):
        self.ui.output_name_lineedit.setText(new_name)
