import bpy
import importlib.util


file_path_1 = 'C:/Users/frank/AppData/Roaming/Blender Foundation/Blender/4.0/scripts/addons/Vector_Dust/panel_creation.py'

# Load the module
spec_1 = importlib.util.spec_from_file_location("panel_creation", file_path_1)
pc = importlib.util.module_from_spec(spec_1)
spec_1.loader.exec_module(pc)

file_path_2 = 'C:/Users/frank/AppData/Roaming/Blender Foundation/Blender/4.0/scripts/addons/Vector_Dust/cabinet_operations.py'

# Load the module
spec_2 = importlib.util.spec_from_file_location("panel_creation", file_path_2)
cbt = importlib.util.module_from_spec(spec_2)
spec_2.loader.exec_module(cbt)


class CONTROL_PT_Panel(bpy.types.Panel):
    bl_label = ''
    bl_idname = 'CONTROL_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Dust Panel'

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text='Control Panel')
        row.operator('ctp.sqn_add', icon='PLUS')
        row.operator('ctp.clear', icon='X')

    def draw(self, context):
        layout = self.layout


class CONTROL_OT_SqnAddButton(bpy.types.Operator):
    bl_label = ''
    bl_idname = 'ctp.sqn_add'

    def execute(self, context):
        cbt.file_panel(None, 'SQN')
        pc.redraw()
        return {'FINISHED'}

class CONTROL_OT_Clear(bpy.types.Operator):
    bl_label = ''
    bl_idname = 'ctp.clear'

    def execute(self, context):
        pc.erase_panels()
        cbt.clear_undrawns()
        return {'FINISHED'}


SystemPanels = [CONTROL_OT_SqnAddButton, CONTROL_OT_Clear, CONTROL_PT_Panel, ]


def register_control_panel():
    for system_class in SystemPanels:
        bpy.utils.register_class(system_class)

def unregister_control_panel():
    for system_class in SystemPanels:
        bpy.utils.unregister_class(system_class)
