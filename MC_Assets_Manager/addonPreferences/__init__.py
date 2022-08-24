import bpy
import importlib

from . import main_properties
from . import addon_preferences_class
from . import open_preferences

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    importlib.reload(addon_preferences_class)
    bpy.utils.register_class(main_properties.AddonPreferencesProps)
    bpy.utils.register_class(addon_preferences_class.AddonPref)
    bpy.utils.register_class(open_preferences.OpenAddonPrefs)
  
def unregister():
    bpy.utils.unregister_class(open_preferences.OpenAddonPrefs)
    bpy.utils.unregister_class(addon_preferences_class.AddonPref)
    bpy.utils.unregister_class(main_properties.AddonPreferencesProps)
    importlib.reload(addon_preferences_class)

def reload():
    '''reloads the addon preferences'''
    unregister()
    register()