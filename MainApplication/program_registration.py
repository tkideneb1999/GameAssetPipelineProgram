from pathlib import Path
import json


class ProgramRegistration:
    def __init__(self):
        self.registered_programs = {}

    def add_program(self, name: str, path: Path, addon_enabled=False):
        self.registered_programs[name] = {"path": path, "addonEnabled": addon_enabled}
        print(f"Added Program: {name}\n    Location: {str(path)}")

    def save(self, directory: Path):
        path = directory / "registeredPrograms.json"
        with path.open('w', encoding="utf-8") as f:
            data = {}
            for p in self.registered_programs:
                data[p] = self.registered_programs[p]
                data[p]["path"] = str(data[p]["path"])
            f.write(json.dumps(self.registered_programs, indent=4))
            f.close()

    def load(self, directory: Path):
        path = directory / "registeredPrograms.json"
        with path.open('r', encoding="utf-8") as f:
            data = json.loads(f.read())
            for p in data:
                print(p)
                self.registered_programs[p] = {"path": Path(data[p]["path"]), "addonEnabled": data[p]["addonEnabled"]}

    def get_program_path(self, name: str) -> Path:
        return self.registered_programs[name]["path"]

    def get_program_addon_enabled(self, name: str) -> bool:
        return self.registered_programs[name]["addonEnabled"]