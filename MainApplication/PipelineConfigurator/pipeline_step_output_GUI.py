# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipeline_step_output_GUI.ui'
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
from ..Common.qtpy.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_pipeline_step_output(object):
    def setupUi(self, pipeline_step_output):
        if not pipeline_step_output.objectName():
            pipeline_step_output.setObjectName(u"pipeline_step_output")
        pipeline_step_output.resize(200, 73)
        self.horizontalLayout = QHBoxLayout(pipeline_step_output)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 2, 4, 2)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.id_d_label = QLabel(pipeline_step_output)
        self.id_d_label.setObjectName(u"id_d_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_d_label.sizePolicy().hasHeightForWidth())
        self.id_d_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.id_d_label)

        self.id_label = QLabel(pipeline_step_output)
        self.id_label.setObjectName(u"id_label")

        self.horizontalLayout_2.addWidget(self.id_label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.output_type_combobox = QComboBox(pipeline_step_output)
        self.output_type_combobox.setObjectName(u"output_type_combobox")
        self.output_type_combobox.setMinimumSize(QSize(150, 0))

        self.verticalLayout.addWidget(self.output_type_combobox)

        self.output_name_lineedit = QLineEdit(pipeline_step_output)
        self.output_name_lineedit.setObjectName(u"output_name_lineedit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.output_name_lineedit.sizePolicy().hasHeightForWidth())
        self.output_name_lineedit.setSizePolicy(sizePolicy1)
        self.output_name_lineedit.setMinimumSize(QSize(150, 0))

        self.verticalLayout.addWidget(self.output_name_lineedit)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.remove_output_button = QPushButton(pipeline_step_output)
        self.remove_output_button.setObjectName(u"remove_output_button")
        self.remove_output_button.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout.addWidget(self.remove_output_button)


        self.retranslateUi(pipeline_step_output)

        QMetaObject.connectSlotsByName(pipeline_step_output)
    # setupUi

    def retranslateUi(self, pipeline_step_output):
        pipeline_step_output.setWindowTitle(QCoreApplication.translate("pipeline_step_output", u"Form", None))
        self.id_d_label.setText(QCoreApplication.translate("pipeline_step_output", u"uid:", None))
        self.id_label.setText(QCoreApplication.translate("pipeline_step_output", u"id", None))
        self.remove_output_button.setText(QCoreApplication.translate("pipeline_step_output", u"-", None))
    # retranslateUi

