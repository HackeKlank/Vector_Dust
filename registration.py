import os
import importlib.util

'''current_dir = os.path.dirname(os.path.abspath(__file__))

def register_all(register=True):
    modules = [
        'property_groups',
        'cabinet_operations',
        'ui_creation',
        'bpy_operations',
        'control_panel',
    ]

    for module in modules:
        module_name = module  # Name of the module you want to import
        module_file = module_name + ".py"
        module_path = os.path.join(current_dir, module_file)

        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        imported = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported)

        # Check and call register or unregister method
        if hasattr(imported, 'register'):
            if register:
                imported.register()
            else:
                # Check for the existence of 'unregister' only if you need to unregister
                if hasattr(imported, 'unregister'):
                    imported.unregister()

'''
current_dir = os.path.dirname(os.path.abspath(__file__))

module_name_1 = "control_panel"  # Name of the module you want to import
module_file_1 = module_name_1 + ".py"
module_path_1 = os.path.join(current_dir, module_file_1)

# Load the module
spec_1 = importlib.util.spec_from_file_location(module_name_1, module_path_1)
cp = importlib.util.module_from_spec(spec_1)
spec_1.loader.exec_module(cp)

module_name_2 = "property_groups"  # Name of the module you want to import
module_file_2 = module_name_2 + ".py"
module_path_2 = os.path.join(current_dir, module_file_2)

# Load the module
spec_2 = importlib.util.spec_from_file_location(module_name_2, module_path_2)
pgps = importlib.util.module_from_spec(spec_2)
spec_2.loader.exec_module(pgps)

def register_all():
    cp.mod_register()
    pgps.mod_unregister()

def unregister_all():
    cp.mod_register()
    pgps.mod_unregister()