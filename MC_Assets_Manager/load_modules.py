import importlib
import json
import bpy

#━━━━━━━━━━━━━ Utils

from .utils import icons

from .utils import github_dlcs

if "properties" in locals():
    importlib.reload(properties)
else:
    from .utils import properties

if "ui_list_presets" in locals():
    importlib.reload(ui_list_presets)
else:
    from .utils import ui_list_presets

if "ui_list_assets" in locals():
    importlib.reload(ui_list_assets)
else:
    from .utils import ui_list_assets

if "ui_list_rigs" in locals():
    importlib.reload(ui_list_rigs)
else:
    from .utils import ui_list_rigs

if "ui_list_dlcs" in locals():
    importlib.reload(ui_list_dlcs)
else:
    from .utils import ui_list_dlcs

if "addonReloader" in locals():
    importlib.reload(addonReloader)
else:
    from .utils import addonReloader

if "utils" in locals():
    importlib.reload(utils)
else:
    from .utils import utils

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

#━━━━━━━━━━━━━ reg Lists

utilRegModules = (icons, properties, ui_list_presets, ui_list_assets,
            ui_list_rigs, ui_list_dlcs, addonReloader, github_dlcs)

mainRegModules = (addonPreferences, shiftAmenu, ui)

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
                        locals()[dlc] = importlib.import_module(name=mod_name, package=__package__)

                    if ure:
                        locals()[dlc].register()
                    else:
                        locals()[dlc].unregister()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    for mod in utilRegModules:
        mod.register()

    for mod in mainRegModules:
        mod.register()

    un_registering_dlcs()

def unregister():
    un_registering_dlcs(False)

    for mod in reversed(mainRegModules):
        mod.unregister()

    for mod in reversed(utilRegModules):
        mod.unregister()