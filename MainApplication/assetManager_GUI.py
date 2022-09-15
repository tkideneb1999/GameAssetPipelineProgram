# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assetManager_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QMetaObject, QSize)
from qtpy.QtGui import (QFont)
from qtpy.QtWidgets import (QHBoxLayout, QLabel, QPushButton,
                               QSizePolicy, QVBoxLayout)

from .Common.AssetDetailsView.assetDetailsView import AssetDetailsView
from .Common.AssetListView.assetListView import AssetListView
from .Common.PipelineViewerView.pipelineViewerView import PipelineViewerView

class Ui_asset_manager(object):
    def setupUi(self, asset_manager):
        if not asset_manager.objectName():
            asset_manager.setObjectName(u"asset_manager")
        asset_manager.resize(1035, 543)
        self.horizontalLayout = QHBoxLayout(asset_manager)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.asset_list = AssetListView(asset_manager)
        self.asset_list.setObjectName(u"asset_list")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_list.sizePolicy().hasHeightForWidth())
        self.asset_list.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.asset_list)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.add_asset_button = QPushButton(asset_manager)
        self.add_asset_button.setObjectName(u"add_asset_button")
        self.add_asset_button.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_2.addWidget(self.add_asset_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.asset_details_label = QLabel(asset_manager)
        self.asset_details_label.setObjectName(u"asset_details_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.asset_details_label.sizePolicy().hasHeightForWidth())
        self.asset_details_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        self.asset_details_label.setFont(font)

        self.verticalLayout_2.addWidget(self.asset_details_label)

        self.asset_details = AssetDetailsView(asset_manager)
        self.asset_details.setObjectName(u"asset_details")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.asset_details.sizePolicy().hasHeightForWidth())
        self.asset_details.setSizePolicy(sizePolicy2)
        self.asset_details.setMinimumSize(QSize(0, 90))

        self.verticalLayout_2.addWidget(self.asset_details)

        self.pipeline_viewer = PipelineViewerView(asset_manager)
        self.pipeline_viewer.setObjectName(u"pipeline_viewer")

        self.verticalLayout_2.addWidget(self.pipeline_viewer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(asset_manager)

        QMetaObject.connectSlotsByName(asset_manager)
    # setupUi

    def retranslateUi(self, asset_manager):
        asset_manager.setWindowTitle(QCoreApplication.translate("asset_manager", u"Form", None))
        self.add_asset_button.setText(QCoreApplication.translate("asset_manager", u"Add Asset", None))
        self.asset_details_label.setText(QCoreApplication.translate("asset_manager", u"Details", None))
    # retranslateUi

