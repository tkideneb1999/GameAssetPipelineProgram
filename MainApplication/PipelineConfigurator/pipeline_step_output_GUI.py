# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pipeline_step_output_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pipeline_step_output(object):
    def setupUi(self, pipeline_step_output):
        pipeline_step_output.setObjectName("pipeline_step_output")
        pipeline_step_output.resize(200, 73)
        self.horizontalLayout = QtWidgets.QHBoxLayout(pipeline_step_output)
        self.horizontalLayout.setContentsMargins(4, 2, 4, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.id_d_label = QtWidgets.QLabel(pipeline_step_output)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_d_label.sizePolicy().hasHeightForWidth())
        self.id_d_label.setSizePolicy(sizePolicy)
        self.id_d_label.setObjectName("id_d_label")
        self.horizontalLayout_2.addWidget(self.id_d_label)
        self.id_label = QtWidgets.QLabel(pipeline_step_output)
        self.id_label.setObjectName("id_label")
        self.horizontalLayout_2.addWidget(self.id_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.output_type_combobox = QtWidgets.QComboBox(pipeline_step_output)
        self.output_type_combobox.setMinimumSize(QtCore.QSize(150, 0))
        self.output_type_combobox.setObjectName("output_type_combobox")
        self.verticalLayout.addWidget(self.output_type_combobox)
        self.output_name_lineedit = QtWidgets.QLineEdit(pipeline_step_output)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_name_lineedit.sizePolicy().hasHeightForWidth())
        self.output_name_lineedit.setSizePolicy(sizePolicy)
        self.output_name_lineedit.setMinimumSize(QtCore.QSize(150, 0))
        self.output_name_lineedit.setObjectName("output_name_lineedit")
        self.verticalLayout.addWidget(self.output_name_lineedit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.remove_output_button = QtWidgets.QPushButton(pipeline_step_output)
        self.remove_output_button.setMaximumSize(QtCore.QSize(32, 16777215))
        self.remove_output_button.setObjectName("remove_output_button")
        self.horizontalLayout.addWidget(self.remove_output_button)

        self.retranslateUi(pipeline_step_output)
        QtCore.QMetaObject.connectSlotsByName(pipeline_step_output)

    def retranslateUi(self, pipeline_step_output):
        _translate = QtCore.QCoreApplication.translate
        pipeline_step_output.setWindowTitle(_translate("pipeline_step_output", "Form"))
        self.id_d_label.setText(_translate("pipeline_step_output", "uid:"))
        self.id_label.setText(_translate("pipeline_step_output", "id"))
        self.remove_output_button.setText(_translate("pipeline_step_output", "-"))
