bl_info = {
    "name": "Game Asset Pipeline Automation",
    "blender": (2, 93 ,3),
    "category": "Automation"
}

import bpy
import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
IS_CONNECTED_TO_HOST = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    
class GAPAExport(bpy.types.Operator):
    """Game Asset Pipeline Automation Export"""
    bl_idname = "wm.gapa_export"
    bl_label = "GAPA Export"
    bl_options =  {'REGISTER'}
    
    def execute(self, context):
        print("Send signal to Main Application")
        send("This is a test message")
        return {'FINISHED'}

        
def menu_func(self, context):
    self.layout.operator(GAPAExport.bl_idname)


def register():
    client.settimeout(2.0)
    global IS_CONNECTED_TO_HOST
    try:
        client.connect(ADDR)
        IS_CONNECTED_TO_HOST = True
        client.setblocking(True)
    except socket.timeout:
        print("[WARNING] Could not connect to Host Application")
        IS_CONNECTED_TO_HOST = False
        
    bpy.utils.register_class(GAPAExport)
    bpy.types.TOPBAR_MT_file.append(menu_func)
    

def unregister():
    bpy.utils.unregister_class(GAPAExport)
    bpy.types.TOPBAR_MT_file.remove(menu_func)
    print(f"Connected to Host = {IS_CONNECTED_TO_HOST}")
    if IS_CONNECTED_TO_HOST:
        send(DISCONNECT_MSG)
    print("Goodbye World!")
    

def send(msg):
    e_msg = msg.encode(FORMAT)
    l_msg = len(msg)
    h_msg = str(l_msg).encode(FORMAT)
    h_msg += b' ' * (HEADER - len(h_msg))
    client.send(h_msg)
    client.send(e_msg)
    print(f"[SENT] {msg}")