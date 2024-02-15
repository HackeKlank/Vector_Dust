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
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

# <editor-fold desc="Control Panel">
class CONTROL_PT_Panel(bpy.types.Panel):
    bl_label = 'Control Panel'
    bl_idname = 'CONTROL_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Dust Panel'

    def draw_header(self, context):
        row = self.layout.row()
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
# </editor-fold>


# <editor-fold desc="Panel Types">
class StringPropertyGroup(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty()


class SequenceFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='Bundle')


class IterationFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='For Loop')
    loop_variable_name: StringProperty(default='i')
    iterations: IntProperty(default=1)


class VariablesFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='Variables')
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
    VAR: CollectionProperty(type=VariablesFolder)

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


# </editor-fold>


# <editor-fold desc="Special Buttons and Functions">
def make_button(multi_item, function: str):

    def button_operation():

        MultiItemPool = bpy.context.scene.MultiItemPool

        match function:

            case 'add_bundle':
                pass

            case 'add_variables':
                pass

            case 'execute':
                execute_item_function(multi_item)

            case 'swap_up':

                previous_child_position = -1
                reference_position = -1

                for position, item in enumerate(MultiItemPool):
                    if item.panel_number == multi_item.panel_number:
                        reference_position = item.panel_number
                        break
                    elif item.parent_number == multi_item.parent_number:
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
                    if item.panel_number == multi_item.panel_number and not panel_found:
                        reference_position = item.panel_number
                        panel_found = True
                    elif item.parent_number == multi_item.parent_number:
                        next_child_position = position
                        break

                if next_child_position == -1:
                    return {'NO SUBSEQUENT PANEL'}
                else:
                    MultiItemPool.move(next_child_position, reference_position)
                    MultiItemPool.move(reference_position+1, next_child_position)

    class BUTTON_OT_Basic(bpy.types.Operator):
        bl_label = ''
        bl_idname = 'btn.' + str(multi_item.panel_number) + '_' + function

        def execute(self, context):
            button_operation()
            return {'FINISHED'}

    bpy.utils.register_class(BUTTON_OT_Basic)

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
                    

# </editor-fold>


# <editor-fold desc="File Operations">


def clear_cabinet():
    erase_panels()
    MultiItemPool = bpy.context.scene.MultiItemPool
    MultiItemPool.clear()


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


# </editor-fold>


# <editor-fold desc="System Displayer">


def draw_item(multi_item):
    
    template_button_name = 'btn.' + str(multi_item.panel_number) + '_' 
    is_child = True if multi_item.parent_id != 'CONTROL_PT_Panel' else False
    make_button(multi_item, 'execute')
    make_button(multi_item, 'delete')

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
                bl_space_type, bl_region_type, bl_category = 'VIEW_3D', 'UI', 'Space Shaper'
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
                bl_space_type, bl_region_type, bl_category = 'VIEW_3D', 'UI', 'Space Shaper'
                bl_idname = multi_item.panel_id
                bl_label = ''
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


# </editor-fold>


# <editor-fold desc="Registration">
SystemDataClasses = [
    StringPropertyGroup,
    GridMakerPanel, TransformationPanel,
    VariablesFolder, SequenceFolder, IterationFolder,
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
# </editor-fold>

