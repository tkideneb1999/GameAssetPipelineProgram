from pathlib import Path
import json

from .program_registration import ProgramRegistration


class Settings(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            # Singleton
            print("Creating Settings")
            cls.instance = super(Settings, cls).__new__(cls)

            # Init
            cls.program_registration = ProgramRegistration()

            cls.current_project_info_path = Path()
            cls.has_settings = False

            cls.save_path = Path.home() / "documents" / "GAPASettings"

        return cls.instance

    def register_program(self, name: str, path: Path, addon_enabled=False) -> None:
        self.program_registration.add_program(name, path)
        self.save()

    def remove_program(self, name: str) -> None:
        result = self.program_registration.remove_program(name)
        if result:
            print(f"[GAPA] Removed {name} from registered programs")
            self.save()

    def set_current_project(self, project_info_path: Path) -> None:
        self.current_project_info_path = project_info_path
        self.save()

    def save(self) -> None:
        if not self.save_path.exists():
            self.save_path.mkdir(parents=True)
        self.program_registration.save(self.save_path)

        settings_path = self.save_path / "settings.json"
        if not settings_path.exists():
            settings_path.touch()
        data = {"current_project": str(self.current_project_info_path)}
        with settings_path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))

    def load(self) -> None:
        print(f"[GAPA] Loading settings from {self.save_path}")
        if not self.save_path.exists():
            print("Settings Files do not exist")
            self.has_settings = False
            return
        self.program_registration.load(self.save_path)
        settings_path = self.save_path / "settings.json"
        if not settings_path.exists():
            print("[GAPA] No settings file detected")
            self.has_settings = False
            return
        with settings_path.open("r", encoding="utf-8") as f:
            data = json.loads(f.read())
            self.current_project_info_path = Path(data["current_project"])
            self.has_settings = True

    def enable_addon(self, name: str, addon_path: Path):
        print("[GAPA] Enabling Addon in Settings")
        self.program_registration.enable_addon(name, addon_path)
        self.save()
