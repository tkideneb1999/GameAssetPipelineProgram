from PySide2 import QtWidgets as qtw
import substance_painter.ui


class GAPAImport:
    def __init__(self):
        self.log = qtw.QTextEdit()
        self.log.setReadOnly(True)
        self.log.setWindowTitle("GAPA Import")
        substance_painter.ui.add_dock_widget(self.log)
        self.testDialogAction = qtw.QAction("Lauch Test Dialog...")
        self.testDialogAction.triggered.connect(self.launch_dialog)
        substance_painter.ui.add_action(
            substance_painter.ui.ApplicationMenu.File,
            self.testDialogAction
        )

    def launch_dialog(self):
        dialog = TestDialog(substance_painter.ui.get_main_window())
        if dialog.exec_():
            self.log.append("Hello")
        else:
            self.log.append("Not Hello")


class TestDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        self.button = qtw.QPushButton(self)
        self.button.setText("Much Wow")

        self.button.clicked.connect(self.clicked)
        self.layout = qtw.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def clicked(self):
        print("Clicked Button")
        self.accept()


GAPAIMPORT_PLUGIN = None


def start_plugin():
    global GAPAIMPORT_PLUGIN
    GAPAIMPORT_PLUGIN = GAPAImport()


def close_plugin():
    global GAPAIMPORT_PLUGIN
    del GAPAIMPORT_PLUGIN


if __name__ == "__main__":
    start_plugin()
