from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from ..Core import pipeline as pipelineModule
from ..Core.settings import Settings
from .pipeline_step_GUI import Ui_pipeline_step
from .pipeline_step_input_GUI import Ui_pipeline_step_input
from .pipeline_step_output_GUI import Ui_pipeline_step_output


class PipelineConfigurator(qtw.QWidget):

    s_pipeline_saved = qtc.pyqtSignal(Path, str)

    def __init__(self, parent=None):
        super(PipelineConfigurator, self).__init__(parent)

        # Data
        self.project_dir: Path = Path()
        self.pipeline_name: str = "Pipeline_01"
        self.settings = Settings()
        self.settings.load()

        # Scroll Widget
        # <editor-fold, desc="Scroll Widget">
        layout = qtw.QVBoxLayout()
        self.name_line_edit = qtw.QLineEdit("Pipeline_Name")
        self.name_line_edit.setText(self.pipeline_name)
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
        # </editor-fold>

        self.step_uid_counter = 0
        self.step_widgets: list[PipelineStepView] = []

        # Buttons
        # <editor-fold, desc="Buttons">
        button_layout = qtw.QVBoxLayout()

        # Add Step Button
        add_step_button = qtw.QPushButton("Add Step")
        add_step_button.setMinimumSize(100, 100)
        add_step_button.clicked.connect(self.add_step)
        button_layout.addWidget(add_step_button)

        # Save Pipeline Button
        save_pipeline_button = qtw.QPushButton("Save")
        save_pipeline_button.setMinimumSize(100, 100)
        save_pipeline_button.clicked.connect(self.save)
        button_layout.addWidget(save_pipeline_button)

        # Load Pipeline Button
        load_pipeline_button = qtw.QPushButton("Load")
        load_pipeline_button.setMinimumSize(100, 100)
        load_pipeline_button.clicked.connect(self.load_pipeline_dialog)
        button_layout.addWidget(load_pipeline_button)

        layout_1.addLayout(button_layout)
        layout.addLayout(layout_1)
        self.setLayout(layout)
        # </editor-fold>

    def set_project_dir(self, project_dir: Path) -> None:
        self.project_dir = project_dir

    def pipeline_name_changed(self) -> None:
        text = self.name_line_edit.text()
        if " " in text:
            print(f"[GAPA] Pipeline Name contains spaces: {text}")
            self.name_line_edit.setText(self.pipeline_name)
            return
        if text == "":
            print(f"[GAPA] No name set")
            self.name_line_edit.setText(self.pipeline_name)
            return
        self.pipeline_name = text

    def add_step(self, load=False) -> None:
        self.step_widgets.append(PipelineStepView(len(self.step_widgets),
                                                  f"s{self.step_uid_counter}",
                                                  load=load,
                                                  parent=self))
        self.step_widgets[-1].s_step_removed.connect(self.remove_step)
        self.step_widgets[-1].s_update_inputs.connect(self.update_output_selection)

        self.step_uid_counter += 1
        self.scrollbar_layout.insertWidget(self.scrollbar_layout.count() - 1,
                                           self.step_widgets[-1])
        self.update_output_selection(self.step_widgets[-1].index)

    def remove_step(self, index: int) -> None:
        for s in range(index + 1, len(self.step_widgets)):
            self.step_widgets[s].index -= 1
        del self.step_widgets[index]
        self.update_output_selection(index)

    def io_changed(self, step_index: int, io_index: int):
        self.update_output_selection(step_index)

    def update_output_selection(self, start_step_index: int) -> None:
        pipeline_outputs = []
        for k in range(len(self.step_widgets)):
            if k >= start_step_index:
                for i in self.step_widgets[k].inputs:
                    i.set_possible_outputs(pipeline_outputs)
            for o in self.step_widgets[k].outputs:
                output = (o.uid, o.get_name())
                pipeline_outputs.append(output)

    def load_pipeline_dialog(self) -> None:
        file_dialog = qtw.QFileDialog(self)
        file_dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Pipeline File (*.json)")
        file_dialog.setViewMode(qtw.QFileDialog.Detail)
        result = file_dialog.exec_()
        if result == 0:
            return
        path = Path(file_dialog.selectedFiles()[0])
        self.load(path)

    def save(self):
        # instantiate Pipeline object
        pipeline = pipelineModule.Pipeline()
        pipeline.name = self.name_line_edit.text()
        pipeline.step_id_counter = self.step_uid_counter
        io_connections: dict[str, str] = {}
        for step in self.step_widgets:
            step_data = step.get_data()
            io_connections = {**io_connections, ** step_data[1]}
            pipeline.pipeline_steps.append(step_data[0])
        pipeline.io_connections = io_connections

        pipeline.save(self.project_dir / "pipelines")

    def load(self, path: Path):
        pipeline = pipelineModule.Pipeline()
        pipeline.load(path)
        for step in pipeline.pipeline_steps:
            self.add_step(load=True)
            self.step_widgets[-1].uid = step.uid
            self.step_widgets[-1].set_name(step.name)
            self.step_widgets[-1].set_up_signals()


