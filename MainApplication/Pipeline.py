import json
from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

import pipelineServer
from pipeline_step_GUI import Ui_pipeline_step
from pipeline_step_input_GUI import Ui_pipeline_step_input
from pipeline_step_output_GUI import Ui_pipeline_step_output


class Pipeline(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.name = "Pipeline_1"
        self.project_dir = Path()
        self.pipeline_steps = []
        self.io_connections = {}
        self.step_id_counter = 0

        layout = qtw.QVBoxLayout()
        self.name_line_edit = qtw.QLineEdit("Pipeline Name")
        self.name_line_edit.setText(self.name)
        layout.addWidget(self.name_line_edit)

        layout_1 = qtw.QHBoxLayout()

        # Scroll Area for Pipeline Steps
        self.scroll_bar = qtw.QScrollArea(self)
        self.scroll_bar.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll_bar.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scroll_bar.setWidgetResizable(True)

        self.scrollbar_layout = qtw.QHBoxLayout()
        self.scrollable_widget = qtw.QWidget()
        self.scrollable_widget.setLayout(self.scrollbar_layout)
        self.scroll_bar.setWidget(self.scrollable_widget)

        layout_1.addWidget(self.scroll_bar)

        # Edit Pipeline Buttons
        button_layout = qtw.QVBoxLayout()
        # Add Step Button
        add_step_button = qtw.QPushButton("Add Step")
        add_step_button.setMinimumSize(100, 100)
        add_step_button.clicked.connect(self.add_pipeline_step)
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

    def set_project_dir(self, project_dir: Path):
        self.project_dir = project_dir

    def pipeline_name_changed(self):
        text = self.name_line_edit.text()
        if " " in text:
            print("name contains space")
            self.name_line_edit.setText(self.name)
            return
        self.name = text

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
        pass

    # -------------------------
    # Add/Remove Pipeline Steps
    # -------------------------

    def add_pipeline_step(self):
        self.pipeline_steps.append(PipelineStep(self, f"s{self.step_id_counter}", len(self.pipeline_steps)))
        self.step_id_counter += 1
        self.scrollable_widget.layout().addWidget(self.pipeline_steps[len(self.pipeline_steps) - 1])
        self.pipeline_steps[len(self.pipeline_steps) - 1].outputs_changed_signal.connect(self.pipeline_steps_outputs_changed)
        self.pipeline_steps[len(self.pipeline_steps) - 1].step_deleted_signal.connect(self.pipeline_step_deleted)
        self.pipeline_steps[len(self.pipeline_steps) - 1].io_mapped_signal.connect(self.connect_step_io)

        self.pipeline_steps[len(self.pipeline_steps) - 1].input_added_signal.connect(self.input_added)
        self.pipeline_steps[len(self.pipeline_steps) - 1].input_deleted_signal.connect(self.input_deleted)

        self.pipeline_steps[len(self.pipeline_steps) - 1].output_deleted_signal.connect(self.output_deleted)

    def pipeline_step_deleted(self, index: int):
        # Delete Input IO Connections of Pipeline Step
        for i in self.pipeline_steps[index].inputs:
            self.delete_io_connection_if_exists(i.uid)

        # Delete Output IO Connections of Pipeline Step
        for o in self.pipeline_steps[index].outputs:
            output_list = list(self.io_connections.values())
            indices = []
            for i in range(len(output_list)):
                if output_list[i] == o.uid:
                    indices.append(i)
            input_list = list(self.io_connections.keys())
            for i in indices:
                del self.io_connections[input_list[i]]

        # Delete Pipeline Step from List and correct indices
        for i in range(index + 1, len(self.pipeline_steps)):
            self.pipeline_steps[i].index -= 1
        del self.pipeline_steps[index]

    # ---------------
    # I/O Connections
    # ---------------

    def pipeline_steps_outputs_changed(self, index: int):
        print("outputs changed")
        pipeline_outputs = []
        for k in range(len(self.pipeline_steps)):
            if k > index:
                for i in self.pipeline_steps[k].inputs:
                    i.set_possible_outputs(pipeline_outputs)
                    self.delete_io_connection_if_exists(i.uid)
            for o in self.pipeline_steps[k].outputs:
                pipeline_outputs.append(o.uid)
        print(self.io_connections)

    def connect_step_io(self, in_id: str, out_id: str):
        self.io_connections[in_id] = out_id
        print(self.io_connections)

    def input_added(self, step_index: int, input_index: int):
        pipeline_outputs = []
        for k in range(0, step_index):
            for o in self.pipeline_steps[k].outputs:
                pipeline_outputs.append(o.uid)
        self.pipeline_steps[step_index].inputs[input_index].set_possible_outputs(pipeline_outputs)

    def input_deleted(self, uid: str):
        self.delete_io_connection_if_exists(uid)
        print(self.io_connections)

    def output_deleted(self, uid: str):
        connected_outputs = list(self.io_connections.values())
        if uid in connected_outputs:
            key = list(self.io_connections.keys())[connected_outputs.index(uid)]
            del self.io_connections[key]
        print(self.io_connections)

    def delete_io_connection_if_exists(self, input_id: str):
        if input_id in self.io_connections:
            del self.io_connections[input_id]

    # -------------
    # Serialization
    # -------------

    def save(self):
        # Collect Save Data
        step_data = []
        for i in range(len(self.pipeline_steps)):
            step_data.append(self.pipeline_steps[i].save_pipeline_step())
        data = {
            "name": self.name,
            "io_connections": self.io_connections,
            "step_id_counter": self.step_id_counter,
            "steps": step_data
            }

        # Write Data
        path = self.project_dir / "pipelines"
        if not path.exists():
            path.mkdir(parents=True)
        path = path / f"{self.name}.json"
        if not path.is_file():
            path.touch()
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))
            f.close()

    def load(self, path: Path):
        for s in self.pipeline_steps:
            s.delete_step() # TODO(BUG): does not delete all steps
        with path.open("r", encoding="utf-8")as f:
            data = json.loads(f.read())
            self.name = data["name"]
            self.name_line_edit.setText(self.name)
            self.step_id_counter = data["step_id_counter"]

            # Load Steps
            for i in data["steps"]:
                self.pipeline_steps.append(PipelineStep(self, i["id"], len(self.pipeline_steps)))

                # Setup necessary signals for pipeline steps
                self.scrollable_widget.layout().addWidget(self.pipeline_steps[len(self.pipeline_steps) - 1])
                self.pipeline_steps[len(self.pipeline_steps) - 1].outputs_changed_signal.connect(
                    self.pipeline_steps_outputs_changed)
                self.pipeline_steps[len(self.pipeline_steps) - 1].step_deleted_signal.connect(
                    self.pipeline_step_deleted)
                self.pipeline_steps[len(self.pipeline_steps) - 1].io_mapped_signal.connect(self.connect_step_io)

                self.pipeline_steps[len(self.pipeline_steps) - 1].input_added_signal.connect(self.input_added)
                self.pipeline_steps[len(self.pipeline_steps) - 1].input_deleted_signal.connect(self.input_deleted)

                self.pipeline_steps[len(self.pipeline_steps) - 1].output_deleted_signal.connect(self.output_deleted)
                self.pipeline_steps[len(self.pipeline_steps) - 1].load_pipeline_step(i)

            # Wrangle IO
            self.pipeline_steps_outputs_changed(0)
            self.io_connections = data["io_connections"]
            print(self.io_connections)
            for k in self.io_connections:
                for s in self.pipeline_steps:
                    for i in s.inputs:
                        if i.uid == k:
                            i.set_selection_with_text(self.io_connections[k])
            # TODO: Optimize search


