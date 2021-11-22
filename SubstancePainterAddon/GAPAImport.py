from pathlib import Path
import importlib

from PySide2 import QtWidgets as qtw

import substance_painter.logging as spLog
import substance_painter.project as spProj

from .GAPACore.UI import importWizardView

importlib.reload(importWizardView)


class GAPAImport:
    def __init__(self, sp_main_window):
        self.import_dialog_action = qtw.QAction("GAPA Import")
        self.import_dialog_action.triggered.connect(self.launch_import_dialog)
        self.project_info: Path = None
        self.sp_main_window = sp_main_window

    def import_files(self, filepaths_data, config, additional_settings) -> None:
        # filepaths: list[tuple[str,Path]], config: str, additional_settings: dict
        spLog.info("[GAPA] Importing files and creating project")

        # Settings
        # Normal Map Format
        normal_map_format = None
        if additional_settings["Normal Map"] == "OpenGL":
            normal_map_format = spProj.NormalMapFormat.OpenGL
        else:
            normal_map_format = spProj.NormalMapFormat.DirectX

        # Use UDIM
        uv_workflow = None
        if additional_settings["UDIM Workflow"] == "No UDIM":
            uv_workflow = spProj.ProjectWorkflow.Default
        elif additional_settings["UDIM Workflow"] == "Texture Set per UV Tile":
            uv_workflow = spProj.ProjectWorkflow.TextureSetPerUVTile
        else:
            uv_workflow = spProj.ProjectWorkflow.UVTile

        # Import Cameras
        import_cameras = additional_settings["Import Cameras"]

        # Tangent per Fragment
        tangent_per_frag = additional_settings["Fragment Tangent"]

        # Create Settings
        settings = spProj.Settings(normal_map_format=normal_map_format,
                                   tangent_space_mode=tangent_per_frag,
                                   project_workflow=uv_workflow,
                                   import_cameras=import_cameras)

        mesh_path = None
        for f in filepaths_data:
            if config == "UE4":
                if f[0] == "lowpoly":
                    mesh_path = f[1]
        # check if project is open
        if spProj.is_open():
            # if project is open
            spLog.warning("Project is already opened")
        #   is it from the same asset
        # if not
        #   create new project with assets
        else:
            spProj.create(mesh_file_path=mesh_path,
                          settings=settings)

    def save_workfile(self, filepath, overwrite=True) -> None:  # filepath: Path
        spLog.info("[GAPA] Saving workfile")
        if not spProj.is_open():
            spLog.warning("[GAPA] No Project opened!")
            return

        if not spProj.needs_saving():
            spLog.warning("[GAPA] Nothing to save!")
            return

        spProj.save_as(str(filepath), spProj.ProjectSaveMode.Full)
        spLog.info(f"[GAPA] Saved successfully at: {spProj.file_path()}")

    def launch_import_dialog(self) -> None:
        if self.project_info is None:
            if not self.launch_project_dialog():
                spLog.warning("[GAPA] Project File has to be selected before importing")
                return
        import_dialog = importWizardView.ImportWizardView(self.project_info, "Substance Painter", self.sp_main_window)
        import_dialog.register_import_files_func(self.import_files)
        import_dialog.register_save_workfile_func(self.save_workfile)
        import_dialog.exec_()

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
        return True
