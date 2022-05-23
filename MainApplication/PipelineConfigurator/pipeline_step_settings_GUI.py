# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipeline_step_settings_GUI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_pipeline_step_settings_GUI(object):
    def setupUi(self, pipeline_step_settings_GUI):
        if not pipeline_step_settings_GUI.objectName():
            pipeline_step_settings_GUI.setObjectName(u"pipeline_step_settings_GUI")
        pipeline_step_settings_GUI.resize(400, 21)
        self.verticalLayout = QVBoxLayout(pipeline_step_settings_GUI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.configs_layout = QHBoxLayout()
        self.configs_layout.setObjectName(u"configs_layout")
        self.configs_layout.setContentsMargins(-1, 0, -1, -1)
        self.label = QLabel(pipeline_step_settings_GUI)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.configs_layout.addWidget(self.label)

        self.configs_combobox = QComboBox(pipeline_step_settings_GUI)
        self.configs_combobox.setObjectName(u"configs_combobox")

        self.configs_layout.addWidget(self.configs_combobox)


        self.verticalLayout.addLayout(self.configs_layout)


        self.retranslateUi(pipeline_step_settings_GUI)

        QMetaObject.connectSlotsByName(pipeline_step_settings_GUI)
    # setupUi

    def retranslateUi(self, pipeline_step_settings_GUI):
        pipeline_step_settings_GUI.setWindowTitle(QCoreApplication.translate("pipeline_step_settings_GUI", u"Form", None))
        self.label.setText(QCoreApplication.translate("pipeline_step_settings_GUI", u"Config", None))
    # retranslateUi

