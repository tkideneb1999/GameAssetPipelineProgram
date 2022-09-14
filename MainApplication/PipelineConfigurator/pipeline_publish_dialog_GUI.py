# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipeline_publish_dialog_GUI.ui'
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
from ..Common.qtpy.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_PublishDialog(object):
    def setupUi(self, PublishDialog):
        if not PublishDialog.objectName():
            PublishDialog.setObjectName(u"PublishDialog")
        PublishDialog.resize(367, 155)
        self.verticalLayout = QVBoxLayout(PublishDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.name_line_edit = QLineEdit(PublishDialog)
        self.name_line_edit.setObjectName(u"name_line_edit")

        self.verticalLayout.addWidget(self.name_line_edit)

        self.error_msg_label = QLabel(PublishDialog)
        self.error_msg_label.setObjectName(u"error_msg_label")
        palette = QPalette()
        brush = QBrush(QColor(255, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.error_msg_label.setPalette(palette)

        self.verticalLayout.addWidget(self.error_msg_label)

        self.registered_pipelines_list = QListWidget(PublishDialog)
        self.registered_pipelines_list.setObjectName(u"registered_pipelines_list")
        self.registered_pipelines_list.setEnabled(False)

        self.verticalLayout.addWidget(self.registered_pipelines_list)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ok_button = QPushButton(PublishDialog)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setEnabled(False)

        self.horizontalLayout.addWidget(self.ok_button)

        self.cancel_button = QPushButton(PublishDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout.addWidget(self.cancel_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(PublishDialog)
        self.ok_button.clicked.connect(PublishDialog.accept)
        self.cancel_button.clicked.connect(PublishDialog.reject)

        QMetaObject.connectSlotsByName(PublishDialog)
    # setupUi

    def retranslateUi(self, PublishDialog):
        PublishDialog.setWindowTitle(QCoreApplication.translate("PublishDialog", u"Publish...", None))
        self.name_line_edit.setPlaceholderText(QCoreApplication.translate("PublishDialog", u"Pipeline Name", None))
        self.error_msg_label.setText("")
        self.ok_button.setText(QCoreApplication.translate("PublishDialog", u"Ok", None))
        self.cancel_button.setText(QCoreApplication.translate("PublishDialog", u"Cancel", None))
    # retranslateUi

