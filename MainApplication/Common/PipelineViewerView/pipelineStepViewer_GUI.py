# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipelineStepViewer_GUI.ui'
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
from qtpy.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
                                                   QSpacerItem, QVBoxLayout, QWidget)

class Ui_pipeline_step_viewer(object):
    def setupUi(self, pipeline_step_viewer):
        if not pipeline_step_viewer.objectName():
            pipeline_step_viewer.setObjectName(u"pipeline_step_viewer")
        pipeline_step_viewer.resize(326, 300)
        pipeline_step_viewer.setFocusPolicy(Qt.StrongFocus)
        pipeline_step_viewer.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(pipeline_step_viewer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(pipeline_step_viewer)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(2)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.name_label = QLabel(self.frame)
        self.name_label.setObjectName(u"name_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.name_label)

        self.program_label = QLabel(self.frame)
        self.program_label.setObjectName(u"program_label")
        sizePolicy.setHeightForWidth(self.program_label.sizePolicy().hasHeightForWidth())
        self.program_label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.program_label)

        self.state_label = QLabel(self.frame)
        self.state_label.setObjectName(u"state_label")
        sizePolicy.setHeightForWidth(self.state_label.sizePolicy().hasHeightForWidth())
        self.state_label.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.state_label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(pipeline_step_viewer)

        QMetaObject.connectSlotsByName(pipeline_step_viewer)
    # setupUi

    def retranslateUi(self, pipeline_step_viewer):
        pipeline_step_viewer.setWindowTitle(QCoreApplication.translate("pipeline_step_viewer", u"Form", None))
        self.name_label.setText(QCoreApplication.translate("pipeline_step_viewer", u"Step Name", None))
        self.program_label.setText(QCoreApplication.translate("pipeline_step_viewer", u"Program", None))
        self.state_label.setText(QCoreApplication.translate("pipeline_step_viewer", u"State", None))
    # retranslateUi

