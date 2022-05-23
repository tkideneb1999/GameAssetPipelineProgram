# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_item_GUI.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_plugin_item(object):
    def setupUi(self, plugin_item):
        if not plugin_item.objectName():
            plugin_item.setObjectName(u"plugin_item")
        plugin_item.resize(400, 23)
        self.horizontalLayout = QHBoxLayout(plugin_item)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.name_label = QLabel(plugin_item)
        self.name_label.setObjectName(u"name_label")

        self.horizontalLayout.addWidget(self.name_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.settings_button = QPushButton(plugin_item)
        self.settings_button.setObjectName(u"settings_button")

        self.horizontalLayout.addWidget(self.settings_button)


        self.retranslateUi(plugin_item)

        QMetaObject.connectSlotsByName(plugin_item)
    # setupUi

    def retranslateUi(self, plugin_item):
        plugin_item.setWindowTitle(QCoreApplication.translate("plugin_item", u"Form", None))
        self.name_label.setText(QCoreApplication.translate("plugin_item", u"Plugin Name", None))
        self.settings_button.setText(QCoreApplication.translate("plugin_item", u"Settings", None))
    # retranslateUi

