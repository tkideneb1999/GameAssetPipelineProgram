from pathlib import Path
import os

from MainApplication.Common.Core.settings import Settings

pyside_path = Path(os.path.abspath(__file__)).parent / "venv" / "Lib" / "site-packages"
plugin_path = Path(os.path.abspath(__file__)).parent / "MainApplication" / "Plugins"
common_path = Path(os.path.abspath(__file__)).parent / "MainApplication" / "Common"
settings = Settings()
settings._set_pyside_path(pyside_path)
settings._set_plugin_dir(plugin_path)
settings._set_common_path(common_path)
settings.save()
