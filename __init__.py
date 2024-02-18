# Note from the bpy extension:
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

import importlib.util
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the module you want to import
module_name = "registration"  # Name of the module you want to import
module_file = module_name + ".py"
module_path = os.path.join(current_dir, module_file)

# Load the module
spec = importlib.util.spec_from_file_location(module_name, module_path)
reg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reg)


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


def register():
    reg.register_all()


def unregister():
    reg.unregister_all()

print('Addon Loaded')

# --init--
# registration
# control_panel
# ui_creatioin
# cabinet_operations
# property_groups
# bpy_operations