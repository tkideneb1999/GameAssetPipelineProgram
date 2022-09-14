from ..Common.qtpy import QtWidgets as qtw

from .loadCurrentProjectWizard_GUI import Ui_loadCurrentProjectWizard


class LoadCurrentProjectWizard(qtw.QDialog):
    def __init__(self, parent=None):
        super(LoadCurrentProjectWizard, self).__init__(parent)
        self.ui = Ui_loadCurrentProjectWizard()
        self.ui.setupUi(self)
