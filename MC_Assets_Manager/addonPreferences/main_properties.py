import bpy
from bpy.props import *

from . import update_functions

class AddonPreferencesProps(bpy.types.PropertyGroup):
    '''
    the property group which stores all 'main' properties
    for the addon : exception --> addon updater
    '''

    #   creates the menu enum (navbar)
    menu : EnumProperty(
        default = "0",
        items = [
            ("0", "Assets", ""),
            ("1", "DLCs", ""),
            ("2", "Online", ""),
            ('3', '', '', 'SETTINGS', 3)
        ])

    #   creates the menu enum (assetsbar)
    assets_menu : EnumProperty(default = "0",
        items = [
            ('0', 'Presets', 'Presets', 'OUTLINER_OB_ARMATURE',0),
            ('1', 'Assets', 'Assets', 'DOCUMENTS',1),
            ('2', 'Rigs', 'Rigs', 'ARMATURE_DATA',2)
        ])

    online_menu : EnumProperty(
        default = "0",
        items = [
            ('0', 'Addon Updater', 'Addon Updater', 'RNA',0),
            ('1', 'Github', 'Github', 'OUTLINER_DATA_VOLUME',1),
        ])

    #   auto check dlc updater
    auto_check_dlc : BoolProperty(
        default=True,
        description="checking automatically for dlc updates every time blender starts"
        )

    #   two UIs : DLCs in the n panel
    two_dlc_ui_panels : BoolProperty(default=False)

    #   reload all while starting blender
    reload_all_during_startup : BoolProperty(default=False)

    #   dlc & file storage path
    storage_path : StringProperty(
        default="",
        subtype="DIR_PATH",
        name="storage path",
        description="This path will be used for the storage of all files and DLCs. If Empty, it will use the defaults internal storage of the addon. When changing the file path the old storage will stil exist. But it will not be used at all. The contents of the old storage will not be copied to the new one! You will have to do that manually. Having the storage on a SSD is recommend since handling everything will be faster than on a HDD",
        update=update_functions.storage_path
        )