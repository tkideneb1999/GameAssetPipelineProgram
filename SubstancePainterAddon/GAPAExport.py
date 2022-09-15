from pathlib import Path
import functools
import queue
import importlib
import json

from qtpy import QtWidgets as qtw
from qtpy import QtCore as qtc

import substance_painter.logging as spLog
import substance_painter.project as spProj
import substance_painter.textureset as spTexSet
import substance_painter.export as spExp

from Common.Dialogs import exportWizardView
from . import pipelineSettings as pS

importlib.reload(exportWizardView)
importlib.reload(pS)


class GAPAExport:
    def __init__(self, program_name, sp_main_window):
        self.export_dialog_action = qtw.QAction("GAPA Export")
        self.export_dialog_action.triggered.connect(self.launch_export_dialog)
        self.project_info: Path = None
        self.sp_main_window = sp_main_window
        self.program = program_name
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.process_queue)
        self.timer.start(1)
        self.queue = queue.Queue()

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
        export_dialog = exportWizardView.ExportWizardView(self.project_info,
                                                          self.program,
                                                          pS.WORKFILE_SUFFIX,
                                                          self.sp_main_window)
        export_dialog.register_export_func(self.export_file)
        export_dialog.register_save_workfile_func(self.save_workfile)
        export_dialog.register_get_output_sets_func(self.get_output_sets)
        export_dialog.exec_()

    def export_file(self, file_paths, config_name, export_settings) -> None:
        print(f"[GAPA] exporting to following paths: {file_paths}")
        config_path = Path(pS.get_pipeline_settings_location()).parent / "configs" / f"{config_name}.json"
        config_data = {}
        with config_path.open("r", encoding="utf-8") as c:
            config_data = json.loads(c.read())
        for o in range(len(config_data["output"]["outputs"])):
            output_name = config_data["output"]["outputs"][o]["outputName"]
            first_entry = list(file_paths.keys())[0]
            for o_uid in file_paths[first_entry]:
                if file_paths[first_entry][o_uid][0] == output_name:
                    index = list(file_paths[first_entry]).index(o_uid)
                    config_data["output"]["outputs"][o]["fileName"] = file_paths[first_entry][o_uid][1].stem
                    if config_data["output"]["outputs"][o]["parameters"].get("fileFormat") is None:
                        config_data["output"]["outputs"][o]["parameters"]["fileFormat"] = export_settings["output_format"][index]
        export_config = {
            "exportPath": None,
            "defaultExportPreset": config_name,
            "exportShaderParams": config_data["output"]["options"]["exportShaderParams"],
            "exportPresets": [{
                "name": config_name,
                "maps": config_data["output"]["outputs"]
            }]
        }
        export_parameters = [{"parameters": {}}]
        export_config["exportParameters"] = export_parameters
        for output_set in file_paths:
            first_entry = list(file_paths[output_set].keys())[0]
            path = file_paths[output_set][first_entry][1].parent
            export_config["exportPath"] = str(path)
            export_list = [{
                "rootPath": output_set,
                "exportPreset": config_name
            }]
            export_config["exportList"] = export_list

            def export():
                result = spExp.export_project_textures(export_config)
                print(f"[GAPA] {result.message}")

            self.queue_function(export)

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

        def save(path_to_file):
            spProj.save_as(str(path_to_file), spProj.ProjectSaveMode.Full)
            spLog.info(f"[GAPA] Saved successfully at: {spProj.file_path()}")

        func = functools.partial(save, filepath)
        self.queue_function(func)

    def get_output_sets(self) -> list:
        print("[GAPA] Getting texture set names for output sets")
        texture_sets = spTexSet.all_texture_sets()
        texture_set_names = []
        for tex_set in texture_sets:
            texture_set_names.append(tex_set.name())
        return texture_set_names

    def queue_function(self, func):
        if spProj.is_busy():
            self.queue.put(func)
        else:
            func()

    def process_queue(self):
        if spProj.is_busy():
            return
        if self.queue.empty():
            return
        func = self.queue.get()
        func()
