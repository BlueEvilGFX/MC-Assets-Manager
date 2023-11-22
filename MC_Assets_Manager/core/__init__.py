import os

import bpy
from bpy.app.handlers import persistent

from MC_Assets_Manager.core import (addonpreferences, operators, ui, uilists,
                                    utils)

# paths
resources_dir = utils.paths.PathConstants.RESOURCES_DIRECTORY
asset_types = [utils.paths.AssetTypes.USER_ASSETS, utils.paths.AssetTypes.USER_PRESETS, utils.paths.AssetTypes.USER_RIGS]

paths = [
    utils.paths.McAM.get_github_icon_directory(),
    utils.paths.PathConstants.STORAGE_DIRECTORY,
    utils.paths.DLC.get_directory()
]

# Add user assets & icons paths
paths.extend([utils.paths.User.get_sub_asset_directory(asset_type) for asset_type in asset_types])
paths.extend([utils.paths.User.get_sub_icon_directory(asset_type) for asset_type in asset_types])
    
for path in paths:
    if not os.path.exists(path):
        os.mkdir(path)

# modules
register_modules = [
    operators,
    addonpreferences,
    utils,
    uilists,
    ui
]

@persistent
def load_handler(dummy):
    bpy.ops.mcam.main_reload()
    check = utils.paths.McAM.get_addon_properties().main_props.auto_check_dlc
    if check:
        utils.github_connect.GitHubReader().connect_threaded()

def register():
    for module in register_modules:
        module.register()

    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    for module in reversed(register_modules):
        module.unregister()