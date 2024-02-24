import importlib.util
import bpy
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the module you want to import
module_name = "cabinet_operations"  # Name of the module you want to import
module_file = module_name + ".py"
module_path = os.path.join(current_dir, module_file)

# Load the module
spec = importlib.util.spec_from_file_location(module_name, module_path)
cbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cbt)


# Panel Creation

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
    draw_panel(multi_item)
    MultiItemPool = bpy.context.scene.MultiItemPool
    child_list = []
    for item in MultiItemPool:
        if item.parent_number == multi_item.panel_number:
            child_list.append(item)
    for child in child_list:
        draw_panel(child)
        if child.generic_type == 'FOLDER':
            display_item(child)


def draw_panel(multi_item):
    
    template_button_name = 'btn.' + str(multi_item.panel_number) + '_' 

    is_child = True if multi_item.parent_id != 'CONTROL_PT_Panel' else False
    is_folder = True if multi_item.generic_type=='FOLDER' else False

    make_button(multi_item.panel_number, 'execute')
    make_button(multi_item.panel_number, 'delete')

    if is_child:
        make_button(multi_item.panel_number, 'swap_up')
        make_button(multi_item.panel_number, 'swamp_down')

    if is_folder:
        make_button(multi_item.panel_number, 'add')
    
    def generic_header(self, context, info):
        layout = self.layout
        layout.prop(info, 'name', text='')
        if is_folder:
            layout.operator(template_button_name + 'add', icon='PLUS')
        if is_child:
            layout.operator(template_button_name + 'swap_up', icon='TRIA_UP')
            layout.operator(template_button_name + 'swap_down', icon='TRIA_DOWN')
        layout.operator(template_button_name + 'execute', text='E')
        layout.operator(template_button_name + 'delete', text='X')
        layout.prop(multi_item, 'is_active', text='')

    match multi_item.mode:

        case 'GRID':

            grid_info = multi_item.GRD[0]

            class GRID_PT_Panel(bpy.types.Panel):
                bl_space_type, bl_region_type, bl_category = 'VIEW_3D', 'UI', 'Dust Panel'
                bl_idname = multi_item.panel_id
                bl_label = ''
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
                bl_label = ''
                bl_parent_id = multi_item.parent_id

                def draw_header(self, context):
                    generic_header(self, context, sequence_info)

                def draw(self, context):
                    layout = self.layout
                    row = layout.row()

            bpy.utils.register_class(SQN_PT_Panel)


    multi_item.is_drawn = True if hasattr(bpy.types, multi_item.panel_id) else False


# Button Creation

def make_button(panel_number: int, function: str):

    if function == 'add':
        make_enum_menu(panel_number)

    class BUTTON_OT_Basic(bpy.types.Operator):

        bl_label = ''
        bl_idname = 'btn.' + str(panel_number) + '_' + function

        def execute(self, context):
            button_operation(panel_number, function)
            return {'FINISHED'}

    bpy.utils.register_class(BUTTON_OT_Basic)

def button_operation(panel_number: int, function:str):

        MultiItemPool = bpy.context.scene.MultiItemPool
        item_in = cbt.get_multi_item(panel_number)

        match function:

            case 'add':
                eval('bpy.ops.object.emen_'+str(panel_number)+'("INVOKE_DEFAULT")')

            case 'execute':
                cbt.execute_item_function(item_in)
            
            case 'delete':
                offspring = cbt.get_heritage(item_in)
                count = len(offspring)
                while count > 0:
                    count-=1
                    item = offspring[count]
                    panel = getattr(bpy.types, item.panel_id, None)
                    if panel is not None:
                        item.is_drawn = False
                        bpy.utils.unregister_class(panel)
                cbt.clear_undrawns()

            case 'swap_up':

                previous_child_position = -1
                reference_position = -1

                for position, item in enumerate(MultiItemPool):
                    if item.panel_number == item_in.panel_number:
                        reference_position = item.panel_number
                        break
                    elif item.parent_number == item_in.parent_number:
                        previous_child_position = position

                if previous_child_position == -1:
                    return {'NO PREVIOUS PANEL'}
                else:
                    MultiItemPool.move(previous_child_position, reference_position)
                    MultiItemPool.move(reference_position - 1, previous_child_position)

                redraw()

            case 'swap_down':
                next_child_position = -1
                reference_position = -1
                panel_found = False

                for position, item in enumerate(MultiItemPool):
                    if item.panel_number == item_in.panel_number and not panel_found:
                        reference_position = item.panel_number
                        panel_found = True
                    elif item.parent_number == item_in.parent_number:
                        next_child_position = position
                        break

                if next_child_position == -1:
                    return {'NO SUBSEQUENT PANEL'}
                else:
                    MultiItemPool.move(next_child_position, reference_position)
                    MultiItemPool.move(reference_position+1, next_child_position)
                
                redraw()

def make_enum_menu(panel_number, is_preset=False):
    items=[]
    if not is_preset:
        items = [
        ("SQN", "Bundle", "A folder for other panels"),
        ("ITN", "Repeater", "Folder for other panels with the option to itterate"),
        ("FNS", "Expression Collection", "Allows access to all offspring folders of the expressions stored inside"),
        ("VAR", "Variable Collection", "Allows access to all offspring folders of the variables stored inside"),
        ("GRD", "Grid", "Creates a grid in space"),
        ("TRF", "Transformation", "Performes a parameterization on selected objects"),
        ("EXE", "Code Execution", "Allows general python code execution"),
        ("FRM", "Manipulate Frames", "Manipulates Playbar"),
        ("MOD", "Blender Modification", "Set and or apply Blender Modifications"),
        ("MAN", "Selection by Name", "Select or duplicate objects by name"),
                ]
    else:
        items = [
            ("SPHERE", "Spheical Parameterization", "Create a Spherical Parameterization"),
        ]

    class ENUM_ET_Menu(bpy.types.Operator):

        bl_idname = "object.emen_" + str(panel_number)
        bl_label = "Create New Panel"
        
        options: bpy.props.EnumProperty(
                               name="Options", 
                               description="Choose a panel to be added", 
                               items=items,
                               )

        def execute(self, context):
            print(self.options)
            cbt.file_panel(cbt.get_multi_item(panel_number), self.options)
            redraw()
            return {'FINISHED'}

        def invoke(self, context, event):
            wm = context.window_manager
            return wm.invoke_props_dialog(self)

    bpy.utils.register_class(ENUM_ET_Menu)