from property_groups import *
from bpy_operations import  *

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

'''def replace_expressions(input_string):
    scene = bpy.context.scene
    while True:
        replaced = False
        for ue, er in zip(scene.universalExpressions.panel_specs, scene.expressionReplacement.panel_specs):
            new_string = input_string.replace(ue.value, er.value)
            if new_string != input_string:
                replaced = True
            input_string = new_string
        if not replaced:
            break
    return input_string'''