class PipelineStep(qtw.QWidget):
    # Signals
    input_added_signal = qtc.pyqtSignal(int, int)
    input_deleted_signal = qtc.pyqtSignal(str)

    outputs_changed_signal = qtc.pyqtSignal(int)
    output_deleted_signal = qtc.pyqtSignal(str)

    step_deleted_signal = qtc.pyqtSignal(int)
    io_mapped_signal = qtc.pyqtSignal(str, str)

    def __init__(self, parent, uid: str, index: int):
        # GUI
        super().__init__(parent)

        self.ui_pipeline_step = Ui_pipeline_step()
        self.ui_pipeline_step.setupUi(self)

        self.ui_pipeline_step.add_output_button.clicked.connect(self.add_output)
        self.ui_pipeline_step.add_input_button.clicked.connect(self.add_input)

        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

        # Data
        self.name = f"step_{uid}"
        self.inputs = []
        self.outputs = []
        self.uid = uid
        self.index = index
        self.input_id_counter = 0
        self.output_id_counter = 0

        self.ui_pipeline_step.pipeline_step_name_lineedit.setText(self.name)

    def open_context_menu(self, pos):
        menu = qtw.QMenu()

        delete_option = menu.addAction("Delete Step")
        delete_option.triggered.connect(self.delete_step)

        menu.exec_(self.mapToGlobal(pos))

    def delete_step(self):
        self.step_deleted_signal.emit(self.index)
        self.deleteLater()

    def input_mapped(self, in_id: str, out_id: str):
        self.io_mapped_signal.emit(in_id, out_id)

    # -------------------------
    # Add/Remove Inputs/Outputs
    # -------------------------

    def add_input(self):
        print("Adding Input")
        self.inputs.append(PipelineStepInput(self, f"{self.uid}i{self.input_id_counter}", len(self.inputs)))
        self.input_id_counter += 1
        self.ui_pipeline_step.inputs_layout.addWidget(self.inputs[len(self.inputs) - 1])
        self.inputs[len(self.inputs) - 1].input_mapped.connect(self.input_mapped)
        self.inputs[len(self.inputs) - 1].input_deleted.connect(self.input_deleted)
        self.input_added_signal.emit(self.index, self.inputs[len(self.inputs) - 1].index)

    def input_deleted(self, index):
        print("Deleting Input")
        self.input_deleted_signal.emit( self.inputs[index].uid)
        for i in range(index+1, len(self.inputs)):
            self.inputs[i].index -= 1
        del self.inputs[index]

    def add_output(self):
        print("Adding Output")
        self.outputs.append(PipelineStepOutput(self, f"{self.uid}o{self.output_id_counter}", len(self.outputs)))
        self.output_id_counter += 1
        self.ui_pipeline_step.outputs_layout.addWidget(self.outputs[len(self.outputs) - 1])
        self.outputs[len(self.outputs) - 1].output_deleted.connect(self.output_deleted)
        self.outputs_changed_signal.emit(self.index)

    def output_deleted(self, index):
        print("Deleting Output")
        self.output_deleted_signal.emit(self.outputs[index].uid)
        for i in range(index+1, len(self.outputs)):
            self.outputs[i].index -= 1
        del self.outputs[index]
        self.outputs_changed_signal.emit(self.index)

    # -------------
    # Serialization
    # -------------
    def save_pipeline_step(self):
        inputs_data = []
        for i in range(len(self.inputs)):
            inputs_data.append(self.inputs[i].save_input())
        outputs_data = []
        for i in range(len(self.outputs)):
            outputs_data.append(self.outputs[i].save_output())
        data = {
            "name": self.name,
            "id": self.uid,
            "input_id_counter": self.input_id_counter,
            "output_id_counter": self.output_id_counter,
            "inputs": inputs_data,
            "outputs": outputs_data
            }
        return data

    def load_pipeline_step(self, data: dict):
        self.name = data["name"]
        self.input_id_counter = data["input_id_counter"]
        self.output_id_counter = data["output_id_counter"]

        # load inputs
        for i in data["inputs"]:
            self.inputs.append(PipelineStepInput(self, i["id"], len(self.inputs)))
            self.ui_pipeline_step.inputs_layout.addWidget(self.inputs[len(self.inputs) - 1])
            self.inputs[len(self.inputs) - 1].input_mapped.connect(self.input_mapped)
            self.inputs[len(self.inputs) - 1].input_deleted.connect(self.input_deleted)

        # load outputs
        for o in data["outputs"]:
            self.outputs.append(PipelineStepOutput(self, o["id"], len(self.outputs)))
            self.ui_pipeline_step.outputs_layout.addWidget(self.outputs[len(self.outputs) - 1])
            self.outputs[len(self.outputs) - 1].output_deleted.connect(self.output_deleted)
            self.outputs[len(self.outputs) - 1].load_output(o)


