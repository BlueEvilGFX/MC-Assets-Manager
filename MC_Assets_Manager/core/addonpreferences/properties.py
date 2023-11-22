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