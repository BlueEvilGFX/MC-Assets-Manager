import bpy
import importlib

from . import properties
from . import main

def register():
    importlib.reload(main)
    from bpy.utils import register_class
    register_class(properties.AddonPreferencesProps)
    register_class(main.AddonPref)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(main.AddonPref)
    unregister_class(properties.AddonPreferencesProps)