from pathlib import Path
import json


class ProgramRegistration:
    def __init__(self):
        self.registered_programs: dict[str, dict] = {}

    def save(self, directory: Path):
        path = directory / "registeredPrograms.json"
        with path.open('w', encoding="utf-8") as f:
            data = {}
            for p in self.registered_programs:
                data[p] = self.registered_programs[p]
                data[p]["addonPath"] = str(data[p]["addonPath"])
            f.write(json.dumps(data, indent=4))
            f.close()

    def load(self, directory: Path):
        path = directory / "registeredPrograms.json"
        if not path.exists():
            return
        print(f"[GAPA] Loading registered programs from {path}")
        with path.open('r', encoding="utf-8") as f:
            data = json.loads(f.read())

            for p in data:
                data[p]["addonPath"] = Path(data[p]["addonPath"])
            self.registered_programs = data

    def get_program_addon_path(self, name: str) -> Path:
        return Path(self.registered_programs[name]["addonPath"])

    def get_program_addon_enabled(self, name: str) -> bool:
        """
        Returns whether Addon for specific program is enabled
        :param name: registered name of the program (executable name)
        :returns: True if addon is enabled, False if not or if the program does not exist
        """
        if self.registered_programs.get(name) is not None:
            return self.registered_programs[name]["addonEnabled"]
        else:
            return False

    def get_program_list(self) -> list:
        return list(self.registered_programs.keys())

    def enable_addon(self, name: str, addon_path: Path) -> None:
        if self.registered_programs.get(name) is None:
            self.registered_programs[name] = {"addonPath": addon_path, "addonEnabled": True}
        print(f"[GAPA] Addon enabled for {name}")
