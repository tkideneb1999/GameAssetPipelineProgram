from pathlib import Path
import importlib

from PySide2 import QtWidgets as qtw

import substance_painter.logging as spLog
import substance_painter.project as spProj

from .GAPACore.UI import exportWizardView
from . import pipelineSettings as pS

importlib.reload(exportWizardView)
importlib.reload(pS)


class GAPAExport:
    def __init__(self, sp_main_window):
        self.export_dialog_action = qtw.QAction("GAPA Export")
        self.export_dialog_action.triggered.connect(self.launch_export_dialog)
        self.project_info: Path = None
        self.sp_main_window = sp_main_window

    def launch_export_dialog(self):
        if not spProj.is_open():
            spLog.warning("[GAPA] No Open Project, nothing to export!")
            return
        metadata = spProj.Metadata("GAPA")
        key_list = metadata.list()
        if "project_info" in key_list:
            self.project_info = Path(metadata.get("project_info"))
        else:
            print("[GAPA] Currently opened project is not part of the Pipeline")
        export_dialog = exportWizardView.ExportWizardView(self.project_info, "Substance Painter", self.sp_main_window)
        export_dialog.register_export_func(self.export_file)
        export_dialog.register_save_workfile_func(self.save_workfile)
        export_dialog.exec_()

    def export_file(self, filepath, config_name, export_settings) -> None:
        config_path = Path(pS.get_pipeline_settings_location()).parent / "configs" / f"{config_name}.json"

        pass

    def save_workfile(self, filepath) -> None:
        spLog.info("[GAPA] Saving workfile")
        if not spProj.is_open():
            spLog.warning("[GAPA] No Project opened!")
            return

        if not spProj.needs_saving():
            spLog.warning("[GAPA] Nothing to save!")
            return
        metadata = spProj.Metadata("GAPA")
        metadata.set("project_info", str(self.project_info))
        spProj.save_as(str(filepath), spProj.ProjectSaveMode.Full)
        spLog.info(f"[GAPA] Saved successfully at: {spProj.file_path()}")
