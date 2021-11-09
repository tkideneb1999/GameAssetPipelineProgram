# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importWizard_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_import_Wizard(object):
    def setupUi(self, import_Wizard):
        import_Wizard.setObjectName("import_Wizard")
        import_Wizard.resize(756, 367)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(import_Wizard)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(-1, 0, -1, -1)
        self.main_layout.setObjectName("main_layout")
        self.asset_list_layout = QtWidgets.QVBoxLayout()
        self.asset_list_layout.setObjectName("asset_list_layout")
        self.asset_list_label = QtWidgets.QLabel(import_Wizard)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.asset_list_label.setFont(font)
        self.asset_list_label.setObjectName("asset_list_label")
        self.asset_list_layout.addWidget(self.asset_list_label)
        self.level_combobox = QtWidgets.QComboBox(import_Wizard)
        self.level_combobox.setObjectName("level_combobox")
        self.asset_list_layout.addWidget(self.level_combobox)
        self.asset_list = QtWidgets.QListWidget(import_Wizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_list.sizePolicy().hasHeightForWidth())
        self.asset_list.setSizePolicy(sizePolicy)
        self.asset_list.setMaximumSize(QtCore.QSize(200, 20000))
        self.asset_list.setObjectName("asset_list")
        self.asset_list_layout.addWidget(self.asset_list)
        self.asset_list_buttons_layout = QtWidgets.QHBoxLayout()
        self.asset_list_buttons_layout.setContentsMargins(-1, 0, -1, -1)
        self.asset_list_buttons_layout.setObjectName("asset_list_buttons_layout")
        self.add_asset_button = QtWidgets.QPushButton(import_Wizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_asset_button.sizePolicy().hasHeightForWidth())
        self.add_asset_button.setSizePolicy(sizePolicy)
        self.add_asset_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.add_asset_button.setObjectName("add_asset_button")
        self.asset_list_buttons_layout.addWidget(self.add_asset_button)
        self.asset_list_layout.addLayout(self.asset_list_buttons_layout)
        self.main_layout.addLayout(self.asset_list_layout)
        self.asset_details_pipeline_layout = QtWidgets.QVBoxLayout()
        self.asset_details_pipeline_layout.setContentsMargins(0, -1, -1, -1)
        self.asset_details_pipeline_layout.setObjectName("asset_details_pipeline_layout")
        self.asset_details_spacer_layout = QtWidgets.QHBoxLayout()
        self.asset_details_spacer_layout.setContentsMargins(-1, -1, 0, -1)
        self.asset_details_spacer_layout.setObjectName("asset_details_spacer_layout")
        self.asset_details_layout = QtWidgets.QFormLayout()
        self.asset_details_layout.setContentsMargins(0, -1, -1, -1)
        self.asset_details_layout.setObjectName("asset_details_layout")
        self.asset_name_d_label = QtWidgets.QLabel(import_Wizard)
        self.asset_name_d_label.setObjectName("asset_name_d_label")
        self.asset_details_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.asset_name_d_label)
        self.asset_name_label = QtWidgets.QLabel(import_Wizard)
        self.asset_name_label.setText("")
        self.asset_name_label.setObjectName("asset_name_label")
        self.asset_details_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.asset_name_label)
        self.asset_level_d_label = QtWidgets.QLabel(import_Wizard)
        self.asset_level_d_label.setObjectName("asset_level_d_label")
        self.asset_details_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.asset_level_d_label)
        self.asset_level_label = QtWidgets.QLabel(import_Wizard)
        self.asset_level_label.setText("")
        self.asset_level_label.setObjectName("asset_level_label")
        self.asset_details_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.asset_level_label)
        self.asset_pipeline_d_label = QtWidgets.QLabel(import_Wizard)
        self.asset_pipeline_d_label.setObjectName("asset_pipeline_d_label")
        self.asset_details_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.asset_pipeline_d_label)
        self.asset_pipeline_label = QtWidgets.QLabel(import_Wizard)
        self.asset_pipeline_label.setText("")
        self.asset_pipeline_label.setObjectName("asset_pipeline_label")
        self.asset_details_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.asset_pipeline_label)
        self.asset_tags_d_label = QtWidgets.QLabel(import_Wizard)
        self.asset_tags_d_label.setObjectName("asset_tags_d_label")
        self.asset_details_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.asset_tags_d_label)
        self.asset_tags_label = QtWidgets.QLabel(import_Wizard)
        self.asset_tags_label.setText("")
        self.asset_tags_label.setObjectName("asset_tags_label")
        self.asset_details_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.asset_tags_label)
        self.asset_comment_d_label = QtWidgets.QLabel(import_Wizard)
        self.asset_comment_d_label.setObjectName("asset_comment_d_label")
        self.asset_details_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.asset_comment_d_label)
        self.asset_comment_label = QtWidgets.QLabel(import_Wizard)
        self.asset_comment_label.setText("")
        self.asset_comment_label.setObjectName("asset_comment_label")
        self.asset_details_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.asset_comment_label)
        self.asset_details_spacer_layout.addLayout(self.asset_details_layout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.asset_details_spacer_layout.addItem(spacerItem)
        self.asset_details_pipeline_layout.addLayout(self.asset_details_spacer_layout)
        self.pipeline_outputs_layout = QtWidgets.QHBoxLayout()
        self.pipeline_outputs_layout.setContentsMargins(-1, 0, 0, -1)
        self.pipeline_outputs_layout.setObjectName("pipeline_outputs_layout")
        self.pipeline_layout = QtWidgets.QVBoxLayout()
        self.pipeline_layout.setContentsMargins(-1, 0, -1, -1)
        self.pipeline_layout.setObjectName("pipeline_layout")
        self.pipeline_label = QtWidgets.QLabel(import_Wizard)
        self.pipeline_label.setObjectName("pipeline_label")
        self.pipeline_layout.addWidget(self.pipeline_label)
        self.pipeline_list = QtWidgets.QListWidget(import_Wizard)
        self.pipeline_list.setFlow(QtWidgets.QListView.LeftToRight)
        self.pipeline_list.setObjectName("pipeline_list")
        self.pipeline_layout.addWidget(self.pipeline_list)
        self.pipeline_outputs_layout.addLayout(self.pipeline_layout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inputs_label = QtWidgets.QLabel(import_Wizard)
        self.inputs_label.setObjectName("inputs_label")
        self.verticalLayout.addWidget(self.inputs_label)
        self.inputs_list = QtWidgets.QListWidget(import_Wizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputs_list.sizePolicy().hasHeightForWidth())
        self.inputs_list.setSizePolicy(sizePolicy)
        self.inputs_list.setMaximumSize(QtCore.QSize(100, 16777215))
        self.inputs_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.inputs_list.setObjectName("inputs_list")
        self.verticalLayout.addWidget(self.inputs_list)
        self.pipeline_outputs_layout.addLayout(self.verticalLayout)
        self.asset_details_pipeline_layout.addLayout(self.pipeline_outputs_layout)
        self.main_layout.addLayout(self.asset_details_pipeline_layout)
        self.verticalLayout_2.addLayout(self.main_layout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.import_button = QtWidgets.QPushButton(import_Wizard)
        self.import_button.setObjectName("import_button")
        self.horizontalLayout_4.addWidget(self.import_button)
        self.cancel_Button = QtWidgets.QPushButton(import_Wizard)
        self.cancel_Button.setObjectName("cancel_Button")
        self.horizontalLayout_4.addWidget(self.cancel_Button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(import_Wizard)
        self.cancel_Button.clicked.connect(import_Wizard.reject)
        QtCore.QMetaObject.connectSlotsByName(import_Wizard)

    def retranslateUi(self, import_Wizard):
        _translate = QtCore.QCoreApplication.translate
        import_Wizard.setWindowTitle(_translate("import_Wizard", "Dialog"))
        self.asset_list_label.setText(_translate("import_Wizard", "Asset List"))
        self.add_asset_button.setText(_translate("import_Wizard", "Add Asset"))
        self.asset_name_d_label.setText(_translate("import_Wizard", "Name:"))
        self.asset_level_d_label.setText(_translate("import_Wizard", "Level:"))
        self.asset_pipeline_d_label.setText(_translate("import_Wizard", "Pipeline:"))
        self.asset_tags_d_label.setText(_translate("import_Wizard", "Tags:"))
        self.asset_comment_d_label.setText(_translate("import_Wizard", "Comment:"))
        self.pipeline_label.setText(_translate("import_Wizard", "Pipeline"))
        self.inputs_label.setText(_translate("import_Wizard", "Inputs"))
        self.import_button.setText(_translate("import_Wizard", "Import"))
        self.cancel_Button.setText(_translate("import_Wizard", "Cancel"))
