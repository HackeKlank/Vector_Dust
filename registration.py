import importlib.util
import os

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
    cp.register_control_panel()
    pgps.register_property_groups()

def unregister_all():
    cp.unregister_control_panel()
    pgps.unregister_property_groups()