class PipelineStepInput(qtw.QWidget):

    # Signals
    input_deleted = qtc.pyqtSignal(int)
    input_mapped = qtc.pyqtSignal(str, str)

    def __init__(self, parent, uid: str, index: int):
        # GUI
        super(PipelineStepInput, self).__init__(parent)
        self.ui_pipeline_step_input = Ui_pipeline_step_input()
        self.ui_pipeline_step_input.setupUi(self)
        self.ui_pipeline_step_input.remove_input_button.clicked.connect(self.delete_input)
        self.ui_pipeline_step_input.input_name_combobox.activated.connect(self.output_selected)

        # Data
        self.index = index
        self.uid = uid

    def set_selection_with_text(self, text: str):
        index = self.ui_pipeline_step_input.input_name_combobox.findText(text)
        if index == -1:
            raise Exception("text not in combobox")
        self.ui_pipeline_step_input.input_name_combobox.setCurrentIndex(index)
        pass

    def delete_input(self):
        self.input_deleted.emit(self.index)
        self.deleteLater()

    def set_possible_outputs(self, outputs: list):
        self.ui_pipeline_step_input.input_name_combobox.clear()
        self.ui_pipeline_step_input.input_name_combobox.addItem("----")
        self.ui_pipeline_step_input.input_name_combobox.model().item(0).setEnabled(False)
        self.ui_pipeline_step_input.input_name_combobox.addItems(outputs)

    def output_selected(self):
        self.input_mapped.emit(self.uid, self.ui_pipeline_step_input.input_name_combobox.currentText())

    def save_input(self):
        return {"id": self.uid}


class PipelineStepOutput(qtw.QWidget):

    # Signals
    output_deleted = qtc.pyqtSignal(int)

    def __init__(self, parent, uid: str, index: int):
        # GUI
        super(PipelineStepOutput, self).__init__(parent)
        self.ui_pipeline_step_output = Ui_pipeline_step_output()
        self.ui_pipeline_step_output.setupUi(self)
        self.ui_pipeline_step_output.remove_output_button.clicked.connect(self.delete_output)

        # Data
        self.index = index
        self.uid = uid
        self.name = f"output_{uid}"

        self.ui_pipeline_step_output.output_name_lineedit.setText(self.name)
        self.ui_pipeline_step_output.output_name_lineedit.editingFinished.connect(self.renamed_output)

    def delete_output(self):
        self.output_deleted.emit(self.index)
        self.deleteLater()

    def renamed_output(self):
        user_name = self.ui_pipeline_step_output.output_name_lineedit.text()

        self.name = f"{user_name}_{self.uid}"
        self.ui_pipeline_step_output.output_name_lineedit.setText(self.name)

    def save_output(self):
        return {"id": self.uid, "name": self.name}

    def load_output(self, data: dict):
        self.name = data["name"]
