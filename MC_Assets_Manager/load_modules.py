import bpy
from bpy.app.handlers import persistent
import importlib, json

PACKAGE_NAME = __package__

#━━━━━━━━━━━━━ Main

if "addonPreferences" in locals():
    importlib.reload(addonPreferences)
else:
    from . import addonPreferences

if "miscs" in locals():
    importlib.reload(miscs)
else:
    from . import miscs

if "ui_lists" in locals():
    importlib.reload(ui_lists)
else:
    from . import ui_lists

if "asset_browser" in locals():
    importlib.reload(asset_browser)
else:
    from . import asset_browser

if "ui" in locals():
    importlib.reload(ui)
else:
    from . import ui
 
#━━━━━━━━━━━━━ reg List

mainRegModules = (miscs, addonPreferences, ui_lists, asset_browser, ui)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@persistent
def load_handler(dummy):
    preferences = miscs.AddonPreferencesProperties.getAddonPropAccess()
    if preferences.main_props.reload_all_during_startup:
        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
    else:
        miscs.AddonReloadManagement.reloadDlcList()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   DLC modules
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def un_registering_dlcs(ure=True):
    '''
    True -> register\n
    False -> unregister
    '''

    mainJson = miscs.AddonPathManagement.getDlcMainJson()

    miscs.AddonReloadManagement.reloadDlcJson()
    with open(mainJson, "r") as json_file:
        data = json.load(json_file)
        for dlc in data:

            if data[dlc]["active"]:
                init_exists = miscs.AddonPathManagement.getDLCInitPath(dlc)[1]

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
    for mod in mainRegModules:
        mod.register()
    un_registering_dlcs()

    bpy.app.handlers.load_post.append(load_handler)
    miscs.github_dlcs.auto_check.create_auto_check_thread()

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    un_registering_dlcs(False)
    for mod in reversed(mainRegModules):
        mod.unregister()