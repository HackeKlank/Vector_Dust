from cabinet_operations import *

def make_button(panel_number: int, function: str):

    class BUTTON_OT_Basic(bpy.types.Operator):

        bl_label = ''
        bl_idname = 'btn.' + str(panel_number) + '_' + function

        def execute(self, context):
            button_operation(panel_number, function)
            return {'FINISHED'}

    bpy.utils.register_class(BUTTON_OT_Basic)

def button_operation(panel_number: int, function:str):

        MultiItemPool = bpy.context.scene.MultiItemPool
        item_in = get_multi_item(panel_number)

        match function:

            case 'execute':
                execute_item_function(item_in)
            
            case 'delete':
                offspring = get_heritage(item_in)
                count = len(offspring)
                while count > 0:
                    count-=1
                    item = offspring[count]
                    panel = getattr(bpy.types, item.panel_id, None)
                    if panel is not None:
                        item.is_drawn = False
                        bpy.utils.unregister_class(panel)
                clear_undrawns()

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

def make_enum_menu(panel_number):

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

    setattr(bpy.types.Scene, 'enum_menu_'+str(panel_number), bpy.props.EnumProperty(
    items=items,
    name="My Enum Property",
    description="Choose an option",
    update=update_enum(panel_number)
            ))
    
def make_enum_preset_menu(panel_number):
    
    items = [
    ("OPTION1", "Sphere Parameterization", "Description for Option 1"),
    ("OPTION2", "Differential Equations Solution", "Description for Option 2"),
    ("OPTION3", "Rotation", "Description for Option 3"),
            ]

    setattr(bpy.types.Scene, 'enum_menu_'+str(panel_number), bpy.props.EnumProperty(
    items=items,
    name="My Enum Property",
    description="Choose an option",
    update=update_enum(panel_number)
            ))

def update_enum(panel_number):
    def inner_function(self, context):
        file_panel(get_multi_item(panel_number), getattr(self, 'enum_menu_'+str(panel_number)))
    return inner_function #The returned function is used as the update function
