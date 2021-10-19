from PyQt5 import QtWidgets as qtw

from pipeline_step_GUI import Ui_pipeline_step
from pipeline_step_input_GUI import Ui_pipeline_step_input
from pipeline_step_output_GUI import Ui_pipeline_step_output


class Pipeline(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = qtw.QHBoxLayout()
        self.pipeline_list = qtw.QListWidget(self)
        self.pipeline_list.setFlow(qtw.QListView.LeftToRight)
        layout.addWidget(self.pipeline_list)

        # Edit Pipeline Buttons
        button_layout = qtw.QVBoxLayout()
        # Add Step Button
        add_step_button = qtw.QPushButton("Add Step")
        add_step_button.setMinimumSize(100, 100)
        add_step_button.clicked.connect(self.add_pipeline_step)
        button_layout.addWidget(add_step_button)

        # Remove Step Button
        remove_step_button = qtw.QPushButton("Remove Step")
        remove_step_button.setMinimumSize(100, 100)
        remove_step_button.clicked.connect(self.remove_pipeline_step_gui)
        button_layout.addWidget(remove_step_button)

        # Edit Step Button
        edit_step_button = qtw.QPushButton("Edit Step")
        edit_step_button.setMinimumSize(100, 100)
        edit_step_button.clicked.connect(self.edit_pipeline_step)
        button_layout.addWidget(edit_step_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_pipeline_step(self):
        pipeline_step = PipelineStep(self)
        step_item = qtw.QListWidgetItem()
        step_item.setSizeHint(pipeline_step.sizeHint())
        self.pipeline_list.addItem(step_item)
        self.pipeline_list.setItemWidget(step_item, pipeline_step)

    def remove_pipeline_step_gui(self):
        selected_step = self.pipeline_list.selectedIndexes()  # Does not return a int but qt object
        if not selected_step:
            return
        else:
            for i in selected_step:
                self.pipeline_list.takeItem(i.row())

    def edit_pipeline_step(self):
        selected_step = self.pipeline_list.selectedIndexes()
        if not selected_step:
            return
        else:
            pass # TODO Implement Edit Pipeline Step


class PipelineStep(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui_pipeline_step = Ui_pipeline_step()
        self.ui_pipeline_step.setupUi(self)
        self.inputs = []
        self.outputs = []

        self.ui_pipeline_step.add_output_button.clicked.connect(self.add_output)

    def add_input(self):
        pass

    def add_output(self):
        self.outputs.append(PipelineStepOutput(self))
        self.ui_pipeline_step.outputs_layout.addWidget(self.outputs[len(self.outputs) - 1])


class PipelineStepInput(qtw.QWidget):
    def __init__(self, parent):
        super(PipelineStepInput, self).__init__(parent)
        self.ui_pipeline_step_input = Ui_pipeline_step_input()
        self.ui_pipeline_step_input.setupUi(self)


class PipelineStepOutput(qtw.QWidget):
    def __init__(self, parent):
        super(PipelineStepOutput, self).__init__(parent)
        self.ui_pipeline_step_output = Ui_pipeline_step_output()
        self.ui_pipeline_step_output.setupUi(self)

