from pathlib import Path
import json
import os
import sys
import importlib


class PluginRegistration:
    def __init__(self):
        self.registered_plugins = {}
        self.plugin_dir: Path = None
        self.global_settings = {}

    def set_plugin_dir(self, directory: Path) -> None:
        self.plugin_dir = directory

    def register_plugins(self):
        if self.plugin_dir is None:
            print("[GAPA] Plugin Dir not set")
            return
        filenames = os.listdir(self.plugin_dir)
        for filename in filenames:
            if filename == "pluginAPI.py" or filename == "__pycache__":
                continue
            if not (self.plugin_dir / filename / "__init__.py").exists():
                print(f"[GAPA] Plugin has no __init__ file: {filename}")
                continue
            module = importlib.import_module(filename)

            # Check if necessary functions exist
            try: 
                module.register_settings
            except NameError:
                print(f"[GAPA] Plugin has no register_settings function: {filename}")
                continue
            try:
                module.run
            except NameError:
                print(f"[GAPA] Plugin has no run function: {filename}")
                continue
            self.registered_plugins[filename] = module
            settings = module.register_settings()
            plugin_settings = {}
            for param in settings.global_settings:
                gui_type = settings.global_settings[param]["type"]
                if gui_type == "combobox":
                    plugin_settings[param] = settings.global_settings[param]["data"][0]
                elif (gui_type == "lineedit") and (settings.global_settings[param]["data"] is None):
                    plugin_settings[param] = ""
                else:
                    plugin_settings[param] = settings.global_settings[param]["data"]
            plugin_settings["has_set_outputs"] = settings.has_set_outputs
            plugin_settings["export_all"] = settings.export_all
            self.global_settings[filename] = plugin_settings

    def load_global_settings(self, directory: Path) -> None:
        for plugin_name in self.global_settings:
            path = directory / f"{plugin_name}.json"
            if not path.exists():
                print(f"[GAPA] Plugin has no Global Settings saved, using default settings: {plugin_name}")
                continue
            with path.open("r", encoding="utf-8") as f:
                data = json.loads(f.read())
                self.global_settings[plugin_name] = data

    def get_plugin_list(self) -> list:
        return list(self.registered_plugins.keys())

    def get_plugin(self, name: str):
        return self.registered_plugins[name]

    def save_global_settings(self, directory: Path) -> None:
        for plugin_name in self.global_settings:
            path = directory / f"{plugin_name}.json"
            if not path.exists():
                path.touch()
            with path.open("w", encoding="utf-8") as f:
                f.write(json.dumps(self.global_settings[plugin_name], indent=4))

    def load(self, directory: Path) -> None:
        save_file = directory / "registeredPlugins.json"
        print(f"[GAPA] Loading Plugin Registration settings from: {str(save_file)}")
        if not save_file.exists():
            print("Start Main Application at least once to make use of Plugins")
            return
        with save_file.open("r", encoding="utf-8") as f:
            data = json.loads(f.read())
            self.plugin_dir = Path(data["pluginDir"])
        plugin_dir_registered = False
        for path in sys.path:
            if path == str(self.plugin_dir):
                plugin_dir_registered = True
                break
        if not plugin_dir_registered:
            sys.path.append(str(self.plugin_dir))
        self.register_plugins()
        self.load_global_settings(directory)

    def save(self, directory: Path) -> None:
        save_file = directory / "registeredPlugins.json"
        if not save_file.exists():
            save_file.touch()
        with save_file.open("w", encoding="utf-8") as f:
            data = {
                "pluginDir": str(self.plugin_dir)
            }
            f.write(json.dumps(data, indent=4))
        self.save_global_settings(directory)
