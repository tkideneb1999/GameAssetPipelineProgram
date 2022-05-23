# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'projectWizard_GUI.ui'
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
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_project_wizard(object):
    def setupUi(self, project_wizard):
        if not project_wizard.objectName():
            project_wizard.setObjectName(u"project_wizard")
        project_wizard.resize(533, 303)
        self.verticalLayout = QVBoxLayout(project_wizard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(project_wizard)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(90, 0))

        self.horizontalLayout.addWidget(self.label)

        self.project_name_line_edit = QLineEdit(project_wizard)
        self.project_name_line_edit.setObjectName(u"project_name_line_edit")

        self.horizontalLayout.addWidget(self.project_name_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 9, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.project_dir_label = QLabel(project_wizard)
        self.project_dir_label.setObjectName(u"project_dir_label")
        sizePolicy.setHeightForWidth(self.project_dir_label.sizePolicy().hasHeightForWidth())
        self.project_dir_label.setSizePolicy(sizePolicy)
        self.project_dir_label.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_2.addWidget(self.project_dir_label)

        self.project_dir_line_edit = QLineEdit(project_wizard)
        self.project_dir_line_edit.setObjectName(u"project_dir_line_edit")

        self.horizontalLayout_2.addWidget(self.project_dir_line_edit)

        self.file_dialog_button = QPushButton(project_wizard)
        self.file_dialog_button.setObjectName(u"file_dialog_button")
        self.file_dialog_button.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.file_dialog_button.sizePolicy().hasHeightForWidth())
        self.file_dialog_button.setSizePolicy(sizePolicy1)
        self.file_dialog_button.setMinimumSize(QSize(30, 0))
        self.file_dialog_button.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_2.addWidget(self.file_dialog_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.project_dir_d_label = QLabel(project_wizard)
        self.project_dir_d_label.setObjectName(u"project_dir_d_label")
        self.project_dir_d_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.project_dir_d_label)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 6, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.levels_label = QLabel(project_wizard)
        self.levels_label.setObjectName(u"levels_label")
        sizePolicy.setHeightForWidth(self.levels_label.sizePolicy().hasHeightForWidth())
        self.levels_label.setSizePolicy(sizePolicy)
        self.levels_label.setMinimumSize(QSize(90, 0))

        self.verticalLayout_6.addWidget(self.levels_label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.level_list = QListWidget(project_wizard)
        self.level_list.setObjectName(u"level_list")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.level_list.sizePolicy().hasHeightForWidth())
        self.level_list.setSizePolicy(sizePolicy2)
        self.level_list.setContextMenuPolicy(Qt.NoContextMenu)
        self.level_list.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.level_list.setFlow(QListView.TopToBottom)

        self.horizontalLayout_3.addWidget(self.level_list)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.levels_d_label = QLabel(project_wizard)
        self.levels_d_label.setObjectName(u"levels_d_label")
        self.levels_d_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.levels_d_label)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.open_project_button = QPushButton(project_wizard)
        self.open_project_button.setObjectName(u"open_project_button")

        self.horizontalLayout_4.addWidget(self.open_project_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.okay_button = QPushButton(project_wizard)
        self.okay_button.setObjectName(u"okay_button")
        self.okay_button.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.okay_button)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(project_wizard)
        self.okay_button.clicked.connect(project_wizard.accept)

        QMetaObject.connectSlotsByName(project_wizard)
    # setupUi

    def retranslateUi(self, project_wizard):
        project_wizard.setWindowTitle(QCoreApplication.translate("project_wizard", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("project_wizard", u"Project Name", None))
        self.project_dir_label.setText(QCoreApplication.translate("project_wizard", u"Project Directory", None))
        self.project_dir_line_edit.setInputMask("")
        self.file_dialog_button.setText(QCoreApplication.translate("project_wizard", u"...", None))
        self.project_dir_d_label.setText(QCoreApplication.translate("project_wizard", u"Select the folder in which the projects root folder will be placed.", None))
        self.levels_label.setText(QCoreApplication.translate("project_wizard", u"Levels", None))
        self.levels_d_label.setText(QCoreApplication.translate("project_wizard", u"The right-click menu on the list enables adding adn removing levels.", None))
        self.open_project_button.setText(QCoreApplication.translate("project_wizard", u"Open Previous...", None))
        self.okay_button.setText(QCoreApplication.translate("project_wizard", u"Create Project", None))
    # retranslateUi

