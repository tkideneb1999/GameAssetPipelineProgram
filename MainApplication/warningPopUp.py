from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc


class WarningPopUp(qtw.QDialog):
    def __init__(self, warning_message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WARNING!")

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
        self.button_box = qtw.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.warning = qtw.QLabel(warning_message)
        self.warning.setAlignment(qtc.Qt.AlignCenter)
        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.warning)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
