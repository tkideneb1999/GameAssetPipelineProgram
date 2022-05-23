# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_GUI.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

class Ui_settings(object):
    def setupUi(self, settings):
        if not settings.objectName():
            settings.setObjectName(u"settings")
        settings.resize(494, 318)
        self.verticalLayout = QVBoxLayout(settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.programs_label = QLabel(settings)
        self.programs_label.setObjectName(u"programs_label")

        self.verticalLayout.addWidget(self.programs_label)

        self.programs_list = QListWidget(settings)
        self.programs_list.setObjectName(u"programs_list")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.programs_list.sizePolicy().hasHeightForWidth())
        self.programs_list.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.programs_list)

        self.plugins_label = QLabel(settings)
        self.plugins_label.setObjectName(u"plugins_label")

        self.verticalLayout.addWidget(self.plugins_label)

        self.plugins_scrollbar = QScrollArea(settings)
        self.plugins_scrollbar.setObjectName(u"plugins_scrollbar")
        sizePolicy.setHeightForWidth(self.plugins_scrollbar.sizePolicy().hasHeightForWidth())
        self.plugins_scrollbar.setSizePolicy(sizePolicy)
        self.plugins_scrollbar.setMinimumSize(QSize(0, 130))
        self.plugins_scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.plugins_scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plugins_scrollbar.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 461, 128))
        self.plugins_scrollbar.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.plugins_scrollbar)


        self.retranslateUi(settings)

        QMetaObject.connectSlotsByName(settings)
    # setupUi

    def retranslateUi(self, settings):
        settings.setWindowTitle(QCoreApplication.translate("settings", u"Form", None))
        self.programs_label.setText(QCoreApplication.translate("settings", u"Programs", None))
        self.plugins_label.setText(QCoreApplication.translate("settings", u"Plugins", None))
    # retranslateUi

