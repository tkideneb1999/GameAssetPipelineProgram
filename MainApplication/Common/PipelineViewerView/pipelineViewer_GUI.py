# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipelineViewer_GUI.ui'
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
from qtpy.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
                                                   QVBoxLayout, QWidget)

class Ui_pipeline_viewer(object):
    def setupUi(self, pipeline_viewer):
        if not pipeline_viewer.objectName():
            pipeline_viewer.setObjectName(u"pipeline_viewer")
        pipeline_viewer.resize(400, 212)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pipeline_viewer.sizePolicy().hasHeightForWidth())
        pipeline_viewer.setSizePolicy(sizePolicy)
        pipeline_viewer.setMinimumSize(QSize(200, 0))
        self.verticalLayout = QVBoxLayout(pipeline_viewer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pipeline_label = QLabel(pipeline_viewer)
        self.pipeline_label.setObjectName(u"pipeline_label")

        self.verticalLayout.addWidget(self.pipeline_label)

        self.pipeline_scrollbar = QScrollArea(pipeline_viewer)
        self.pipeline_scrollbar.setObjectName(u"pipeline_scrollbar")
        self.pipeline_scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.pipeline_scrollbar.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 398, 177))
        self.pipeline_scrollbar.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.pipeline_scrollbar)


        self.retranslateUi(pipeline_viewer)

        QMetaObject.connectSlotsByName(pipeline_viewer)
    # setupUi

    def retranslateUi(self, pipeline_viewer):
        pipeline_viewer.setWindowTitle(QCoreApplication.translate("pipeline_viewer", u"Form", None))
        self.pipeline_label.setText(QCoreApplication.translate("pipeline_viewer", u"Pipeline", None))
    # retranslateUi

