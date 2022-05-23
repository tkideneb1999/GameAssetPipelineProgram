# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipeline_step_input_GUI.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_pipeline_step_input(object):
    def setupUi(self, pipeline_step_input):
        if not pipeline_step_input.objectName():
            pipeline_step_input.setObjectName(u"pipeline_step_input")
        pipeline_step_input.resize(200, 77)
        self.horizontalLayout = QHBoxLayout(pipeline_step_input)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.id_d_label = QLabel(pipeline_step_input)
        self.id_d_label.setObjectName(u"id_d_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_d_label.sizePolicy().hasHeightForWidth())
        self.id_d_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.id_d_label)

        self.id_label = QLabel(pipeline_step_input)
        self.id_label.setObjectName(u"id_label")

        self.horizontalLayout_2.addWidget(self.id_label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.input_type_combo_box = QComboBox(pipeline_step_input)
        self.input_type_combo_box.setObjectName(u"input_type_combo_box")
        self.input_type_combo_box.setMinimumSize(QSize(150, 0))

        self.verticalLayout.addWidget(self.input_type_combo_box)

        self.input_name_combobox = QComboBox(pipeline_step_input)
        self.input_name_combobox.setObjectName(u"input_name_combobox")
        self.input_name_combobox.setMinimumSize(QSize(150, 0))

        self.verticalLayout.addWidget(self.input_name_combobox)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.remove_input_button = QPushButton(pipeline_step_input)
        self.remove_input_button.setObjectName(u"remove_input_button")
        self.remove_input_button.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout.addWidget(self.remove_input_button)


        self.retranslateUi(pipeline_step_input)

        QMetaObject.connectSlotsByName(pipeline_step_input)
    # setupUi

    def retranslateUi(self, pipeline_step_input):
        pipeline_step_input.setWindowTitle(QCoreApplication.translate("pipeline_step_input", u"Form", None))
        self.id_d_label.setText(QCoreApplication.translate("pipeline_step_input", u"uid:", None))
        self.id_label.setText(QCoreApplication.translate("pipeline_step_input", u"id", None))
        self.remove_input_button.setText(QCoreApplication.translate("pipeline_step_input", u"-", None))
    # retranslateUi

