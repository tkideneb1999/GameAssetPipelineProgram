from pathlib import Path

from program_registration import ProgramRegistration


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Singleton
            print("Creating Settings")
            cls._instance = super(Settings, cls).__new__(cls)

            # Init
            cls.program_registration = ProgramRegistration()
            cls.save_path = Path.home() / "documents" / "GAPASettings"

        return cls._instance

    def register_program(self, name: str, path: Path, addon_enabled=False) -> None:
        self.program_registration.add_program(name, path)
        self.save()

    def save(self) -> None:
        if not self.save_path.exists():
            self.save_path.mkdir(parents=True)
        self.program_registration.save(self.save_path)

    def load(self) -> None:
        print(f"[GAPA] Loading settings from {self.save_path}")
        if not self.save_path.exists():
            print("Settings Files do not exist")
            return
        self.program_registration.load(self.save_path)

    def enable_addon(self, name: str):
        print("[GAPA] Enabling Addon in Settings")
        self.program_registration.enable_addon(name)
        self.save()
