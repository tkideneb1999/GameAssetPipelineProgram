# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipeline_step_GUI.ui'
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
from qtpy.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from .pipelineStepSettingsView import PipelineStepSettingsView

class Ui_pipeline_step(object):
    def setupUi(self, pipeline_step):
        if not pipeline_step.objectName():
            pipeline_step.setObjectName(u"pipeline_step")
        pipeline_step.resize(450, 208)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pipeline_step.sizePolicy().hasHeightForWidth())
        pipeline_step.setSizePolicy(sizePolicy)
        pipeline_step.setMinimumSize(QSize(450, 110))
        self.horizontalLayout_2 = QHBoxLayout(pipeline_step)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(3, 0, 3, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.pipeline_step_name_label = QLabel(pipeline_step)
        self.pipeline_step_name_label.setObjectName(u"pipeline_step_name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pipeline_step_name_label.sizePolicy().hasHeightForWidth())
        self.pipeline_step_name_label.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.pipeline_step_name_label)

        self.pipeline_step_name_lineedit = QLineEdit(pipeline_step)
        self.pipeline_step_name_lineedit.setObjectName(u"pipeline_step_name_lineedit")

        self.verticalLayout.addWidget(self.pipeline_step_name_lineedit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.program_label = QLabel(pipeline_step)
        self.program_label.setObjectName(u"program_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.program_label.sizePolicy().hasHeightForWidth())
        self.program_label.setSizePolicy(sizePolicy2)
        self.program_label.setMinimumSize(QSize(60, 20))
        self.program_label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(10)
        self.program_label.setFont(font)
        self.program_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.program_label)

        self.program_combobox = QComboBox(pipeline_step)
        self.program_combobox.setObjectName(u"program_combobox")

        self.horizontalLayout_3.addWidget(self.program_combobox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.program_settings = PipelineStepSettingsView(pipeline_step)
        self.program_settings.setObjectName(u"program_settings")
        self.program_settings.setMinimumSize(QSize(0, 10))

        self.verticalLayout.addWidget(self.program_settings)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.inputs_layout = QVBoxLayout()
        self.inputs_layout.setObjectName(u"inputs_layout")
        self.inputs_layout.setContentsMargins(0, -1, -1, -1)
        self.inputs_label = QLabel(pipeline_step)
        self.inputs_label.setObjectName(u"inputs_label")
        sizePolicy1.setHeightForWidth(self.inputs_label.sizePolicy().hasHeightForWidth())
        self.inputs_label.setSizePolicy(sizePolicy1)

        self.inputs_layout.addWidget(self.inputs_label)

        self.add_input_button = QPushButton(pipeline_step)
        self.add_input_button.setObjectName(u"add_input_button")
        self.add_input_button.setMinimumSize(QSize(100, 20))
        self.add_input_button.setMaximumSize(QSize(16777215, 20))

        self.inputs_layout.addWidget(self.add_input_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.inputs_layout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.inputs_layout)

        self.line = QFrame(pipeline_step)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.VLine)

        self.horizontalLayout.addWidget(self.line)

        self.outputs_layout = QVBoxLayout()
        self.outputs_layout.setObjectName(u"outputs_layout")
        self.outputs_layout.setContentsMargins(0, -1, -1, -1)
        self.outputs_label = QLabel(pipeline_step)
        self.outputs_label.setObjectName(u"outputs_label")
        sizePolicy1.setHeightForWidth(self.outputs_label.sizePolicy().hasHeightForWidth())
        self.outputs_label.setSizePolicy(sizePolicy1)
        self.outputs_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.outputs_layout.addWidget(self.outputs_label)

        self.add_output_button = QPushButton(pipeline_step)
        self.add_output_button.setObjectName(u"add_output_button")
        self.add_output_button.setMinimumSize(QSize(100, 20))
        self.add_output_button.setMaximumSize(QSize(16777215, 20))

        self.outputs_layout.addWidget(self.add_output_button)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.outputs_layout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.outputs_layout)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_2 = QFrame(pipeline_step)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setFrameShape(QFrame.VLine)

        self.horizontalLayout_2.addWidget(self.line_2)


        self.retranslateUi(pipeline_step)

        QMetaObject.connectSlotsByName(pipeline_step)
    # setupUi

    def retranslateUi(self, pipeline_step):
        pipeline_step.setWindowTitle(QCoreApplication.translate("pipeline_step", u"Form", None))
        self.pipeline_step_name_label.setText(QCoreApplication.translate("pipeline_step", u"Pipeline Step Name", None))
        self.program_label.setText(QCoreApplication.translate("pipeline_step", u"Program", None))
        self.inputs_label.setText(QCoreApplication.translate("pipeline_step", u"Inputs", None))
        self.add_input_button.setText(QCoreApplication.translate("pipeline_step", u"+", None))
        self.outputs_label.setText(QCoreApplication.translate("pipeline_step", u"Outputs", None))
        self.add_output_button.setText(QCoreApplication.translate("pipeline_step", u"+", None))
    # retranslateUi

