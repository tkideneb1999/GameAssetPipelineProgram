import bpy
from pathlib import Path


class GAPA_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    project_dir: bpy.props.StringProperty(name="Project Info File", subtype="FILE_PATH")
    # TODO(Blender Addon): Check if valid Project Path

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "project_dir")

    def on_proj_dir_update(self, context):
        if context.preferences.addons[__package__].preferences.project_dir == "":
            print("[GAPA] Project Info File Path set to None")
            return
        proj_dir = context.preferences.addons[__package__].preferences.project_dir
        is_valid = self.check_project_dir_validity(proj_dir)
        if not is_valid:
            print("[GAPA] Project Info File not valid")
            context.preferences.addons[__package__].preferences.project_dir = ""

    def check_project_dir_validity(self, filepath: Path) -> bool:
        if not filepath.exists() or (filepath.suffix == "gapaproj"):
            return False
        else:
            return True
