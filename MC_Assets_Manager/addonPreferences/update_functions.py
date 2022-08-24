import os
import bpy

from ..miscs import utils

def storage_path(self, context):
    path = self.main_props.storage_path
    if path == "":
        bpy.ops.mcam.main_reload()
        bpy.ops.wm.save_userpref()
        return

    from ..miscs.github_dlcs.operators import clear_github_data
    from ..miscs.github_dlcs.auto_check import create_auto_check_thread
    
    clear_github_data()
    create_auto_check_thread()

    dlcs = os.path.join(path, "DLCs")

    o_assets= os.path.join(path, "own_assets")
    o_rigs = os.path.join(path, "own_rigs")
    o_presets = os.path.join(path, "own_presets")

    o_assets_icons = os.path.join(o_assets, "icons")
    o_rigs_icons = os.path.join(o_rigs, "icons")
    o_presets_icons = os.path.join(o_presets, "icons")

    paths = (dlcs, o_assets, o_rigs, o_presets, o_assets_icons, o_rigs_icons, o_presets_icons)

    for p in paths:
        if not os.path.exists(p):
            os.mkdir(p)

    json_path = os.path.join(path, "dlcs.json")
    with open(json_path, 'w') as f:
        f.write('{}')

    paths = bpy.context.preferences.filepaths

    for i, library in enumerate(paths.asset_libraries):
        if library.name == "McAM":
            library.path = utils.AddonPathManagement.getStorageDirPath()
            break

    bpy.ops.mcam.main_reload()
    bpy.ops.wm.save_userpref()