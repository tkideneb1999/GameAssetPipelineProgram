from PyQt5 import QtWidgets as qtw
from pipeline_step_GUI import Ui_pipeline_step

class PipelineConfigGUI(qtw.QWidget):
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
        add_step_button.clicked.connect(self.add_pipeline_step_gui)
        button_layout.addWidget(add_step_button)

        # Remove Step Button
        remove_step_button = qtw.QPushButton("Remove Step")
        remove_step_button.setMinimumSize(100, 100)
        remove_step_button.clicked.connect(self.remove_pipeline_step_gui)
        button_layout.addWidget(remove_step_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_pipeline_step_gui(self):
        pipeline_step = PipelineStepGUI(self)
        step_item = qtw.QListWidgetItem()
        step_item.setSizeHint(pipeline_step.sizeHint())
        self.pipeline_list.addItem(step_item)
        self.pipeline_list.setItemWidget(step_item, pipeline_step)

    def remove_pipeline_step_gui(self):
        selected_step = self.pipeline_list.selectedIndexes()
        if not selected_step:
            print("Nothing selected")
        else:
            for i in selected_step:
                self.pipeline_list.takeItem(i)



class PipelineStepGUI(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui_pipeline_step = Ui_pipeline_step()
        self.ui_pipeline_step.setupUi(self)

