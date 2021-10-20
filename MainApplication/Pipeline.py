from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

import pipelineServer
from pipeline_step_GUI import Ui_pipeline_step
from pipeline_step_input_GUI import Ui_pipeline_step_input
from pipeline_step_output_GUI import Ui_pipeline_step_output


class Pipeline(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.pipeline_steps = []
        self.io_connections = {}
        self.step_id_counter = 0

        layout = qtw.QHBoxLayout()

        # Scroll Area for Pipeline Steps
        self.scroll_bar = qtw.QScrollArea(self)
        self.scroll_bar.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll_bar.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scroll_bar.setWidgetResizable(True)

        self.scrollbar_layout = qtw.QHBoxLayout()
        self.scrollable_widget = qtw.QWidget()
        self.scrollable_widget.setLayout(self.scrollbar_layout)
        self.scroll_bar.setWidget(self.scrollable_widget)

        layout.addWidget(self.scroll_bar)

        # Edit Pipeline Buttons
        button_layout = qtw.QVBoxLayout()
        # Add Step Button
        add_step_button = qtw.QPushButton("Add Step")
        add_step_button.setMinimumSize(100, 100)
        add_step_button.clicked.connect(self.add_pipeline_step)
        button_layout.addWidget(add_step_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    # -------------------------
    # Add/Remove Pipeline Steps
    # -------------------------

    def add_pipeline_step(self):
        self.pipeline_steps.append(PipelineStep(self, f"s{self.step_id_counter}", len(self.pipeline_steps)))
        self.step_id_counter += 1
        self.scrollable_widget.layout().addWidget(self.pipeline_steps[len(self.pipeline_steps) - 1])
        self.pipeline_steps[len(self.pipeline_steps) - 1].io_changed.connect(self.pipeline_steps_io_changed)
        self.pipeline_steps[len(self.pipeline_steps) - 1].step_deleted.connect(self.pipeline_step_deleted)

    def pipeline_step_deleted(self, index: int):
        for i in range(index + 1, len(self.pipeline_steps)):
            self.pipeline_steps[i].index -= 1
        del self.pipeline_steps[index]

    def pipeline_steps_io_changed(self):
        print("outputs changed")
        pipeline_outputs = []
        for k in range(len(self.pipeline_steps)):
            for i in self.pipeline_steps[k].inputs:
                i.set_possible_outputs(pipeline_outputs)
            for o in self.pipeline_steps[k].outputs:
                pipeline_outputs.append(o.uid)
            # TODO: collect all outputs from pipeline steps
            # TODO: set all outputs correctly in the input comboboxes

    def connect_step_io(self):
        pass


class PipelineStep(qtw.QWidget):
    # Signals
    io_changed = qtc.pyqtSignal()
    step_deleted = qtc.pyqtSignal(int)

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
        self.inputs = []
        self.outputs = []
        self.uid = uid
        self.index = index
        self.input_id_counter = 0
        self.output_id_counter = 0

    def open_context_menu(self, pos):
        menu = qtw.QMenu()

        delete_option = menu.addAction("Delete Step")
        delete_option.triggered.connect(self.delete_step)

        menu.exec_(self.mapToGlobal(pos))

    def delete_step(self):
        self.step_deleted.emit(self.index)
        self.deleteLater()

    # -------------------------
    # Add/Remove Inputs/Outputs
    # -------------------------

    def add_input(self):
        self.inputs.append(PipelineStepInput(self, f"{self.uid}i{self.input_id_counter}", len(self.inputs)))
        self.input_id_counter += 1
        self.ui_pipeline_step.inputs_layout.addWidget(self.inputs[len(self.inputs) - 1])
        self.io_changed.emit()

    def input_deleted(self, index):
        for i in range(index+1, len(self.inputs)):
            self.inputs[i].index -= 1
        del self.inputs[index]
        self.io_changed.emit()

    def add_output(self):
        self.outputs.append(PipelineStepOutput(self, f"{self.uid}o{self.output_id_counter}", len(self.outputs)))
        self.output_id_counter += 1
        self.ui_pipeline_step.outputs_layout.addWidget(self.outputs[len(self.outputs) - 1])
        self.outputs[len(self.outputs) - 1].output_deleted.connect(self.output_deleted)
        self.io_changed.emit()

    def output_deleted(self, index):
        for i in range(index+1, len(self.outputs)):
            self.outputs[i].index -= 1
        del self.outputs[index]
        self.io_changed.emit()


class PipelineStepInput(qtw.QWidget):

    # Signals
    input_deleted = qtc.pyqtSignal(int)

    def __init__(self, parent, uid: str, index: int):
        # GUI
        super(PipelineStepInput, self).__init__(parent)
        self.ui_pipeline_step_input = Ui_pipeline_step_input()
        self.ui_pipeline_step_input.setupUi(self)
        self.ui_pipeline_step_input.remove_input_button.clicked.connect(self.delete_input)

        # Data
        self.index = index
        self.uid = uid

    def delete_input(self):
        self.input_deleted.emit(self.index)
        self.deleteLater()

    def set_possible_outputs(self, outputs: list):
        self.ui_pipeline_step_input.input_name_combobox.clear()
        self.ui_pipeline_step_input.input_name_combobox.addItems(outputs)

    # TODO: Pipeline Input: Emit Signal if mapped output changed


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

    def delete_output(self):
        self.output_deleted.emit(self.index)
        self.deleteLater()
