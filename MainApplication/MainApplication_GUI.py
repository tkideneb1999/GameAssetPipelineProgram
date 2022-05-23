# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainApplication_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1041, 600)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1041, 600))
        self.actionSet_as_current_project = QAction(MainWindow)
        self.actionSet_as_current_project.setObjectName(u"actionSet_as_current_project")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setAutoFillBackground(False)
        self.assets_tab = QWidget()
        self.assets_tab.setObjectName(u"assets_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.assets_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, -1, -1, -1)
        self.tabs.addTab(self.assets_tab, "")
        self.pipelines_tab = QWidget()
        self.pipelines_tab.setObjectName(u"pipelines_tab")
        self.pipelines_tab.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.pipelines_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabs.addTab(self.pipelines_tab, "")
        self.settings_tab = QWidget()
        self.settings_tab.setObjectName(u"settings_tab")
        self.verticalLayout_2 = QVBoxLayout(self.settings_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabs.addTab(self.settings_tab, "")
        self.project_settings_tab = QWidget()
        self.project_settings_tab.setObjectName(u"project_settings_tab")
        self.verticalLayout_5 = QVBoxLayout(self.project_settings_tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabs.addTab(self.project_settings_tab, "")

        self.verticalLayout.addWidget(self.tabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1041, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionSet_as_current_project)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSet_as_current_project.setText(QCoreApplication.translate("MainWindow", u"Set as current project", None))
        self.tabs.setTabText(self.tabs.indexOf(self.assets_tab), QCoreApplication.translate("MainWindow", u"Assets", None))
        self.tabs.setTabText(self.tabs.indexOf(self.pipelines_tab), QCoreApplication.translate("MainWindow", u"Pipeline Configurator", None))
        self.tabs.setTabText(self.tabs.indexOf(self.settings_tab), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tabs.setTabText(self.tabs.indexOf(self.project_settings_tab), QCoreApplication.translate("MainWindow", u"Project Settings", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