class PipelineStepView(qtw.QWidget):
    # Step Signals
    s_step_removed = qtc.pyqtSignal(int)  # Step Index
    s_update_inputs = qtc.pyqtSignal(int)  # Step Index

    def __init__(self, index: int, uid, load=False, parent=None):
        super(PipelineStepView, self).__init__(parent)
        self.ui = Ui_pipeline_step()
        self.ui.setupUi(self)

        self.ui.pipeline_step_name_lineedit.setText(f"step_{uid}")

        # Data
        self.uid = uid
        self.index: int = index
        self.uses_configs = False

        self.input_uid_counter = 0
        self.inputs: list[PipelineInputView] = []

        self.output_uid_counter = 0
        self.outputs: list[PipelineOutputView] = []

        # Add IO Buttons
        self.ui.add_input_button.clicked.connect(self.add_input)
        self.ui.add_output_button.clicked.connect(self.add_output)

        # Program, Config Selection, Settings
        if not load:
            self.set_up_signals()

        settings = Settings()
        self.ui.program_combobox.addItems(settings.program_registration.get_program_list())
        self.ui.program_combobox.addItems(settings.plugin_registration.get_plugin_list())

        # Context Menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.launch_context_menu)

    def set_up_signals(self) -> None:
        self.ui.program_combobox.currentTextChanged.connect(self.select_program)
        self.ui.program_settings.s_selected_config.connect(self.select_config)

    def set_name(self, new_name: str) -> None:
        self.ui.pipeline_step_name_lineedit.setText(new_name)

    def launch_context_menu(self, pos) -> None:
        menu = qtw.QMenu(self)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_step)
        menu.exec_(self.mapToGlobal(pos))

    def delete_step(self) -> None:
        self.s_step_removed.emit(self.index)
        self.deleteLater()

    def add_input(self) -> None:
        self.inputs.append(PipelineInputView(len(self.inputs),
                                             f"{self.uid}.i{self.input_uid_counter}",
                                             parent=self))
        self.inputs[-1].s_remove.connect(self.remove_input)
        self.ui.inputs_layout.addWidget(self.inputs[-1])
        self.input_uid_counter += 1
        if not self.uses_configs:
            self.s_update_inputs.emit(self.index)

    def remove_input(self, index: int) -> None:
        for i in range(index + 1, len(self.inputs)):
            self.inputs[i].index -= 1
        del self.inputs[index]
        if not self.uses_configs:
            self.s_update_inputs.emit(self.index)

    def add_output(self) -> None:
        self.outputs.append(PipelineOutputView(len(self.outputs),
                                               f"{self.uid}.o{self.output_uid_counter}",
                                               parent=self))
        self.outputs[-1].s_remove.connect(self.remove_output)
        self.outputs[-1].s_renamed.connect(self.output_renamed)
        self.ui.outputs_layout.addWidget((self.outputs[-1]))
        self.output_uid_counter += 1
        if not self.uses_configs:
            self.s_update_inputs.emit(self.index)

    def output_renamed(self, index: int) -> None:
        self.s_update_inputs.emit(self.index)

    def remove_output(self, index: int) -> None:
        for i in range(index + 1, len(self.outputs)):
            self.outputs[i].index -= 1
        del self.outputs[index]
        if not self.uses_configs:
            self.s_update_inputs.emit(self.index)

    def select_program(self, new_program: str) -> None:
        configs_available = self.ui.program_settings.program_changed(new_program)
        self.uses_configs = configs_available
        self.set_io_button_interactivity(not configs_available)

    def select_config(self, config_name: str) -> None:  # TODO: What happens when configs not available
        # Delete all inputs/outputs
        inputs_len = len(self.inputs)
        for i in reversed(range(inputs_len)):
            self.inputs[i].remove()
        outputs_len = len(self.outputs)
        for o in reversed(range(outputs_len)):
            self.outputs[o].remove()

        config = self.ui.program_settings.settings.configs[config_name]
        for i in config["inputs"]:
            # Add Input
            self.add_input()
            # Rename Input
            self.inputs[-1].set_name(i[0])

        for o in config["outputs"]:
            # Add Output
            self.add_output()
            # Rename Output
            self.outputs[-1].set_name(o[0])
        self.s_update_inputs.emit(self.index)

    def get_data(self) -> tuple[pipelineModule.PipelineStep, dict[str, str]]:

        additional_settings = self.ui.program_settings.get_additional_settings()
        outputs_data = [o.get_data() for o in self.outputs]
        inputs_data = [i.get_data() for i in self.inputs]

        # Step Info
        pipeline_step = pipelineModule.PipelineStep(self.uid)
        pipeline_step.name = self.ui.pipeline_step_name_lineedit.text()
        pipeline_step.program = self.ui.program_combobox.currentText()
        pipeline_step.input_id_counter = self.input_uid_counter
        pipeline_step.output_id_counter = self.output_uid_counter

        # IO
        connections = {}
        for i in inputs_data:
            pipeline_step.inputs.append(i[0])
            connections[i[0].uid] = i[1]
        for o in outputs_data:
            pipeline_step.outputs.append(o)

        # Settings
        required_settings = self.ui.program_settings.get_required_settings()
        pipeline_step.is_plugin = required_settings["is_plugin"]
        pipeline_step.has_set_outputs = required_settings["has_set_outputs"]
        pipeline_step.export_all = required_settings["export_all"]
        pipeline_step.config = self.ui.program_settings.current_config()
        pipeline_step.additional_settings = additional_settings
        return pipeline_step, connections

    def set_data(self, step: pipelineModule.PipelineStep) -> None:
        # Pipeline Info
        self.uid = step.uid
        self.ui.pipeline_step_name_lineedit.setText(step.name)
        self.ui.program_combobox.setCurrentText(step.program)
        self.input_uid_counter = step.input_id_counter
        self.output_uid_counter = step.output_id_counter

        # Required_settings
        configs_available = self.ui.program_settings.program_changed(step.program)
        self.set_io_button_interactivity(not configs_available)
        if configs_available:
            self.ui.program_settings.config_changed(step.config)

        # Additional Settings
        self.ui.program_settings.set_additional_settings(step.additional_settings)

        for i in step.inputs:
            self.add_input()


    # Helpers
    def set_io_button_interactivity(self, is_active: bool) -> None:
        print(f"[GAPA] Setting add buttons enabled status to: {is_active}")
        self.ui.add_input_button.setEnabled(is_active)
        self.ui.add_output_button.setEnabled(is_active)


