# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assetList_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                                                QMetaObject, QObject, QPoint, QRect,
                                                QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                                               QFont, QFontDatabase, QGradient, QIcon,
                                               QImage, QKeySequence, QLinearGradient, QPainter,
                                               QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
                                                   QLabel, QLineEdit, QSizePolicy, QTreeWidget,
                                                   QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_asset_list_widget(object):
    def setupUi(self, asset_list_widget):
        if not asset_list_widget.objectName():
            asset_list_widget.setObjectName(u"asset_list_widget")
        asset_list_widget.resize(230, 452)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(asset_list_widget.sizePolicy().hasHeightForWidth())
        asset_list_widget.setSizePolicy(sizePolicy)
        asset_list_widget.setMinimumSize(QSize(230, 0))
        asset_list_widget.setMaximumSize(QSize(230, 16777215))
        self.verticalLayout = QVBoxLayout(asset_list_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.assets_label = QLabel(asset_list_widget)
        self.assets_label.setObjectName(u"assets_label")
        font = QFont()
        font.setPointSize(12)
        self.assets_label.setFont(font)

        self.verticalLayout.addWidget(self.assets_label)

        self.search_bar = QLineEdit(asset_list_widget)
        self.search_bar.setObjectName(u"search_bar")
        self.search_bar.setEnabled(False)

        self.verticalLayout.addWidget(self.search_bar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.checkBox = QCheckBox(asset_list_widget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setEnabled(False)

        self.horizontalLayout.addWidget(self.checkBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.asset_tree = QTreeWidget(asset_list_widget)
        self.asset_tree.setObjectName(u"asset_tree")
        self.asset_tree.setAlternatingRowColors(False)
        self.asset_tree.setIndentation(20)
        self.asset_tree.setRootIsDecorated(True)
        self.asset_tree.setUniformRowHeights(False)
        self.asset_tree.setAnimated(False)
        self.asset_tree.header().setVisible(False)
        self.asset_tree.header().setCascadingSectionResizes(False)
        self.asset_tree.header().setProperty("showSortIndicator", False)
        self.asset_tree.header().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.asset_tree)


        self.retranslateUi(asset_list_widget)

        QMetaObject.connectSlotsByName(asset_list_widget)
    # setupUi

    def retranslateUi(self, asset_list_widget):
        asset_list_widget.setWindowTitle(QCoreApplication.translate("asset_list_widget", u"Form", None))
        self.assets_label.setText(QCoreApplication.translate("asset_list_widget", u"Assets", None))
        self.search_bar.setText(QCoreApplication.translate("asset_list_widget", u"not available", None))
        self.checkBox.setText(QCoreApplication.translate("asset_list_widget", u"Tag Search (not available)", None))
        ___qtreewidgetitem = self.asset_tree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("asset_list_widget", u"1", None));
    # retranslateUi

