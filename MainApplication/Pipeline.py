from PyQt5 import QtWidgets as qtw
from pipeline_step_GUI import Ui_pipeline_step


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


class PipelineStep(qtw.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui_pipeline_step = Ui_pipeline_step()
        self.ui_pipeline_step.setupUi(self)

        # Set Pipeline Steps
        step_list = ["Modeling", "UV Mapping", "Textures", "Game Import"]
        self.ui_pipeline_step.pipeline_step_combo_box.addItems(step_list)

        # Set Program for Pipeline Steps
        program_list = ["Blender", "Substance Painter", "Unity"]
        self.ui_pipeline_step.step_program_combo_box.addItems(program_list)
