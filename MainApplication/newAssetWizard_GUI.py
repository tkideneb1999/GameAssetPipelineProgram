# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newAssetWizard_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from .Common.qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from .Common.qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from .Common.qtpy.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_new_asset_wizard(object):
    def setupUi(self, new_asset_wizard):
        if not new_asset_wizard.objectName():
            new_asset_wizard.setObjectName(u"new_asset_wizard")
        new_asset_wizard.resize(400, 212)
        self.verticalLayout = QVBoxLayout(new_asset_wizard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.name_label = QLabel(new_asset_wizard)
        self.name_label.setObjectName(u"name_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)
        self.name_label.setMinimumSize(QSize(50, 0))

        self.horizontalLayout.addWidget(self.name_label)

        self.name_line_edit = QLineEdit(new_asset_wizard)
        self.name_line_edit.setObjectName(u"name_line_edit")

        self.horizontalLayout.addWidget(self.name_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 9, -1, -1)
        self.pipeline_label = QLabel(new_asset_wizard)
        self.pipeline_label.setObjectName(u"pipeline_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pipeline_label.sizePolicy().hasHeightForWidth())
        self.pipeline_label.setSizePolicy(sizePolicy1)
        self.pipeline_label.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_5.addWidget(self.pipeline_label)

        self.pipeline_combobox = QComboBox(new_asset_wizard)
        self.pipeline_combobox.setObjectName(u"pipeline_combobox")

        self.horizontalLayout_5.addWidget(self.pipeline_combobox)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.level_label = QLabel(new_asset_wizard)
        self.level_label.setObjectName(u"level_label")
        sizePolicy.setHeightForWidth(self.level_label.sizePolicy().hasHeightForWidth())
        self.level_label.setSizePolicy(sizePolicy)
        self.level_label.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_2.addWidget(self.level_label)

        self.levels_combo_box = QComboBox(new_asset_wizard)
        self.levels_combo_box.setObjectName(u"levels_combo_box")

        self.horizontalLayout_2.addWidget(self.levels_combo_box)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tags_label = QLabel(new_asset_wizard)
        self.tags_label.setObjectName(u"tags_label")
        sizePolicy.setHeightForWidth(self.tags_label.sizePolicy().hasHeightForWidth())
        self.tags_label.setSizePolicy(sizePolicy)
        self.tags_label.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_3.addWidget(self.tags_label)

        self.tags_line_edit = QLineEdit(new_asset_wizard)
        self.tags_line_edit.setObjectName(u"tags_line_edit")

        self.horizontalLayout_3.addWidget(self.tags_line_edit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.tags_d_label = QLabel(new_asset_wizard)
        self.tags_d_label.setObjectName(u"tags_d_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tags_d_label.sizePolicy().hasHeightForWidth())
        self.tags_d_label.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.tags_d_label)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.comment_label = QLabel(new_asset_wizard)
        self.comment_label.setObjectName(u"comment_label")
        sizePolicy1.setHeightForWidth(self.comment_label.sizePolicy().hasHeightForWidth())
        self.comment_label.setSizePolicy(sizePolicy1)
        self.comment_label.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_4.addWidget(self.comment_label)

        self.comment_line_edit = QLineEdit(new_asset_wizard)
        self.comment_line_edit.setObjectName(u"comment_line_edit")

        self.horizontalLayout_4.addWidget(self.comment_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.dialogue_buttons = QDialogButtonBox(new_asset_wizard)
        self.dialogue_buttons.setObjectName(u"dialogue_buttons")
        self.dialogue_buttons.setOrientation(Qt.Horizontal)
        self.dialogue_buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.dialogue_buttons)


        self.retranslateUi(new_asset_wizard)
        self.dialogue_buttons.accepted.connect(new_asset_wizard.accept)
        self.dialogue_buttons.rejected.connect(new_asset_wizard.reject)

        QMetaObject.connectSlotsByName(new_asset_wizard)
    # setupUi

    def retranslateUi(self, new_asset_wizard):
        new_asset_wizard.setWindowTitle(QCoreApplication.translate("new_asset_wizard", u"Dialog", None))
        self.name_label.setText(QCoreApplication.translate("new_asset_wizard", u"Name*", None))
        self.pipeline_label.setText(QCoreApplication.translate("new_asset_wizard", u"Pipeline*", None))
        self.level_label.setText(QCoreApplication.translate("new_asset_wizard", u"Level*", None))
        self.tags_label.setText(QCoreApplication.translate("new_asset_wizard", u"Tags", None))
        self.tags_d_label.setText(QCoreApplication.translate("new_asset_wizard", u"Tags separated by comma", None))
        self.comment_label.setText(QCoreApplication.translate("new_asset_wizard", u"Comment", None))
    # retranslateUi

