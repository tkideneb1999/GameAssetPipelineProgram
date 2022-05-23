# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loadCurrentProjectWizard_GUI.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_loadCurrentProjectWizard(object):
    def setupUi(self, loadCurrentProjectWizard):
        if not loadCurrentProjectWizard.objectName():
            loadCurrentProjectWizard.setObjectName(u"loadCurrentProjectWizard")
        loadCurrentProjectWizard.resize(400, 60)
        self.verticalLayout = QVBoxLayout(loadCurrentProjectWizard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.load_project_label = QLabel(loadCurrentProjectWizard)
        self.load_project_label.setObjectName(u"load_project_label")

        self.verticalLayout.addWidget(self.load_project_label)

        self.buttonBox = QDialogButtonBox(loadCurrentProjectWizard)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.No|QDialogButtonBox.Yes)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(loadCurrentProjectWizard)
        self.buttonBox.accepted.connect(loadCurrentProjectWizard.accept)
        self.buttonBox.rejected.connect(loadCurrentProjectWizard.reject)

        QMetaObject.connectSlotsByName(loadCurrentProjectWizard)
    # setupUi

    def retranslateUi(self, loadCurrentProjectWizard):
        loadCurrentProjectWizard.setWindowTitle(QCoreApplication.translate("loadCurrentProjectWizard", u"Dialog", None))
        self.load_project_label.setText(QCoreApplication.translate("loadCurrentProjectWizard", u"Load project from settings?", None))
    # retranslateUi

