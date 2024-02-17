# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import bpy
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, FloatProperty
import itertools as itt


bl_info = {
    "name" : "Vector Dust",
    "author" : "Frank Dininno",
    "description" : "",
    "blender" : (4, 00, 0),
    "version" : (0, 0, 2),
    "location" : "VIEW_3D",
    "warning" : "",
    "category" : "Dust Panel"
}

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


class StringPropertyGroup(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty()


class IntPropertyGroup(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty()


class SequenceFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='Bundle')


class IterationFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='Repeater')
    loop_variable_name: StringProperty(default='i')
    iterations: IntProperty(default=1)


class VariablesPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Variables')
    variables: CollectionProperty(type=StringPropertyGroup)
    values: CollectionProperty(type=IntPropertyGroup)


class FunctionsPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Functions')
    placeholders: CollectionProperty(type=StringPropertyGroup)
    replacements: CollectionProperty(type=StringPropertyGroup)


class GridMakerPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Grid') # type: ignore
    x_dimension: StringProperty(default='1')
    y_dimension: StringProperty(default='1')
    z_dimension: StringProperty(default='1')
    x_offset: StringProperty(default='0')
    y_offset: StringProperty(default='0')
    z_offset: StringProperty(default='0')
    density: StringProperty(default='0')
    is_hollow: BoolProperty(default=True)


class TransformationPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Transformation')
    x_function: StringProperty()
    timespan: FloatProperty()


class MultiItem(bpy.types.PropertyGroup):
    ITN: CollectionProperty(type=IterationFolder)
    SQN: CollectionProperty(type=SequenceFolder)
    VAR: CollectionProperty(type=VariablesPanel)

    GRD: CollectionProperty(type=GridMakerPanel)
    TRF: CollectionProperty(type=TransformationPanel)

    is_drawn: BoolProperty(default=False)
    is_active: BoolProperty(default=True)
    mode: StringProperty()
    generic_type: StringProperty()
    panel_number: IntProperty()
    parent_number: IntProperty()
    panel_id: StringProperty()
    parent_id: StringProperty(default='CONTROL_PT_Panel')
    
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
    ("OPTION3", "Option 3", "Description for Option 3"),
            ]

    setattr(bpy.types.Scene, 'enum_menu_'+str(panel_number), bpy.props.EnumProperty(
    items=items,
    name="My Enum Property",
    description="Choose an option",
    update=update_enum(panel_number)
            ))

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

def update_enum(panel_number):
    def inner_function(self, context):
        file_panel(get_multi_item(panel_number), getattr(self, 'enum_menu_'+str(panel_number)))
    return inner_function #The returned function is used as the update function

def clear_cabinet():
    erase_panels()
    clear_undrawns()


def get_position(multi_item):
    MultiItemPool = bpy.context.scene.MultiItemPool
    for i, item in enumerate(MultiItemPool):
        if item.panel_number == multi_item.panel_number:
            return i
    return {'NO PANEL FOUND'}

def get_multi_item(panel_number):
    MultiItemPool = bpy.context.scene.MultiItemPool
    for item in MultiItemPool:
        if item.panel_number == panel_number:
            return item
    return {'NO PANEL FOUND'}

def file_panel(parent_item, type):
    bpy.context.scene.CurrentPanelNumber += 1
    CurrentNumber = bpy.context.scene.CurrentPanelNumber
    MultiItemPool = bpy.context.scene.MultiItemPool

    new_item = MultiItemPool.add()

    new_item.mode = type

    if type in {'SQN', 'VAR', 'ITN', 'SEP'}:
        new_item.generic_type = 'FOLDER'
    else:
        new_item.generic_type = 'PANEL'

    new_item.panel_number = CurrentNumber
    new_item.panel_id = 'PANEL_PT_' + str(new_item.panel_number)

    if parent_item is not None:
        new_item.parent_number = parent_item.panel_number
        new_item.parent_id = 'PANEL_PT_' + str(parent_item.panel_number)

    exec('new_item.' + type + '.add()')


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

def clear_undrawns():
    MultiItemPool = bpy.context.scene.MultiItemPool
    count = len(MultiItemPool)
    while count > 0:
        count -= 1
        item = MultiItemPool[count]
        if not item.is_drawn:
            position = get_position(item)
            MultiItemPool.remove(position)

def execute_item_function(multi_item):

    folder_types = ['SQN', 'ITN']

    match multi_item.mode:

        case multi_item.mode if multi_item in folder_types:

            repetitions = 1

            if multi_item.mode == 'ITN':
                repetitions = multi_item.ITN[0].iterations

            for _ in range(repetitions):
                MultiItemPool = bpy.context.scene.MultiItemPool
                child_list = []
                for item in MultiItemPool:
                    if item.parent_number == multi_item.panel_number:
                        child_list.append(item)
                for child in child_list:
                    execute_item_function(child)

def get_children(multi_item, start_index=0):
    MultiItemPool = bpy.context.scene.MultiItemPool
    list = []
    for i in range(start_index, len(MultiItemPool)):
        if MultiItemPool[i].parent_number == multi_item.panel_number:
            list.append(MultiItemPool[i])
    return list


def get_heritage(multi_item):
    list = []
    list.append(multi_item)
    start_pos = get_position(multi_item)
    def loop(in_item, start_position):
        if in_item.generic_type == 'FOLDER':
            child_list = get_children(in_item, start_position)
            if len(child_list)>0:
                for item in child_list:
                    list.append(item)
                    loop(item, get_position(item))
    loop(multi_item, start_pos)
    return list

def draw_item(multi_item):
    
    template_button_name = 'btn.' + str(multi_item.panel_number) + '_' 
    is_child = True if multi_item.parent_id != 'CONTROL_PT_Panel' else False
    make_button(multi_item.panel_number, 'execute')
    make_button(multi_item.panel_number, 'delete')

    if is_child:
        make_button(multi_item, 'swap_up')
        make_button(multi_item, 'swamp_down')
    
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


def display_cabinet():
    MultiItemPool = bpy.context.scene.MultiItemPool
    for item_pointer in MultiItemPool:
        display_item(item_pointer)


def redraw():
    erase_panels()
    display_cabinet()

SystemDataClasses = [
    StringPropertyGroup, IntPropertyGroup,
    GridMakerPanel, TransformationPanel, VariablesPanel, FunctionsPanel,
    SequenceFolder, IterationFolder,
    MultiItem,
]
SystemPanels = [CONTROL_OT_SqnAddButton, CONTROL_OT_Clear, CONTROL_PT_Panel, ]


def registerFileSystem():
    for system_class in itt.chain(SystemDataClasses, SystemPanels):
        bpy.utils.register_class(system_class)
    bpy.types.Scene.MultiItemPool = CollectionProperty(type=MultiItem)
    bpy.types.Scene.CurrentPanelNumber = bpy.props.IntProperty(default=0)


def unregisterFileSystem():
    for system_class in itt.chain(SystemDataClasses, SystemPanels):
        bpy.utils.unregister_class(system_class)
    del bpy.types.Scene.MultiItemPool
    del bpy.types.Scene.CurrentPanelNumber


def register():
    registerFileSystem()


def unregister():
    unregisterFileSystem()

# --init--
# registration
# control_panel
# panel_creation
# ui_operators
# property_groups
# bpy_operations