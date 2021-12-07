# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pipeline_step_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pipeline_step(object):
    def setupUi(self, pipeline_step):
        pipeline_step.setObjectName("pipeline_step")
        pipeline_step.resize(450, 208)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pipeline_step.sizePolicy().hasHeightForWidth())
        pipeline_step.setSizePolicy(sizePolicy)
        pipeline_step.setMinimumSize(QtCore.QSize(450, 110))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(pipeline_step)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pipeline_step_name_label = QtWidgets.QLabel(pipeline_step)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pipeline_step_name_label.sizePolicy().hasHeightForWidth())
        self.pipeline_step_name_label.setSizePolicy(sizePolicy)
        self.pipeline_step_name_label.setObjectName("pipeline_step_name_label")
        self.verticalLayout.addWidget(self.pipeline_step_name_label)
        self.pipeline_step_name_lineedit = QtWidgets.QLineEdit(pipeline_step)
        self.pipeline_step_name_lineedit.setObjectName("pipeline_step_name_lineedit")
        self.verticalLayout.addWidget(self.pipeline_step_name_lineedit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.program_label = QtWidgets.QLabel(pipeline_step)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_label.sizePolicy().hasHeightForWidth())
        self.program_label.setSizePolicy(sizePolicy)
        self.program_label.setMinimumSize(QtCore.QSize(60, 20))
        self.program_label.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.program_label.setFont(font)
        self.program_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.program_label.setObjectName("program_label")
        self.horizontalLayout_3.addWidget(self.program_label)
        self.program_combobox = QtWidgets.QComboBox(pipeline_step)
        self.program_combobox.setObjectName("program_combobox")
        self.horizontalLayout_3.addWidget(self.program_combobox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.program_settings = PipelineStepSettingsView(pipeline_step)
        self.program_settings.setMinimumSize(QtCore.QSize(0, 10))
        self.program_settings.setObjectName("program_settings")
        self.verticalLayout.addWidget(self.program_settings)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputs_layout = QtWidgets.QVBoxLayout()
        self.inputs_layout.setContentsMargins(0, -1, -1, -1)
        self.inputs_layout.setObjectName("inputs_layout")
        self.inputs_label = QtWidgets.QLabel(pipeline_step)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputs_label.sizePolicy().hasHeightForWidth())
        self.inputs_label.setSizePolicy(sizePolicy)
        self.inputs_label.setObjectName("inputs_label")
        self.inputs_layout.addWidget(self.inputs_label)
        self.add_input_button = QtWidgets.QPushButton(pipeline_step)
        self.add_input_button.setMinimumSize(QtCore.QSize(100, 20))
        self.add_input_button.setMaximumSize(QtCore.QSize(16777215, 20))
        self.add_input_button.setObjectName("add_input_button")
        self.inputs_layout.addWidget(self.add_input_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.inputs_layout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.inputs_layout)
        self.line = QtWidgets.QFrame(pipeline_step)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.outputs_layout = QtWidgets.QVBoxLayout()
        self.outputs_layout.setContentsMargins(0, -1, -1, -1)
        self.outputs_layout.setObjectName("outputs_layout")
        self.outputs_label = QtWidgets.QLabel(pipeline_step)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputs_label.sizePolicy().hasHeightForWidth())
        self.outputs_label.setSizePolicy(sizePolicy)
        self.outputs_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.outputs_label.setObjectName("outputs_label")
        self.outputs_layout.addWidget(self.outputs_label)
        self.add_output_button = QtWidgets.QPushButton(pipeline_step)
        self.add_output_button.setMinimumSize(QtCore.QSize(100, 20))
        self.add_output_button.setMaximumSize(QtCore.QSize(16777215, 20))
        self.add_output_button.setObjectName("add_output_button")
        self.outputs_layout.addWidget(self.add_output_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.outputs_layout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.outputs_layout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.line_2 = QtWidgets.QFrame(pipeline_step)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)

        self.retranslateUi(pipeline_step)
        QtCore.QMetaObject.connectSlotsByName(pipeline_step)

    def retranslateUi(self, pipeline_step):
        _translate = QtCore.QCoreApplication.translate
        pipeline_step.setWindowTitle(_translate("pipeline_step", "Form"))
        self.pipeline_step_name_label.setText(_translate("pipeline_step", "Pipeline Step Name"))
        self.program_label.setText(_translate("pipeline_step", "Program"))
        self.inputs_label.setText(_translate("pipeline_step", "Inputs"))
        self.add_input_button.setText(_translate("pipeline_step", "+"))
        self.outputs_label.setText(_translate("pipeline_step", "Outputs"))
        self.add_output_button.setText(_translate("pipeline_step", "+"))
from MainApplication.PipelineConfigurator.pipelineStepSettingsView import PipelineStepSettingsView