import importlib.util
import os
import bpy

current_dir = os.path.dirname(os.path.abspath(__file__))

module_name_1 = "ui_creation"  # Name of the module you want to import
module_file_1 = module_name_1 + ".py"
module_path_1 = os.path.join(current_dir, module_file_1)

# Load the module
spec_1 = importlib.util.spec_from_file_location(module_name_1, module_path_1)
ui = importlib.util.module_from_spec(spec_1)
spec_1.loader.exec_module(ui)

module_name_2 = "cabinet_operations"  # Name of the module you want to import
module_file_2 = module_name_2 + ".py"
module_path_2 = os.path.join(current_dir, module_file_2)

# Load the module
spec_2 = importlib.util.spec_from_file_location(module_name_2, module_path_2)
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
        ui.redraw()
        return {'FINISHED'}

class CONTROL_OT_Clear(bpy.types.Operator):
    bl_label = ''
    bl_idname = 'ctp.clear'

    def execute(self, context):
        ui.erase_panels()
        cbt.clear_undrawns()
        CurrentPanelNumber = bpy.context.scene.CurrentPanelNumber
        bpy.context.scene.CurrentPanelNumber = 0
        return {'FINISHED'}


SystemPanels = [CONTROL_OT_SqnAddButton, CONTROL_OT_Clear, CONTROL_PT_Panel, ]


def mod_register():
    for system_class in SystemPanels:
        bpy.utils.register_class(system_class)

def mod_unregister():
    for system_class in SystemPanels:
        bpy.utils.unregister_class(system_class)
