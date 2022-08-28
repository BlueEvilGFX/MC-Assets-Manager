import bpy
import os
import bpy.utils.previews

from . import paths


#━━━━━━━━━━━━━━━    constants    ━━━━━━━━━━━━━━━━━━━━━━━━━━
PCOLL_ASSET = "Assets"
PCOLL_PRESET = "Presets"
PCOLL_RIG = "Rigs"
PCOLL_MCAM = "McAM"
PCOLL_DLC = "DLCs"

class ReadIconsIntern:
    """
    class contains lower level reading methods which are used by other functions 
    """

    @staticmethod
    def read_mcam_icons(pcoll) -> None:
        """
        reads the mcam icons into the addon
        """
        dir= paths.RESSOURCES_ICON_DIR
        icons = paths.get_ressources_icons()

        for icon in icons:
            path = os.path.join(dir, icon+".png")
            name = paths.MCAM_ICON + icon
            pcoll.load(name, path, "IMAGE")

    @staticmethod
    def read_dlc_icons(pcoll, asset_type=None, icon_prefix=None) -> None:
        """
        asset_type = None:
            - reads the main icons of the dlcs:
            - name = paths.DLC_MAIN_ICON + name
            - icon_prefix is not needed here

        asset_type = ASSETS | PRESETS | RIGS:
            - loads the asset_type icons of all dlcs
            - set icon_prefix to asset_type:
                - DLC_MAIN_ICON
                - DLC_ASSET_ICON
                - DLC_PRESET_ICON
                - DLC_RIG_ICON 
        """
        dlc_dir = paths.get_dlc_dir()
        dlc_list = paths.get_dlcs()
        for dlc in dlc_list:
            if asset_type is None:
                path = os.path.join(dlc_dir, dlc, "icon.png")
                if os.path.exists(path):
                    name = paths.DLC_MAIN_ICON + name
                    pcoll.load(name, path, "IMAGE")
            else:
                # return since without icon_prefix icons cannot be loaded
                if icon_prefix is None:
                    return

                icon_dir = paths.get_dlc_sub_assets_icon_dir(dlc, asset_type)
                icons = paths.get_dlc_sub_assets_icons(dlc, asset_type)
                for icon in icons:
                    name = icon_prefix + icon
                    path = os.path.join(icon_dir, icon+".png")
                    pcoll.load(name, path, "IMAGE")

    @staticmethod
    def read_user_icon(pcoll, asset_type) -> None:
        """
        reads the asser icons:\n
        real pcoll!
        asset_type: USER_ASSETS | USER_PRESETS | USER_RIGS
        name:user = paths.USER_XXX_ICON + name
        name:dlc  = dlc_name + name ('TheKronisDLC_hammer')
        """
        # read user preset icons
        icon_dir= paths.get_user_sub_icon_dir(asset_type)
        icons = paths.get_user_sub_icons(asset_type)
        for icon in icons:
            path = os.path.join(icon_dir, icon+".png")
            name = paths.USER_PRESET_ICON + icon
            pcoll.load(name, path, "IMAGE")

    @staticmethod
    def reload_icons(pcoll, asset_type=None, icon_prefix=None) -> None:
        """
        pcoll: 
            - PCOLL_ASSET
            - PCOLL_PRESET
            - PCOLL_RIG
            - PCOLL_MCAM
            - PCOLL_DLC

        asset_type: None? --> reads dlc main icons
            - ASSETS
            - PRESETS
            - RIGS

        icon_prefix: only needed when asset_type declared
            - DLC_MAIN_ICON
            - DLC_ASSET_ICON
            - DLC_PRESET_ICON
            - DLC_RIG_ICON\n
        >
        - clears the given pcoll category and reloads it
        - when user icons available: loads them automatically too
        """
        # removes icons
        if pcoll in mcam_icons.values():
            bpy.utils.previews.remove(pcoll)
            for icon in mcam_icons[pcoll]:
                bpy.utils.previews.remove(icon)
            mcam_icons[pcoll] = {}


        # load icons again
        user_dlc = {
            PCOLL_ASSET:paths.USER_ASSETS,
            PCOLL_PRESET:paths.USER_PRESETS,
            PCOLL_RIG:paths.USER_RIGS
            }
        
        pcoll_icons = bpy.utils.previews.new()
        if user_dlc.get(pcoll):
            __class__.read_user_icon(pcoll_icons, user_dlc[pcoll])
        __class__.read_dlc_icons(pcoll)

        mcam_icons[pcoll] = pcoll_icons

#━━━━━━━━━━━━━━━    functions    ━━━━━━━━━━━━━━━━━━━━━━━━━━
def reload_mcam_icons() -> None:
    pcoll = PCOLL_MCAM
    asset_type = None
    icon_prefix = None
    ReadIconsIntern.reload_icons(pcoll, asset_type, icon_prefix)

def reload_dlc_icons() -> None:
    pcoll = PCOLL_DLC
    asset_type = None
    icon_prefix = None
    ReadIconsIntern.reload_icons(pcoll, asset_type, icon_prefix)

def reload_asset_icons() -> None:
    pcoll = PCOLL_ASSET
    asset_type = paths.ASSETS
    icon_prefix = paths.DLC_ASSET_ICON
    ReadIconsIntern.reload_icons(pcoll, asset_type, icon_prefix)

def reload_preset_icons() -> None:
    pcoll = PCOLL_PRESET
    asset_type = paths.PRESETS
    icon_prefix = paths.DLC_PRESET_ICON
    ReadIconsIntern.reload_icons(pcoll, asset_type, icon_prefix)

def reload_rig_icons() -> None:
    pcoll = PCOLL_RIG
    asset_type = paths.RIGS
    icon_prefix = paths.DLC_RIG_ICON
    ReadIconsIntern.reload_icons(pcoll, asset_type, icon_prefix)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

mcam_icons = {}

def register():
    reload_mcam_icons()
    reload_dlc_icons()
    reload_asset_icons()
    reload_preset_icons()
    reload_rig_icons()

def unregister():
    for pcoll in mcam_icons.values():
        bpy.utils.previews.remove(pcoll)
    mcam_icons.clear()