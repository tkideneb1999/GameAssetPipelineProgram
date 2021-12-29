import json
import os
from pathlib import Path

import pluginAPI

from . import xNormal

gen_name_suffix_map = {
    "gen_normals": "normals",
    "gen_heights": "heights",
    "gen_ao": "occlusion",
    "gen_bent": "bent_normals",
    "gen_prt": "prtP",
    "gen_proximity": "proximity",
    "gen_convexity": "convexity",
    "gen_thickness": "thickness",
    "gen_cavity": "cavity",
    "gen_wire": "wire_rays",
    "gen_directions": "directions",
    "gen_radiosity_normals": "radNM",
    "gen_curve": "curvature",
    "gen_derivative_normals": "deriv",
    "gen_translucency": "translucency"
}

def get_file_path() -> Path:
    return Path(os.path.abspath(__file__))


def run(import_data: dict, export_data: dict, settings: dict, config_name: str) -> None:

    # Set xNormal Path
    xNormal_path = Path(settings["global"]["exe path"])
    if not xNormal_path.exists():
        print(f"[xNormal Plugin] exe Path does not exist: {str(xNormal_path)}")
        return
    if not xNormal_path.is_file():
        print(f"[xNormal Plugin] exe Path is not a file: {str(xNormal_path)}")

    xNormal.path = str(xNormal_path)

    # Load Config
    config_path = get_file_path().parent / "Configs" / f"{config_name}.json"
    config_data = {}
    with config_path.open("r", encoding="utf-8") as f:
        config_data = json.loads(f.read())

    gen_opts_dict = {
        "width": settings["asset"]["Width"],
        "height": settings["asset"]["height"],
        "edge_padding": settings["asset"]["edge_padding"],
        "bucket_size": settings["asset"]["Bucket Size"],

        "aa": settings["asset"]["Antialiasing"]
    }
    high_meshes = []
    low_meshes = []


    # Substance Normal Map Types
    normals_y = "Y+"
    if settings["pipeline"]["Normal Map Type"] == "DirectX":
        normals_y = "Y-"

    import_file_paths = import_data[0]
    for output_set in import_file_paths:
        for uid in import_file_paths[output_set]:
            file_data = import_file_paths[output_set][uid]
            if file_data[0] == "highpoly":
                high_opts = {
                    "average_normals": config_data["input"]["inputs"][1]["average_normals"],
                }
                high_meshes.append(xNormal.high_mesh_options(file_data[1], **high_opts))
            if file_data[0] == "lowpoly":
                low_opts = {
                    "average_normals": config_data["input"]["inputs"][1]["average_normals"],
                    "normals_y": normals_y
                }
                low_meshes.append(xNormal.low_mesh_options(file_data[1], **low_opts))

    config_output_names = [o["outputName"] for o in list(config_data["output"]["outputs"].values())]
    for output_set in export_data:
        map_gens = []
        for uid in export_data[output_set]:
            output_name = export_data[output_set][uid][0]
            gen_name = config_data["output"]["outputs"].index(output_name)["genName"]
            if gen_name not in gen_name_suffix_map:
                print(f"[xNormal Plugin] Gen Name not a valid baker: {gen_name}")
            gen_opts_dict[gen_name] = True
            file_path: Path = export_data[output_set][uid][1]
            map_gens.append((gen_name, file_path.stem))
        # if settings["pipeline"]["Bake sets separate"]:
        # Generate Gen Options
        temp_path: Path = list(export_data[output_set].values())[0][1]
        suffix = temp_path.suffix
        temp_path = temp_path.parent / f"temp.{suffix}"
        gen_opts = xNormal.generation_options(temp_path, **gen_opts_dict)

        # Generate and serialize Config String
        config_string = xNormal.config(high_meshes, low_meshes, gen_opts)
        xml_config_path = temp_path.parent / "xNormalBakeConfig.xml"
        with xml_config_path.open("w", encoding="utf-8") as f:
            f.write(config_string)

        # Run xNormal
        print(f"[xNormal Plugin] Running xNormal.\n Enabled Bakers: {map_gens}")
        retcode = xNormal.run_config_filename(str(xml_config_path))
        if not retcode == 0:
            print("[xNormal Plugin] Baking not successful")
            return
        for gen_name in map_gens:
            file_path = temp_path.parent / f"temp_{gen_name_suffix_map[gen_name[0]]}.{suffix}"
            if not file_path.exists():
                print(f"[xNormal Plugin] File does not exist under that name: {file_path.name}")
                continue
            file_path.rename(file_path.with_stem(gen_name[1]))


def register_settings() -> pluginAPI.PluginSettings:
    config_path = get_file_path().parent / "Configs"
    config_folder_exists = config_path.exists()
    print(f"ConfigPath exists: {config_folder_exists}, at: {config_path}")
    settings = pluginAPI.PluginSettings(config_dir=config_path)
    settings.set_export_data_types(["tga", "png", "exr"])

    # Global Settings
    settings.add_lineedit("exe path", pluginAPI.SettingsEnum.GLOBAL)

    # Pipeline Settings
    settings.add_combobox("Normal Map Type", pluginAPI.SettingsEnum.PIPELINE, ["OpenGL", "DirectX"])

    # Asset Settings
    settings.add_combobox("Width", pluginAPI.SettingsEnum.ASSET, ["16", "32", "64", "128", "256", "512", "1024", "2048",
                                                                  "4096"])
    settings.add_combobox("Height", pluginAPI.SettingsEnum.ASSET, ["16", "32", "64", "128", "256", "512", "1024",
                                                                   "2048", "4096"])
    settings.add_combobox("Antialiasing", pluginAPI.SettingsEnum.ASSET, ["1x", "2x", "4x"])
    settings.add_combobox("Bucket Size", pluginAPI.SettingsEnum.ASSET, ["16", "32", "64", "128", "256", "512"])
    settings.add_lineedit("Edge Padding", pluginAPI.SettingsEnum.ASSET, default_value="1")
    settings.add_lineedit("Max Ray Distance Front", pluginAPI.SettingsEnum.ASSET, "50")
    settings.add_lineedit("Max Ray Distance Back", pluginAPI.SettingsEnum.ASSET, "50")
    settings.add_checkbox("Bake sets separate", pluginAPI.SettingsEnum.ASSET)

    settings.add_combobox("Heights Tonemap", pluginAPI.SettingsEnum.ASSET, ["Interactive", "Manual", "RawFPValues"], tab="Height Map")

    return settings
