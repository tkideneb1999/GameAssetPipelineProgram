import queue
from pathlib import Path
import json
import functools

from PyQt5 import QtCore as qtc

from .Core.settings import Settings
from .Core.asset import Asset

from MainApplication.pluginAssetSettingsView import PluginAssetSettingsView


class PluginHandler(qtc.QObject):
    def __init__(self, project_dir=None, parent=None):
        super(PluginHandler, self).__init__(parent)
        self.project_dir = project_dir
        self.settings = Settings()
        self.settings.load()
        self.parent_widget = parent

        self.plugin_thread = PluginThread(parent=self)
        self.plugin_thread.finished.connect(self.plugin_thread_finished)
        self.plugin_func_queue: queue.Queue = queue.Queue()

    def set_project_dir(self, project_dir):
        self.project_dir = project_dir

    def run_plugin(self, asset: Asset, step_index: int) -> None:
        if self.project_dir is None:
            print("[GAPA][PluginHandler] Project dir is None, can not execute plugin")
            return
        plugin_name = asset.pipeline.get_step_program(step_index)
        plugin = self.settings.plugin_registration.get_plugin(plugin_name)
        plugin_gui_settings = plugin.register_settings()
        asset_gui_settings = plugin_gui_settings.asset_settings
        step = asset.pipeline.pipeline_steps[step_index]
        saved_asset_settings = asset.pipeline_progress[step.uid]["settings"]
        if step.export_all:
            outputs = None
        else:
            outputs = [(o.uid, o.name) for o in step.outputs]
        if saved_asset_settings == {}:
            run_plugin_dialog = PluginAssetSettingsView(asset_gui_settings,
                                                        enable_execute=True,
                                                        outputs=outputs,
                                                        parent=self.parent_widget)
        else:
            run_plugin_dialog = PluginAssetSettingsView(asset_gui_settings,
                                                        enable_execute=True,
                                                        saved_settings=saved_asset_settings,
                                                        outputs=outputs,
                                                        parent=self.parent_widget)
        result = run_plugin_dialog.exec_()
        if result != 0:
            if run_plugin_dialog.execute_clicked:
                import_data = asset.import_assets(step_index)
                abs_import_paths = import_data[0]
                workfile_dir = None
                for output_set in abs_import_paths:
                    if output_set == "workfiles":
                        workfile_dir = self.project_dir / import_data[0]["workfiles"]
                        continue
                    for output in abs_import_paths[output_set]:
                        abs_import_paths[output_set][output] = (import_data[0][output_set][output][0],
                                                                self.project_dir / import_data[0][output_set][output][1])
                del abs_import_paths["workfiles"]

                if step.export_all:
                    output_uids = [o.uid for o in step.outputs]
                    export_suffixes = [o.data_type for o in step.outputs]
                else:
                    output_uids = [run_plugin_dialog.current_output[0]]
                    output_index = step.get_io_index_by_uid(output_uids[0])
                    export_suffixes = [step.outputs[output_index].data_type]

                publish_data = asset.publish_step_file(step.uid, output_uids, export_suffixes)

                # Convert relative paths to absolute paths
                abs_export_paths = publish_data
                for output_set in publish_data:
                    for o in publish_data[output_set]:
                        abs_export_paths[output_set][o] = (publish_data[output_set][o][0], self.project_dir / publish_data[output_set][o][1])

                # Collect settings
                asset_settings = run_plugin_dialog.get_settings()
                global_settings = self.settings.plugin_registration.global_settings[plugin_name]
                pipeline_settings = asset.pipeline.get_additional_settings(step_index)
                project_settings = self.get_project_settings(plugin_name)
                asset_info = {"name": asset.name,
                              "level": asset.level,
                              "tags": asset.tags,
                              "workfile_dir": workfile_dir}
                if project_settings is None:
                    return
                plugin_settings = {"global": global_settings,
                                   "pipeline": pipeline_settings,
                                   "asset": asset_settings,
                                   "project": project_settings,
                                   "asset_info": asset_info}
                config = asset.pipeline.pipeline_steps[step_index].config
                plugin_func = functools.partial(plugin.run, abs_import_paths, abs_export_paths, plugin_settings, config)
                if self.plugin_thread.isRunning():
                    self.plugin_func_queue.put(plugin_func)
                else:
                    self.plugin_thread.set_plugin_func(plugin_func)
                    self.plugin_thread.start()
            else:
                asset_settings = run_plugin_dialog.get_settings()
            asset.pipeline_progress[step.uid]["settings"] = asset_settings
            asset.save(self.project_dir)

    def get_project_settings(self, name) -> dict:
        path = Path() / self.project_dir / "projectPluginSettings.json"
        if not path.exists():
            print("[GAPA] PluginHandler: projectPluginSettings.json does not exist")
            return None
        settings = {}
        with path.open("r", encoding="utf-8") as f:
            settings = json.loads(f.read())
        return settings[name]

    def plugin_thread_finished(self):
        if self.plugin_func_queue.empty():
            return
        else:
            self.plugin_thread.set_plugin_func(self.plugin_func_queue.get())
            self.plugin_thread.start()


class PluginThread(qtc.QThread):
    def __init__(self, plugin_func=None, parent=None):
        super(PluginThread, self).__init__(parent)
        self.plugin_func = plugin_func

    def set_plugin_func(self, plugin_func):
        self.plugin_func = plugin_func

    def run(self) -> None:
        if self.plugin_func is None:
            print("[GAPA] No Plugin Function set")
            return
        self.plugin_func()
