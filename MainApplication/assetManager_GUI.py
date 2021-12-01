# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assetManager_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_asset_manager(object):
    def setupUi(self, asset_manager):
        asset_manager.setObjectName("asset_manager")
        asset_manager.resize(1035, 543)
        self.horizontalLayout = QtWidgets.QHBoxLayout(asset_manager)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.asset_list = AssetListView(asset_manager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_list.sizePolicy().hasHeightForWidth())
        self.asset_list.setSizePolicy(sizePolicy)
        self.asset_list.setObjectName("asset_list")
        self.verticalLayout.addWidget(self.asset_list)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_asset_button = QtWidgets.QPushButton(asset_manager)
        self.add_asset_button.setObjectName("add_asset_button")
        self.horizontalLayout_2.addWidget(self.add_asset_button)
        self.remove_asset_button = QtWidgets.QPushButton(asset_manager)
        self.remove_asset_button.setObjectName("remove_asset_button")
        self.horizontalLayout_2.addWidget(self.remove_asset_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.asset_details_label = QtWidgets.QLabel(asset_manager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_details_label.sizePolicy().hasHeightForWidth())
        self.asset_details_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.asset_details_label.setFont(font)
        self.asset_details_label.setObjectName("asset_details_label")
        self.verticalLayout_2.addWidget(self.asset_details_label)
        self.asset_details = AssetDetailsView(asset_manager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_details.sizePolicy().hasHeightForWidth())
        self.asset_details.setSizePolicy(sizePolicy)
        self.asset_details.setMinimumSize(QtCore.QSize(0, 90))
        self.asset_details.setObjectName("asset_details")
        self.verticalLayout_2.addWidget(self.asset_details)
        self.pipeline_viewer = PipelineViewerView(asset_manager)
        self.pipeline_viewer.setObjectName("pipeline_viewer")
        self.verticalLayout_2.addWidget(self.pipeline_viewer)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(asset_manager)
        QtCore.QMetaObject.connectSlotsByName(asset_manager)

    def retranslateUi(self, asset_manager):
        _translate = QtCore.QCoreApplication.translate
        asset_manager.setWindowTitle(_translate("asset_manager", "Form"))
        self.add_asset_button.setText(_translate("asset_manager", "Add"))
        self.remove_asset_button.setText(_translate("asset_manager", "Remove"))
        self.asset_details_label.setText(_translate("asset_manager", "Details"))
from .AssetDetailsView.assetDetailsView import AssetDetailsView
from .AssetListView.assetListView import AssetListView
from .PipelineViewerView.pipelineViewerView import PipelineViewerView
