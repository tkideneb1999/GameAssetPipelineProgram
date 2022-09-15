# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assetDetails_GUI.ui'
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
from qtpy.QtWidgets import (QApplication, QFormLayout, QLabel, QSizePolicy,
                                                   QWidget)

class Ui_asset_details(object):
    def setupUi(self, asset_details):
        if not asset_details.objectName():
            asset_details.setObjectName(u"asset_details")
        asset_details.resize(407, 90)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(asset_details.sizePolicy().hasHeightForWidth())
        asset_details.setSizePolicy(sizePolicy)
        asset_details.setMinimumSize(QSize(0, 90))
        self.formLayout = QFormLayout(asset_details)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.name_d_label = QLabel(asset_details)
        self.name_d_label.setObjectName(u"name_d_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.name_d_label)

        self.name_label = QLabel(asset_details)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.name_label)

        self.level_d_label = QLabel(asset_details)
        self.level_d_label.setObjectName(u"level_d_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.level_d_label)

        self.level_label = QLabel(asset_details)
        self.level_label.setObjectName(u"level_label")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.level_label)

        self.pipeline_d_label = QLabel(asset_details)
        self.pipeline_d_label.setObjectName(u"pipeline_d_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.pipeline_d_label)

        self.pipeline_label = QLabel(asset_details)
        self.pipeline_label.setObjectName(u"pipeline_label")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pipeline_label)

        self.tags_d_label = QLabel(asset_details)
        self.tags_d_label.setObjectName(u"tags_d_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.tags_d_label)

        self.tags_label = QLabel(asset_details)
        self.tags_label.setObjectName(u"tags_label")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.tags_label)

        self.comment_d_label = QLabel(asset_details)
        self.comment_d_label.setObjectName(u"comment_d_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.comment_d_label)

        self.comment_label = QLabel(asset_details)
        self.comment_label.setObjectName(u"comment_label")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comment_label)


        self.retranslateUi(asset_details)

        QMetaObject.connectSlotsByName(asset_details)
    # setupUi

    def retranslateUi(self, asset_details):
        asset_details.setWindowTitle(QCoreApplication.translate("asset_details", u"Form", None))
        self.name_d_label.setText(QCoreApplication.translate("asset_details", u"Name:", None))
        self.name_label.setText("")
        self.level_d_label.setText(QCoreApplication.translate("asset_details", u"Level:", None))
        self.level_label.setText("")
        self.pipeline_d_label.setText(QCoreApplication.translate("asset_details", u"Pipeline:", None))
        self.pipeline_label.setText("")
        self.tags_d_label.setText(QCoreApplication.translate("asset_details", u"Tags:", None))
        self.tags_label.setText("")
        self.comment_d_label.setText(QCoreApplication.translate("asset_details", u"Comment:", None))
        self.comment_label.setText("")
    # retranslateUi

