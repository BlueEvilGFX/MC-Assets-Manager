import bpy
from bpy.app.handlers import persistent
import importlib, json



#━━━━━━━━━━━━━ Utils

PACKAGE_NAME = __package__

if "utils" in locals():
    importlib.reload(utils)
else:
    from . import utils

#━━━━━━━━━━━━━ Main

if "addonPreferences" in locals():
    importlib.reload(addonPreferences)
else:
    from . import addonPreferences

if "shiftAmenu" in locals():
    importlib.reload(shiftAmenu)
else:
    from . import shiftAmenu

if "ui" in locals():
    importlib.reload(ui)
else:
    from . import ui
 
#━━━━━━━━━━━━━ reg List

mainRegModules = (addonPreferences, shiftAmenu, ui)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@persistent
def load_handler(dummy):
    preferences = utils.AddonPreferencesProperties.getAddonPropAccess()
    if preferences.reload_all_during_startup:
        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
    else:
        utils.AddonReloadManagement.reloadDlcList()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   DLC modules
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def un_registering_dlcs(ure=True):
    '''
    True -> register\n
    False -> unregister
    '''

    mainJson = utils.AddonPathManagement.getDlcMainJson()

    utils.AddonReloadManagement.reloadDlcJson()
    with open(mainJson, "r") as json_file:
        data = json.load(json_file)
        for dlc in data:

            if data[dlc]["active"]:
                init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]

                if init_exists:
                    if dlc in locals():
                        importlib.reload(eval(dlc))
                    else:
                        mod_name = ".files.DLCs.%s" % dlc
                        locals()[dlc] = importlib.import_module(name=mod_name, package=PACKAGE_NAME)

                    if ure:
                        locals()[dlc].register()
                    else:
                        locals()[dlc].unregister()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    utils.register()
    for mod in mainRegModules:
        mod.register()
    un_registering_dlcs()

    bpy.app.handlers.load_post.append(load_handler)
    utils.github_dlcs.auto_check.create_auto_check_thread()

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    un_registering_dlcs(False)
    for mod in reversed(mainRegModules):
        mod.unregister()
    utils.unregister()