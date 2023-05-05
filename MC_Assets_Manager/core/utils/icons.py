import os

import bpy
import bpy.utils.previews

from . import paths

#━━━━━━━━━━━━━━━    description    ━━━━━━━━━━━━━━━━━━━━━━━━
"""
This py file can load every icon of user and dlc assets.
To access the icon do following:

    for dlc main icons:
        pcoll = icons.mcam_icons[icons.PCOLL_DLC_ID]
        custom_icon = pcoll[item.name].icon_id

    for preset icons:
        pcoll = icons.mcam_icons[icons.PCOLL_PRESET_ID]
        custom_icon = pcoll[item.icon].icon_id
"""

#━━━━━━━━━━━━━━━    constants    ━━━━━━━━━━━━━━━━━━━━━━━━━━
PCOLL_ASSET_ID = "Assets"
PCOLL_PRESET_ID = "Presets"
PCOLL_RIG_ID = "Rigs"
PCOLL_MCAM_ID = "McAM"
PCOLL_DLC_ID = "DLCs"
PCOLL_GITHUB_DLC_ID = "GitHubDLCs"

class IconReader:
    """
    class contains lower level reading methods which are used by other functions 
    """

    @staticmethod
    def read_mcam_icons(pcoll) -> None:
        """
        description:
            - real pcoll!
            - the mcam main icons into the addon
            - it uses the resources/icons path for it
        """
        dir = paths.RESOURCES_ICON_DIR
        icons = paths.get_resources_icons()

        for icon in icons:
            path = os.path.join(dir, icon+".png")
            pcoll.load(icon, path, "IMAGE")

    @staticmethod
    def read_dlc_icons(pcoll, asset_type=None, icon_prefix=None) -> None:
        """
        args:
            pcoll: real pcoll reference to blenders api
            asset_type: enum of
                ASSETS | PRESETS | RIGS
                , default = None
            icon_prefix: enum of
                DLC_MAIN_ICON | DLC_ASSET_ICON |
                DLC_PRESET_ICON | DLC_RIG_ICON
                , default = None
        
        description:
            - reads the main icons of the dlcs:
            - if asset_type is set to None --> loads the main dlc icons
        """
        dlc_dir = paths.get_dlc_dir()
        dlc_list = paths.get_dlcs()
        for dlc in dlc_list:
            if asset_type is None:
                path = os.path.join(dlc_dir, dlc, "icon.png")
                if os.path.exists(path):
                    pcoll.load(dlc, path, "IMAGE")
            else:
                # return since without icon_prefix icons cannot be loaded
                if icon_prefix is None:
                    return

                icon_dir = paths.get_dlc_sub_assets_icon_dir(dlc, asset_type)
                icons = paths.get_dlc_sub_assets_icons(dlc, asset_type)
                for icon in icons:
                    path = os.path.join(icon_dir, icon+".png")
                    name = icon_prefix + ':' + dlc + ':' + icon
                    pcoll.load(name, path, "IMAGE")

    @staticmethod
    def read_user_icon(pcoll, asset_type) -> None:
        """
        reads the asser icons:\n
        real pcoll!
        asset_type: USER_ASSETS | USER_PRESETS | USER_RIGS
        name:user = paths.USER_XXX_ICON + name
        """
        # read user preset icons
        icon_dir= paths.get_user_sub_icon_dir(asset_type)
        icons = paths.get_user_sub_icons(asset_type)
        for icon in icons:
            path = os.path.join(icon_dir, icon+".png")
            name = asset_type + ':' + icon
            pcoll.load(name, path, "IMAGE")

    @staticmethod
    def read_github_dlc_icons(pcoll) -> None:
        """
        reads the github dlc icons
        """
        icon_dir = paths.get_github_icon_dir()
        icons = os.listdir(icon_dir) # lists icons with extension
        for icon in icons:
            path = os.path.join(icon_dir, icon)
            name = os.path.splitext(icon)[0]
            pcoll.load(name, path, "IMAGE")

    @staticmethod
    def reload_icons(pcoll_id, asset_type=None, icon_prefix=None) -> None:
        """
        args:
            pcoll_id: enum of
                PCOLL_ASSET_ID | PCOLL_PRESET_ID | PCOLL_RIG_ID | PCOLL_MCAM_I
                | PCOLL_DLC_ID | PCOLL_GITHUB_DLC_ID
            asset_type: 
                ASSETS | PRESETS | RIGS
                , default = None

            icon_prefix: only needed when asset_type declared
                DLC_MAIN_ICON | DLC_ASSET_ICON | DLC_PRESET_ICON | DLC_RIG_ICON
                , default = None
         
        description:
            - clears the given pcoll category and reloads it
            - when user icons available: loads them automatically too
        """
        # clears icons from pcoll
        if pcoll_id in mcam_icons.keys():
            pcoll = mcam_icons[pcoll_id]
            bpy.utils.previews.remove(pcoll)

        pcoll = bpy.utils.previews.new()

        if pcoll_id == PCOLL_MCAM_ID:
            __class__.read_mcam_icons(pcoll)
        elif pcoll_id == PCOLL_GITHUB_DLC_ID:
            __class__.read_github_dlc_icons(pcoll)
        else:
            # dictionary to get corresponding user asses
            user_dlc = {
                PCOLL_ASSET_ID : paths.USER_ASSETS,
                PCOLL_PRESET_ID : paths.USER_PRESETS,
                PCOLL_RIG_ID : paths.USER_RIGS
                }
            
            # load user and dlc icons
            if user_dlc.get(pcoll_id):
                __class__.read_user_icon(pcoll, user_dlc[pcoll_id])
            __class__.read_dlc_icons(pcoll, asset_type, icon_prefix)

        mcam_icons[pcoll_id] = pcoll

#━━━━━━━━━━━━━━━    functions    ━━━━━━━━━━━━━━━━━━━━━━━━━━
def reload_mcam_icons() -> None:
    pcoll_id = PCOLL_MCAM_ID
    asset_type = None
    icon_prefix = None
    IconReader.reload_icons(pcoll_id, asset_type, icon_prefix)

def reload_dlc_icons() -> None:
    pcoll_id = PCOLL_DLC_ID
    asset_type = None
    icon_prefix = None
    IconReader.reload_icons(pcoll_id, asset_type, icon_prefix)

def reload_asset_icons() -> None:
    pcoll_id = PCOLL_ASSET_ID
    asset_type = paths.ASSETS
    icon_prefix = paths.DLC_ASSET_ICON
    IconReader.reload_icons(pcoll_id, asset_type, icon_prefix)

def reload_preset_icons() -> None:
    pcoll_id = PCOLL_PRESET_ID
    asset_type = paths.PRESETS
    icon_prefix = paths.DLC_PRESET_ICON
    IconReader.reload_icons(pcoll_id, asset_type, icon_prefix)

def reload_rig_icons() -> None:
    pcoll_id = PCOLL_RIG_ID
    asset_type = paths.RIGS
    icon_prefix = paths.DLC_RIG_ICON
    IconReader.reload_icons(pcoll_id, asset_type, icon_prefix)

def reload_github_dlc_icons() -> None:
    pcoll_id = PCOLL_GITHUB_DLC_ID
    IconReader.reload_icons(pcoll_id)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

mcam_icons = {}

def register():
    reload_mcam_icons()
    reload_dlc_icons()

def unregister():
    for pcoll in mcam_icons.values():
        bpy.utils.previews.remove(pcoll)
    mcam_icons.clear()