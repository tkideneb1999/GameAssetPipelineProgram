import bpy

bl_info = {
    "name": "Game Asset Pipeline Automation",
    "blender": (2, 93 ,3),
    "category": "Automation"
}

    
class GAPAExport(bpy.types.Operator):
    """Game Asset Pipeline Automation Export"""
    bl_idname = "wm.gapa_export"
    bl_label = "GAPA Export"
    bl_options =  {'REGISTER'}
    
    def execute(self, context):
        print("Send signal to Main Application")
        return {'FINISHED'}

        
def menu_func(self, context):
    self.layout.operator(GAPAExport.bl_idname)


def register():
    bpy.utils.register_class(GAPAExport)
    bpy.types.TOPBAR_MT_file.append(menu_func)
    

def unregister():
    bpy.utils.unregister_class(GAPAExport)
    bpy.types.TOPBAR_MT_file.remove(menu_func)
    print("Goodbye World!")