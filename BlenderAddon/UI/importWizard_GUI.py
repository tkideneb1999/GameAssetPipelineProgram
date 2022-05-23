# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'importWizard_GUI.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from .AssetDetailsView.assetDetailsView import AssetDetailsView
from .AssetListView.assetListView import AssetListView
from .PipelineViewerView.pipelineViewerView import PipelineViewerView

class Ui_import_Wizard(object):
    def setupUi(self, import_Wizard):
        if not import_Wizard.objectName():
            import_Wizard.setObjectName(u"import_Wizard")
        import_Wizard.resize(756, 367)
        self.verticalLayout_2 = QVBoxLayout(import_Wizard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(-1, 0, -1, -1)
        self.asset_list = AssetListView(import_Wizard)
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
        self.asset_details = AssetDetailsView(import_Wizard)
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
        self.pipeline_viewer = PipelineViewerView(import_Wizard)
        self.pipeline_viewer.setObjectName(u"pipeline_viewer")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pipeline_viewer.sizePolicy().hasHeightForWidth())
        self.pipeline_viewer.setSizePolicy(sizePolicy2)

        self.pipeline_outputs_layout.addWidget(self.pipeline_viewer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.inputs_label = QLabel(import_Wizard)
        self.inputs_label.setObjectName(u"inputs_label")

        self.verticalLayout.addWidget(self.inputs_label)

        self.inputs_list = QListWidget(import_Wizard)
        self.inputs_list.setObjectName(u"inputs_list")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.inputs_list.sizePolicy().hasHeightForWidth())
        self.inputs_list.setSizePolicy(sizePolicy3)
        self.inputs_list.setMaximumSize(QSize(100, 16777215))
        self.inputs_list.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout.addWidget(self.inputs_list)


        self.pipeline_outputs_layout.addLayout(self.verticalLayout)


        self.asset_details_pipeline_layout.addLayout(self.pipeline_outputs_layout)


        self.main_layout.addLayout(self.asset_details_pipeline_layout)


        self.verticalLayout_2.addLayout(self.main_layout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.import_button = QPushButton(import_Wizard)
        self.import_button.setObjectName(u"import_button")

        self.horizontalLayout_4.addWidget(self.import_button)

        self.cancel_Button = QPushButton(import_Wizard)
        self.cancel_Button.setObjectName(u"cancel_Button")

        self.horizontalLayout_4.addWidget(self.cancel_Button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(import_Wizard)
        self.cancel_Button.clicked.connect(import_Wizard.reject)

        QMetaObject.connectSlotsByName(import_Wizard)
    # setupUi

    def retranslateUi(self, import_Wizard):
        import_Wizard.setWindowTitle(QCoreApplication.translate("import_Wizard", u"Dialog", None))
        self.inputs_label.setText(QCoreApplication.translate("import_Wizard", u"Inputs", None))
        self.import_button.setText(QCoreApplication.translate("import_Wizard", u"Import", None))
        self.cancel_Button.setText(QCoreApplication.translate("import_Wizard", u"Cancel", None))
    # retranslateUi

