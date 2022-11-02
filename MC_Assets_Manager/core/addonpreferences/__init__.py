import importlib

import bpy

from . import main, properties


def register():
    importlib.reload(main)
    bpy.utils.register_class(properties.AddonPreferencesProps)
    bpy.utils.register_class(main.AddonPref)

def unregister():
    bpy.utils.unregister_class(main.AddonPref)
    bpy.utils.unregister_class(properties.AddonPreferencesProps)

def reload_addon_preferences():
    unregister()
    register()