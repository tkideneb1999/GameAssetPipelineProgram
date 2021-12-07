from pathlib import Path
import importlib
import queue
import functools

from PySide2 import QtWidgets as qtw

import substance_painter.logging as spLog
import substance_painter.project as spProj
import substance_painter.event as spEvent

from .UI import importWizardView
from .Core import settings as settingsModule

importlib.reload(importWizardView)
importlib.reload(settingsModule)


class GAPAImport:
    def __init__(self, program_name, sp_main_window):
        self.import_dialog_action = qtw.QAction("GAPA Import")
        self.import_dialog_action.triggered.connect(self.launch_import_dialog)
        self.project_info: Path = None
        self.sp_main_window = sp_main_window
        self.program = program_name
        self.queue = queue.Queue()
        spEvent.DISPATCHER.connect(spEvent.BusyStatusChanged, self.painter_busy_changed)

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
        tangent_per_frag = spProj.TangentSpace.PerVertex
        if additional_settings["Fragment Tangent"]:
            tangent_per_frag = spProj.TangentSpace.PerFragment

        # Create Settings
        settings = spProj.Settings(normal_map_format=normal_map_format,
                                   tangent_space_mode=tangent_per_frag,
                                   project_workflow=uv_workflow,
                                   import_cameras=import_cameras)
        spLog.info(f"[GAPA] creating project with config: {config}")
        mesh_path = None
        mesh_maps = []
        for f in filepaths_data:
            if config == "UE4":
                if f[0] == "lowpoly":
                    mesh_path = str(f[1])
                else:
                    mesh_maps.append(str(f[1]))
            if config == "NoMapsUE4":
                if f[0] == "lowpoly":
                    mesh_path = str(f[1])
        # check if project is open
        if spProj.is_open():
            # if project is open
            spLog.warnig("[GAPA] A Project is already opened")
            spLog.info("[GAPA] Saving opened project and closing it")
            if spProj.needs_saving():
                spProj.save(spProj.ProjectSaveMode.Full)
            spProj.close()
        spProj.create(mesh_file_path=mesh_path,
                      mesh_map_file_paths=mesh_maps,
                      settings=settings)

    def save_workfile(self, filepath, overwrite=True) -> None:  # filepath: Path
        spLog.info("[GAPA] Saving workfile")
        if not spProj.is_open():
            spLog.warning("[GAPA] No Project opened!")
            return

        if not spProj.needs_saving():
            spLog.warning("[GAPA] Nothing to save!")
            return
        metadata = spProj.Metadata("GAPA")
        metadata.set("project_info", str(self.project_info))

        def save(path_to_file):
            spProj.save_as(str(path_to_file), spProj.ProjectSaveMode.Full)
            spLog.info(f"[GAPA] Saved successfully at: {spProj.file_path()}")

        func = functools.partial(save, filepath)
        self.queue_function(func)

    def launch_import_dialog(self) -> None:
        if spProj.is_open() and (self.project_info is None):
            metadata = spProj.Metadata("GAPA")
            key_list = metadata.list()
            if "project_info" in key_list:
                self.project_info = Path(metadata.get("project_info"))
        if self.project_info is None:
            spLog.info("Using current project from GAPA Settings")
            settings = settingsModule.Settings()
            settings.load()
            if not settings.has_settings:
                print("[GAPA] No Project dir set in GAPA Settings. Set a project with the Main Application")
                return
            self.project_info = settings.current_project_info_path
        import_dialog = importWizardView.ImportWizardView(self.project_info, self.program, self.sp_main_window)
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

    def queue_function(self, func):
        if spProj.is_busy():
            self.queue.put(func)
        else:
            func()

    def painter_busy_changed(self, is_busy):
        if is_busy:
            return
        else:
            func = self.queue.get()
            func()
