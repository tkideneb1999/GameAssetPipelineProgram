# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties_bin_port_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from ..Common.qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from ..Common.qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from ..Common.qtpy.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Port(object):
    def setupUi(self, Port):
        if not Port.objectName():
            Port.setObjectName(u"Port")
        Port.resize(204, 65)
        self.verticalLayout = QVBoxLayout(Port)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.port_name_edit = QLineEdit(Port)
        self.port_name_edit.setObjectName(u"port_name_edit")
        self.port_name_edit.setEnabled(True)

        self.verticalLayout.addWidget(self.port_name_edit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.data_type_menu = QComboBox(Port)
        self.data_type_menu.setObjectName(u"data_type_menu")
        self.data_type_menu.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_type_menu.sizePolicy().hasHeightForWidth())
        self.data_type_menu.setSizePolicy(sizePolicy)
        self.data_type_menu.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.data_type_menu)

        self.remove_port_button = QPushButton(Port)
        self.remove_port_button.setObjectName(u"remove_port_button")
        self.remove_port_button.setMinimumSize(QSize(20, 0))

        self.horizontalLayout.addWidget(self.remove_port_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Port)

        QMetaObject.connectSlotsByName(Port)
    # setupUi

    def retranslateUi(self, Port):
        Port.setWindowTitle(QCoreApplication.translate("Port", u"Form", None))
        self.remove_port_button.setText(QCoreApplication.translate("Port", u"-", None))
    # retranslateUi

