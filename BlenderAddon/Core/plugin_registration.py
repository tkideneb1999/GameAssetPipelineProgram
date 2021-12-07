from pathlib import Path
import json
import os
import sys
import importlib


class PluginRegistration:
    def __init__(self):
        self.registered_plugins = {}
        self.plugin_dir: Path = None

    def set_plugin_dir(self, directory: Path) -> None:
        self.plugin_dir = directory

    def register_plugins(self):
        if self.plugin_dir is None:
            print("[GAPA] Plugin Dir not set")
            return
        filenames = os.listdir(self.plugin_dir)
        print(sys.path)
        for filename in filenames:
            if not (self.plugin_dir / filename / "__init__.py").exists():
                print(f"[GAPA] Plugin has no __init__ file: {filename}")
                continue
            module = importlib.import_module(filename)
            module.register()

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
        print(sys.path)
        self.register_plugins()

    def save(self, directory: Path) -> None:
        save_file = directory / "registeredPlugins.json"
        if not save_file.exists():
            save_file.touch()
        with save_file.open("w", encoding="utf-8") as f:
            data = {
                "pluginDir": str(self.plugin_dir)
            }
            f.write(json.dumps(data, indent=4))
