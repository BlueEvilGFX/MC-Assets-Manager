import bpy
from bpy.props import *

class AddonPreferencesProps(bpy.types.PropertyGroup):
    '''
    the property group which stores all 'main' properties
    for the addon preferences : exception --> addon updater
    '''

    #   creates the menu enum (navbar)
    menu : EnumProperty(
        default = "Assets",
        items = [
            ("Assets", "Assets", "Assets"),
            ("DLCs", "DLCs", "DLCs"),
            ("Online", "Online", "Online"),
            ("Settings", "", "", "SETTINGS", 3)
        ])

    #   creates the menu enum (assetsbar)
    assets_menu : EnumProperty(default = "Presets",
        items = [
            ('Assets', 'Assets', 'Assets', 'DOCUMENTS',0),
            ('Presets', 'Presets', 'Presets', 'OUTLINER_OB_ARMATURE',1),
            ('Rigs', 'Rigs', 'Rigs', 'ARMATURE_DATA',2)
        ])

    online_menu : EnumProperty(
        default = "Addon Updater",
        items = [
            ('Addon Updater', 'Addon Updater', 'Addon Updater', 'RNA',0),
            ('Github', 'Github', 'Github', 'OUTLINER_DATA_VOLUME',1),
        ])

    #   auto check dlc updater
    auto_check_dlc : BoolProperty(
        default=True,
        description="checking automatically for dlc updates every time blender starts"
        )

    #   two UIs : DLCs in the n panel
    two_dlc_ui_panels : BoolProperty()

    #   dlc & file storage path
    storage_path : StringProperty(
        subtype="DIR_PATH",
        name="storage path",
        description="This path will be used for the storage of all files and DLCs. If Empty, it will use the defaults internal storage of the addon. When changing the file path the old storage will stil exist. But it will not be used at all. The contents of the old storage will not be copied to the new one! You will have to do that manually. Having the storage on a SSD is recommend since handling everything will be faster than on a HDD",
        # update=storage_path
        )

# def storage_path(self, context):
#     path = self.main_props.storage_path
#     if path == "":
#         bpy.ops.mcam.main_reload()
#         bpy.ops.wm.save_userpref()
#         return

#     from ..miscs.github_dlcs.operators import clear_github_data
#     from ..miscs.github_dlcs.check_in_background import create_auto_check_thread
    
#     clear_github_data()
#     create_auto_check_thread()

#     dlcs = os.path.join(path, "DLCs")

#     o_assets= os.path.join(path, "own_assets")
#     o_rigs = os.path.join(path, "own_rigs")
#     o_presets = os.path.join(path, "own_presets")

#     o_assets_icons = os.path.join(o_assets, "icons")
#     o_rigs_icons = os.path.join(o_rigs, "icons")
#     o_presets_icons = os.path.join(o_presets, "icons")

#     paths = (dlcs, o_assets, o_rigs, o_presets, o_assets_icons, o_rigs_icons, o_presets_icons)

#     for p in paths:
#         if not os.path.exists(p):
#             os.mkdir(p)

#     json_path = os.path.join(path, "dlcs.json")
#     with open(json_path, 'w') as f:
#         f.write('{}')

#     paths = bpy.context.preferences.filepaths

#     for i, library in enumerate(paths.asset_libraries):
#         if library.name == "McAM":
#             library.path = utils.AddonPathManagement.getStorageDirPath()
#             break

#     bpy.ops.mcam.main_reload()
#     bpy.ops.wm.save_userpref()