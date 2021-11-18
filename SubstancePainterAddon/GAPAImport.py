from pathlib import Path
import importlib

from PySide2 import QtWidgets as qtw

import substance_painter.logging as spLog

from .GAPACore.UI import importWizardView

importlib.reload(importWizardView)


class GAPAImport:
    def __init__(self, sp_main_window):
        self.testDialogAction = qtw.QAction("GAPA Import")
        self.testDialogAction.triggered.connect(self.launch_import_dialog)
        self.project_info: Path = None
        self.sp_main_window = sp_main_window

    def import_files(self, filepaths) -> None:  # filepaths: list[Path]
        spLog.info("[GAPA] Importing files and creating project")
        pass

    def save_workfile(self, filepath) -> None:  # filepath: Path
        spLog.info("[GAPA] Saving workfile")
        pass

    def launch_import_dialog(self) -> None:
        if self.project_info is None:
            pass
            if not self.launch_project_dialog():
                spLog.warning("[GAPA] Project File has to be selected before importing")
                return
        # import_dialog = importWizardView.ImportWizardView(self.project_info, "Substance Painter", spUI.get_main_window())
        # import_dialog.register_import_files_func(self.import_files)
        # import_dialog.register_save_workfile_func(self.save_workfile)

    def launch_project_dialog(self) -> bool:
        dialog = qtw.QFileDialog(self.sp_main_window)
        dialog.setWindowTitle("Select the project info file ...")
        dialog.setFileMode(qtw.QFileDialog.ExistingFile)
        dialog.setNameFilter("Project File (*.gapaproj)")
        dialog.setViewMode(qtw.QFileDialog.Detail)
        result = dialog.exec_()
        if result == 0:
            return False
        self.project_info = Path(dialog.selectedFiles()[0])