class PipelineInputView(qtw.QWidget):
    s_remove = qtc.pyqtSignal(int)

    def __init__(self, index: int, uid: str, parent=None):
        super(PipelineInputView, self).__init__(parent)
        self.ui = Ui_pipeline_step_input()
        self.ui.setupUi(self)
        self.ui.remove_input_button.clicked.connect(self.remove)

        self.index = index
        self.uid = uid
        self.name = ""
        self.possible_outputs: list[tuple[str, str]] = []  # uid, name

    def remove(self) -> None:
        self.s_remove.emit(self.index)
        self.deleteLater()

    def set_name(self, name):
        self.name = name
        self.ui.id_label.setText(f"{name} - {self.uid}")

    def set_data_type_combobox(self, data_types: list[str], current_data_type: str) -> None:
        self.ui.input_type_combo_box.clear()
        self.ui.input_type_combo_box.addItems(data_types)
        self.ui.input_type_combo_box.setCurrentText(current_data_type)

    def set_possible_outputs(self, outputs: list[tuple[str, str]]) -> bool:
        current_index = self.ui.input_name_combobox.currentIndex() - 1
        current_output_exists = False
        new_data_index = -1
        current_data: tuple[str, str] = tuple()
        if current_index >= 0:
            current_data = self.possible_outputs[current_index]

        self.possible_outputs = outputs

        if current_index >= 0:
            # Determine if current output still exists
            for po in range(len(self.possible_outputs)):
                if self.possible_outputs[po][0] == current_data[0]:
                    current_output_exists = True
                    new_data_index = po
                    break

        combobox_list = [f"{o[1]} - {o[0]}" for o in outputs]
        self.ui.input_name_combobox.clear()
        self.ui.input_name_combobox.addItem("----")
        self.ui.input_name_combobox.model().item(0).setEnabled(False)
        self.ui.input_name_combobox.addItems(combobox_list)

        if current_output_exists:
            self.ui.input_name_combobox.setCurrentIndex(new_data_index + 1)

        return current_output_exists

    def disable_customization(self, disabled: bool) -> None:
        self.ui.remove_input_button.setDisabled(disabled)
        self.ui.input_type_combo_box.setDisabled(disabled)

    def get_data(self) -> tuple[pipelineModule.PipelineInput, str]:
        input_type = self.ui.input_type_combo_box.currentText()
        output_index = self.ui.input_name_combobox.currentIndex()
        if output_index == 0:
            selected_output = None
        else:
            selected_output = self.possible_outputs[output_index - 1][0]
        pipeline_input = pipelineModule.PipelineInput(self.uid)
        pipeline_input.name = self.name
        return pipeline_input, selected_output

    def set_data(self, pipeline_input: pipelineModule.PipelineInput) -> None:
        self.uid = pipeline_input.uid
        self.name = pipeline_input.name



