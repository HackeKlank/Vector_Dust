from panel_creation import *


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
        file_panel(None, 'SQN')
        redraw()
        return {'FINISHED'}

class CONTROL_OT_Clear(bpy.types.Operator):
    bl_label = ''
    bl_idname = 'ctp.clear'

    def execute(self, context):
        clear_cabinet()
        return {'FINISHED'}


SystemPanels = [CONTROL_OT_SqnAddButton, CONTROL_OT_Clear, CONTROL_PT_Panel, ]


def register_control_panel():
    for system_class in SystemPanels:
        bpy.utils.register_class(system_class)

def unregister_control_panel():
    for system_class in SystemPanels:
        bpy.utils.unregister_class(system_class)