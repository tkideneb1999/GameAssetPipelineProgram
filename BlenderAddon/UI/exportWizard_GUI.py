# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exportWizard_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from .AssetDetailsView.assetDetailsView import AssetDetailsView
from .AssetListView.assetListView import AssetListView
from .PipelineViewerView.pipelineViewerView import PipelineViewerView

class Ui_export_Wizard(object):
    def setupUi(self, export_Wizard):
        if not export_Wizard.objectName():
            export_Wizard.setObjectName(u"export_Wizard")
        export_Wizard.resize(758, 367)
        self.verticalLayout_2 = QVBoxLayout(export_Wizard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(-1, 0, -1, -1)
        self.asset_list = AssetListView(export_Wizard)
        self.asset_list.setObjectName(u"asset_list")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_list.sizePolicy().hasHeightForWidth())
        self.asset_list.setSizePolicy(sizePolicy)
        self.asset_list.setMinimumSize(QSize(230, 0))

        self.main_layout.addWidget(self.asset_list)

        self.asset_details_pipeline_layout = QVBoxLayout()
        self.asset_details_pipeline_layout.setObjectName(u"asset_details_pipeline_layout")
        self.asset_details_pipeline_layout.setContentsMargins(0, -1, -1, -1)
        self.asset_details = AssetDetailsView(export_Wizard)
        self.asset_details.setObjectName(u"asset_details")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.asset_details.sizePolicy().hasHeightForWidth())
        self.asset_details.setSizePolicy(sizePolicy1)
        self.asset_details.setMinimumSize(QSize(0, 90))

        self.asset_details_pipeline_layout.addWidget(self.asset_details)

        self.pipeline_outputs_layout = QHBoxLayout()
        self.pipeline_outputs_layout.setObjectName(u"pipeline_outputs_layout")
        self.pipeline_outputs_layout.setContentsMargins(-1, 0, 0, -1)
        self.pipeline_viewer = PipelineViewerView(export_Wizard)
        self.pipeline_viewer.setObjectName(u"pipeline_viewer")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pipeline_viewer.sizePolicy().hasHeightForWidth())
        self.pipeline_viewer.setSizePolicy(sizePolicy2)

        self.pipeline_outputs_layout.addWidget(self.pipeline_viewer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.outputs_label = QLabel(export_Wizard)
        self.outputs_label.setObjectName(u"outputs_label")

        self.verticalLayout.addWidget(self.outputs_label)

        self.outputs_list = QListWidget(export_Wizard)
        self.outputs_list.setObjectName(u"outputs_list")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.outputs_list.sizePolicy().hasHeightForWidth())
        self.outputs_list.setSizePolicy(sizePolicy3)
        self.outputs_list.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout.addWidget(self.outputs_list)

        self.export_selected_checkbox = QCheckBox(export_Wizard)
        self.export_selected_checkbox.setObjectName(u"export_selected_checkbox")

        self.verticalLayout.addWidget(self.export_selected_checkbox)

        self.file_format_label = QLabel(export_Wizard)
        self.file_format_label.setObjectName(u"file_format_label")

        self.verticalLayout.addWidget(self.file_format_label)

        self.file_format_combobox = QComboBox(export_Wizard)
        self.file_format_combobox.setObjectName(u"file_format_combobox")

        self.verticalLayout.addWidget(self.file_format_combobox)


        self.pipeline_outputs_layout.addLayout(self.verticalLayout)


        self.asset_details_pipeline_layout.addLayout(self.pipeline_outputs_layout)


        self.main_layout.addLayout(self.asset_details_pipeline_layout)


        self.verticalLayout_2.addLayout(self.main_layout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.publish_button = QPushButton(export_Wizard)
        self.publish_button.setObjectName(u"publish_button")

        self.horizontalLayout_4.addWidget(self.publish_button)

        self.cancel_Button = QPushButton(export_Wizard)
        self.cancel_Button.setObjectName(u"cancel_Button")

        self.horizontalLayout_4.addWidget(self.cancel_Button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(export_Wizard)
        self.cancel_Button.clicked.connect(export_Wizard.reject)

        QMetaObject.connectSlotsByName(export_Wizard)
    # setupUi

    def retranslateUi(self, export_Wizard):
        export_Wizard.setWindowTitle(QCoreApplication.translate("export_Wizard", u"Dialog", None))
        self.outputs_label.setText(QCoreApplication.translate("export_Wizard", u"Outputs", None))
        self.export_selected_checkbox.setText(QCoreApplication.translate("export_Wizard", u"Export Selected", None))
        self.file_format_label.setText(QCoreApplication.translate("export_Wizard", u"File Format", None))
        self.publish_button.setText(QCoreApplication.translate("export_Wizard", u"Publish", None))
        self.cancel_Button.setText(QCoreApplication.translate("export_Wizard", u"Cancel", None))
    # retranslateUi