class PipelineOutputView(qtw.QWidget):
    s_remove = qtc.pyqtSignal(int)  # Output Index
    s_renamed = qtc.pyqtSignal(int, str)  # Output Index, New Name

    def __init__(self, index: int, uid: str, parent=None):
        super(PipelineOutputView, self).__init__(parent)
        self.ui = Ui_pipeline_step_output()
        self.ui.setupUi(self)
        self.ui.remove_output_button.clicked.connect(self.remove)
        self.ui.output_name_lineedit.editingFinished.connect(self.rename_output)

        self.index = index
        self.name = "output_uid"
        self.uid = uid
        self.ui.id_label.setText(uid)

    def remove(self) -> None:
        self.s_remove.emit(self.index)
        self.deleteLater()

    def get_name(self) -> str:
        return self.ui.output_name_lineedit.text()

    def set_name(self, name):
        self.ui.output_name_lineedit.setText(name)

    def rename_output(self):
        new_name = self.ui.output_name_lineedit.text()
        if " " in new_name:
            print(f"[GAPA] not a valid name, contains spaces: {new_name}")
            self.ui.output_name_lineedit.setText(self.name)
            return
        if new_name == "":
            print("[GAPA] output must be named")
            self.ui.output_name_lineedit.setText(self.name)
            return
        self.name = new_name
        self.s_renamed.emit(self.index, self.name)

    def set_data_type_combobox(self, data_types: list[str], current_data_type: str) -> None:
        self.ui.output_type_combobox.clear()
        self.ui.output_type_combobox.addItems(data_types)
        self.ui.output_type_combobox.setCurrentText(current_data_type)

    def disable_customization(self, disabled: bool) -> None:
        self.ui.output_name_lineedit.setReadOnly(disabled)
        self.ui.output_type_combobox.setDisabled(disabled)

    def get_data(self) -> pipelineModule.PipelineOutput:
        name = self.ui.output_name_lineedit.text()
        output_type = self.ui.output_type_combobox.currentText()
        pipeline_output = pipelineModule.PipelineOutput(self.uid)
        pipeline_output.name = self.name
        pipeline_output.data_type = output_type
        return pipeline_output
