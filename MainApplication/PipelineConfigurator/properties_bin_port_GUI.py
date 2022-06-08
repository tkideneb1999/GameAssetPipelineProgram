# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties_bin_port_GUI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Port(object):
    def setupUi(self, Port):
        if not Port.objectName():
            Port.setObjectName(u"Port")
        Port.resize(200, 66)
        self.verticalLayout = QVBoxLayout(Port)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.port_name_edit = QLineEdit(Port)
        self.port_name_edit.setObjectName(u"port_name_edit")

        self.verticalLayout.addWidget(self.port_name_edit)

        self.data_type_menu = QComboBox(Port)
        self.data_type_menu.setObjectName(u"data_type_menu")

        self.verticalLayout.addWidget(self.data_type_menu)


        self.retranslateUi(Port)

        QMetaObject.connectSlotsByName(Port)
    # setupUi

    def retranslateUi(self, Port):
        Port.setWindowTitle(QCoreApplication.translate("Port", u"Form", None))
    # retranslateUi

