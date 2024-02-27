import importlib.util
import os
import bpy

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the module you want to import
module_name_1 = "property_groups"  # Name of the module you want to import
module_file_1 = module_name_1 + ".py"
module_path_1 = os.path.join(current_dir, module_file_1)

# Load the module
spec_1 = importlib.util.spec_from_file_location(module_name_1, module_path_1)
pgps = importlib.util.module_from_spec(spec_1)
spec_1.loader.exec_module(pgps)

module_name_2 = "bpy_operations"  # Name of the module you want to import
module_file_2 = module_name_2 + ".py"
module_path_2 = os.path.join(current_dir, module_file_2)

# Load the module
spec_2 = importlib.util.spec_from_file_location(module_name_2, module_path_2)
bops = importlib.util.module_from_spec(spec_2)
spec_2.loader.exec_module(bops)


def empty_undrawns():
    MultiItemPool = bpy.context.scene.MultiItemPool
    count = len(MultiItemPool)
    while count > 0:
        count -= 1
        item = MultiItemPool[count]
        is_value_present = any(item.panel_number == i.value for i in bpy.context.scene.ErasedPanels)
        if is_value_present:
            position = get_position(item)
            MultiItemPool.remove(position)

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
    return None

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

def get_offspring(multi_item, start_index=0):
    MultiItemPool = bpy.context.scene.MultiItemPool
    list = []
    if multi_item:
        for i in range(start_index, len(MultiItemPool)):
            if MultiItemPool[i].parent_number == multi_item.panel_number:
                list.append(MultiItemPool[i])
    else:
        for i in range(start_index, len(MultiItemPool)):
            if MultiItemPool[i].parent_number == -1:
                list.append(MultiItemPool[i])
    return list

def get_heritage(multi_item, mode='ALL'):
    list = []
    list.append(multi_item)
    start_pos = get_position(multi_item)
    def loop(in_item, start_position):
        if in_item.generic_type == 'FOLDER':
            child_list = get_offspring(in_item, start_position)
            if len(child_list)>0:
                for item in child_list:
                    if mode=='ALL' or in_item.mode==mode:
                        list.append(item)
                    loop(item, get_position(item))
    loop(multi_item, start_pos)
    return list

def get_upfill(multi_item, mode='ALL'):
    list = []
    list.append(get_offspring(multi_item))
    def loop(in_item):
        if in_item.parent_number != -1:
            parent = get_multi_item(in_item.parent_number)
            child_list = get_offspring(parent, get_position(parent))
            if mode=='ALL':
                list.extend(child_list)
            else:
                for item in child_list:
                    if item.mode == mode:
                        list.append(item)
            loop(item, get_position(item))
        else:
            child_list = bpy.context.scene.MultiItemPool
            for item in child_list:
                if mode=='ALL' or item.mode==mode:
                    list.append(item)

    loop(multi_item)
    return list

def count_type(in_list, mode: str):
    count=0
    for item in in_list:
        if item.mode==mode:
            count+=1
    return count

def get_prev_sibling(multi_item):
    MultiItemPool = bpy.context.scene.MultiItemPool
    for position, item in enumerate(MultiItemPool):
        if item.panel_number == multi_item.panel_number:
            return None
        elif item.parent_number == multi_item.parent_number:
            return position
    return None

def get_next_sibling(multi_item):
    MultiItemPool = bpy.context.scene.MultiItemPool
    found_start=False
    for position, item in enumerate(MultiItemPool):
        if item.panel_number == multi_item.panel_number:
            found_start=True
        elif item.parent_number == multi_item.parent_number and found_start:
            return position
    return None