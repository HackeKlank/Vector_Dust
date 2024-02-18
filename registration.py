import importlib.util

file_path_1 = 'C:/Users/frank/AppData/Roaming/Blender Foundation/Blender/4.0/scripts/addons/Vector_Dust/control_panel.py'

# Load the module
spec_1 = importlib.util.spec_from_file_location("control_panel", file_path_1)
cp = importlib.util.module_from_spec(spec_1)
spec_1.loader.exec_module(cp)

file_path_2 = 'C:/Users/frank/AppData/Roaming/Blender Foundation/Blender/4.0/scripts/addons/Vector_Dust/property_groups.py'

# Load the module
spec_2 = importlib.util.spec_from_file_location("property_groups", file_path_2)
pgps = importlib.util.module_from_spec(spec_2)
spec_2.loader.exec_module(pgps)

def register_all():
    cp.register_control_panel()
    pgps.register_property_groups()

def unregister_all():
    cp.unregister_control_panel()
    pgps.unregister_property_groups()
    