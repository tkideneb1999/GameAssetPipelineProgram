# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tagDatabase_GUI.ui'
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
from ..Common.qtpy.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_tagDatabase(object):
    def setupUi(self, tagDatabase):
        if not tagDatabase.objectName():
            tagDatabase.setObjectName(u"tagDatabase")
        tagDatabase.resize(478, 300)
        self.horizontalLayout_2 = QHBoxLayout(tagDatabase)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tag_list = QListWidget(tagDatabase)
        self.tag_list.setObjectName(u"tag_list")

        self.horizontalLayout_2.addWidget(self.tag_list)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.add_tag_button = QPushButton(tagDatabase)
        self.add_tag_button.setObjectName(u"add_tag_button")

        self.verticalLayout.addWidget(self.add_tag_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.retranslateUi(tagDatabase)

        QMetaObject.connectSlotsByName(tagDatabase)
    # setupUi

    def retranslateUi(self, tagDatabase):
        tagDatabase.setWindowTitle(QCoreApplication.translate("tagDatabase", u"Form", None))
        self.add_tag_button.setText(QCoreApplication.translate("tagDatabase", u"Add Tag", None))
    # retranslateUi

