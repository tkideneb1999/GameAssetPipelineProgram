from pathlib import Path
import importlib.util
import sys
import json


def _load_packages_paths():
    """
    Loads & returns the paths to necessary packages
    :return: dictionary of Paths to Common Package & the Main Applications Python Packages
    """
    settings_path = Path.home() / "documents" / "GAPASettings" / "settings.json"
    if not settings_path.exists():
        return
    package_paths = {}
    with settings_path.open("r", encoding="utf-8") as f:
        data = json.loads(f.read())
        package_paths["site_packages"] = Path(data["pyside_path"])
        package_paths["common_path"] = Path(data["common_path"])
    return package_paths


def _load_common_module(common_modules_path: Path):
    """
    Loads the Common Package containing GUI Functionality for Import & Export Dialogs
    :param common_modules_path: Absolute Path to the common
    """
    spec = importlib.util.spec_from_file_location("Common", common_modules_path / "__init__.py")
    common_package = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = common_package
    spec.loader.exec_module(common_package)
    return common_package


def _load_site_packages(site_packages_path: Path, use_main_app_pyside: bool):
    """
    Adds the Main Applications Site packages to the Python Environment if use_main_app_pyside is True
    Otherwise Loads the qtpy module and required packaging module
    :param site_packages_path: Path to the site Packages of the Main Application
    :param use_main_app_pyside: Whether to use the PySide6 Installation of the Main Application
    """
    # Add all packages from site packages of Main Application
    if use_main_app_pyside:
        sys.path.append(str(site_packages_path))
        return
    # Else:
    # Add packaging package
    packaging_spec = importlib.util.spec_from_file_location("packaging", site_packages_path / "packaging" / "__init__.py")
    packaging_package = importlib.util.module_from_spec(packaging_spec)
    sys.modules[packaging_spec.name] = packaging_package
    packaging_spec.loader.exec_module(packaging_package)

    # Add qtpy
    qtpy_spec = importlib.util.spec_from_file_location("qtpy", site_packages_path / "qtpy" / "__init__.py")
    qtpy_package = importlib.util.module_from_spec(qtpy_spec)
    sys.modules[qtpy_spec.name] = qtpy_package
    qtpy_spec.loader.exec_module(qtpy_package)


def load_required_packages(use_main_app_pyside: bool):
    """
    Convenience function to load necessary GAPA modules
    :param use_main_app_pyside: whether to use the PySide6 installation in the Main Applications Python Environment
    """
    package_paths = _load_packages_paths()
    _load_site_packages(package_paths["site_packages"], use_main_app_pyside)
    _load_common_module(package_paths["common_path"])

