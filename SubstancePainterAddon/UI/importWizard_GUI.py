# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importWizard_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import importlib

from PySide2 import QtCore, QtWidgets

from .AssetDetailsView import assetDetailsView
from .AssetListView import assetListView
from .PipelineViewerView import pipelineViewerView

importlib.reload(assetDetailsView)
importlib.reload(assetListView)
importlib.reload(pipelineViewerView)


class Ui_import_Wizard(object):
    def setupUi(self, import_Wizard):
        import_Wizard.setObjectName("import_Wizard")
        import_Wizard.resize(756, 367)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(import_Wizard)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(-1, 0, -1, -1)
        self.main_layout.setObjectName("main_layout")
        self.asset_list = assetListView.AssetListView(import_Wizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_list.sizePolicy().hasHeightForWidth())
        self.asset_list.setSizePolicy(sizePolicy)
        self.asset_list.setMinimumSize(QtCore.QSize(230, 0))
        self.asset_list.setObjectName("asset_list")
        self.main_layout.addWidget(self.asset_list)
        self.asset_details_pipeline_layout = QtWidgets.QVBoxLayout()
        self.asset_details_pipeline_layout.setContentsMargins(0, -1, -1, -1)
        self.asset_details_pipeline_layout.setObjectName("asset_details_pipeline_layout")
        self.asset_details = assetDetailsView.AssetDetailsView(import_Wizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_details.sizePolicy().hasHeightForWidth())
        self.asset_details.setSizePolicy(sizePolicy)
        self.asset_details.setMinimumSize(QtCore.QSize(0, 90))
        self.asset_details.setObjectName("asset_details")
        self.asset_details_pipeline_layout.addWidget(self.asset_details)
        self.pipeline_outputs_layout = QtWidgets.QHBoxLayout()
        self.pipeline_outputs_layout.setContentsMargins(-1, 0, 0, -1)
        self.pipeline_outputs_layout.setObjectName("pipeline_outputs_layout")
        self.pipeline_viewer = pipelineViewerView.PipelineViewerView(import_Wizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pipeline_viewer.sizePolicy().hasHeightForWidth())
        self.pipeline_viewer.setSizePolicy(sizePolicy)
        self.pipeline_viewer.setObjectName("pipeline_viewer")
        self.pipeline_outputs_layout.addWidget(self.pipeline_viewer)
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
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
        self.inputs_label.setText(_translate("import_Wizard", "Inputs"))
        self.import_button.setText(_translate("import_Wizard", "Import"))
        self.cancel_Button.setText(_translate("import_Wizard", "Cancel"))