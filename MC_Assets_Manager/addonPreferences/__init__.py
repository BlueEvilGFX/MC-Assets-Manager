import bpy, importlib
from . import addonPreferencesClass
from . import openPreferences

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    importlib.reload(addonPreferencesClass)
    bpy.utils.register_class(addonPreferencesClass.AddonPref)
    bpy.utils.register_class(openPreferences.OpenAddonPrefs)
  
def unregister():
    bpy.utils.unregister_class(openPreferences.OpenAddonPrefs)
    bpy.utils.unregister_class(addonPreferencesClass.AddonPref)
    importlib.reload(addonPreferencesClass)

def reload():
    '''reloads the addon preferences'''
    unregister()
    register()