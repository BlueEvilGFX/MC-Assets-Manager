import os

import bpy
from bpy.app.handlers import persistent

from MC_Assets_Manager.core import (addonpreferences, operators, ui, uilists,
                                    utils)

# paths
resources_dir = utils.paths.RESOURCES_DIR
paths = [
    utils.paths.get_github_icon_dir(),
    utils.paths.get_storage_dir(),
    utils.paths.get_dlc_dir(),
    # user assets & icons
    utils.paths.get_user_sub_asset_dir(utils.paths.USER_ASSETS),
    utils.paths.get_user_sub_icon_dir(utils.paths.USER_ASSETS),
    utils.paths.get_user_sub_asset_dir(utils.paths.USER_PRESETS),
    utils.paths.get_user_sub_icon_dir(utils.paths.USER_PRESETS),
    utils.paths.get_user_sub_asset_dir(utils.paths.USER_RIGS),
    utils.paths.get_user_sub_icon_dir(utils.paths.USER_RIGS)
]

for path in paths:
    if not os.path.exists(path):
        os.mkdir(path)

# modules
register_modules = [
    addonpreferences,
    utils,
    operators,
    uilists,
    ui
]

@persistent
def load_handler(dummy):
    bpy.ops.mcam.main_reload()
    check = utils.paths.get_addon_properties().main_props.auto_check_dlc
    if check:
        utils.github_connect.check_in_background()

def register():
    for module in register_modules:
        module.register()

    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    for module in reversed(register_modules):
        module.unregister()