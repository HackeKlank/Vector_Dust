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

file_path = 'C:/Users/frank/AppData/Roaming/Blender Foundation/Blender/4.0/scripts/addons/Vector_Dust/registration.py'

# Load the module
spec = importlib.util.spec_from_file_location("registration", file_path)
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

# --init--
# registration
# control_panel
# panel_creation
# ui_operators
# cabinet_operations
# property_groups
# bpy_operations