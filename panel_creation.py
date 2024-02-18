import importlib.util
import os
import bpy

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the module you want to import
module_name = "ui_operators"  # Name of the module you want to import
module_file = module_name + ".py"
module_path = os.path.join(current_dir, module_file)
# Load the module
spec = importlib.util.spec_from_file_location(module_name, module_path)
ui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui)

def erase_panels():
    MultiItemPool = bpy.context.scene.MultiItemPool
    length = len(MultiItemPool)
    while length > 0:
        length -= 1
        item = MultiItemPool[length]
        panel_class_name = item.panel_id  # replace with your panel class's bl_idname
        if item.is_drawn:
            item.is_drawn = False
            cls = getattr(bpy.types, panel_class_name)
            bpy.utils.unregister_class(cls)

def redraw():
    erase_panels()
    display_cabinet()


def display_cabinet():
    MultiItemPool = bpy.context.scene.MultiItemPool
    for item_pointer in MultiItemPool:
        display_item(item_pointer)


def display_item(multi_item):
    draw_item(multi_item)
    MultiItemPool = bpy.context.scene.MultiItemPool
    child_list = []
    for item in MultiItemPool:
        if item.parent_number == multi_item.panel_number:
            child_list.append(item)
    for child in child_list:
        draw_item(child)
        if child.generic_type == 'FOLDER':
            display_item(child)


def draw_item(multi_item):
    
    template_button_name = 'btn.' + str(multi_item.panel_number) + '_' 
    is_child = True if multi_item.parent_id != 'CONTROL_PT_Panel' else False
    ui.make_button(multi_item.panel_number, 'execute')
    ui.make_button(multi_item.panel_number, 'delete')

    if is_child:
        ui.make_button(multi_item, 'swap_up')
        ui.make_button(multi_item, 'swamp_down')
    
    def generic_header(self, context, info):
        layout = self.layout
        layout.prop(info, 'name', text='')
        if is_child:
            layout.operator(template_button_name + 'swap_down', icon='TRIA_UP')
            layout.operator(template_button_name + 'swap_up', icon='TRIA_DOWN')
        layout.operator(template_button_name + 'execute', text='E')
        layout.operator(template_button_name + 'delete', text='X')
        layout.prop(multi_item, 'is_active', text='')

    match multi_item.mode:

        case 'GRID':

            grid_info = multi_item.GRD

            class GRID_PT_Panel(bpy.types.Panel):
                bl_space_type, bl_region_type, bl_category = 'VIEW_3D', 'UI', 'Dust Panel'
                bl_idname = multi_item.panel_id
                bl_label = bl_idname
                bl_parent_id = multi_item.parent_id
                bl_options = {'DEFAULT_CLOSED'}

                def draw_header(self, context):
                    generic_header(self, context, grid_info)
                    
                def draw(self, context):
                    layout = self.layout
                    row = layout.row()
                    row.prop(grid_info, 'x_offset')
                    row.prop(grid_info, 'x_dimension')
                    row = layout.row()
                    row.prop(grid_info, 'y_offset')
                    row.prop(grid_info, 'y_dimension')
                    row = layout.row()
                    row.prop(grid_info, 'z_offset')
                    row.prop(grid_info, 'z_dimension')
                    layout.prop(grid_info, 'density')
                    layout.prop(grid_info, 'is_hollow')

            bpy.utils.register_class(GRID_PT_Panel)

        case 'SQN':

            sequence_info = multi_item.SQN[0]

            class SQN_PT_Panel(bpy.types.Panel):
                bl_space_type, bl_region_type, bl_category = 'VIEW_3D', 'UI', 'Dust Panel'
                bl_idname = multi_item.panel_id
                bl_label = bl_idname
                bl_parent_id = multi_item.parent_id
                bl_options = {'DEFAULT_CLOSED'}

                def draw_header(self, context):
                    generic_header(self, context, sequence_info)

                def draw(self, context):
                    layout = self.layout

            bpy.utils.register_class(SQN_PT_Panel)


    multi_item.is_drawn = True if hasattr(bpy.types, multi_item.panel_id) else False
