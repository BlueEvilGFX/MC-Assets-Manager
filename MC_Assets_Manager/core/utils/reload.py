import json
import os

# DO NOT REMOVE BPY -> EVAL USAGE
import bpy

from .. import addonpreferences
from . import paths


#━━━━━━━━━━━━━━━    reload dlc json    ━━━━━━━━━━━━━━━━━━━━
def reload_dlc_json() -> None:
    """
    reloads the dlc main json file which stores all dlc data:
    - gets all installed dlcs from the dlc dir
    - reads every single data.json file
    - writes the data to the dlc.json file
    - sets the active status: if dlc new: set to True else set to stored state
    """
    dlc_json = paths.get_dlc_json()
    dlc_list = paths.get_dlcs()
    dlc_dict = {}

    with open(dlc_json, 'r') as file:
        data = json.load(file)

        for dlc in dlc_list:
            # sets the active status of the dlc accordingly:
            # new -> True else  -> use stored
            dlc_sub_json = paths.get_dlc_sub_json(dlc)
            with open(dlc_sub_json, 'r') as sub_file:
                dlc_dict[dlc] = json.load(sub_file)
                dlc_dict[dlc]["active"] = True if data.get("dlc") is None\
                                                else data[dlc]["active"]
    
    with open(dlc_json, "w") as file:
        json.dump(dlc_dict, file, indent=4)

#━━━━━━━━━━━━━━━    reload dlc list    ━━━━━━━━━━━━━━━━━━━━
def reload_dlc_list() -> None:
    """
    reads dlc.json file and reloads the items in the dlc ui list\n
    -> sets all data from the item propertygroup
    """
    dlc_json = paths.get_dlc_json()
    dlc_list = eval("bpy.context.scene.mc_assets_manager_props."+paths.UI_LIST_DLCS)
    dlc_list.clear()

    with open(dlc_json, 'r') as file:
        data = json.load(file)

        for dlc in data:
            dlc_data = data[dlc]
            item = dlc_list.add()
            item.name = dlc
            item.type = dlc_data["type"]
            item.creator = dlc_data["creator"]
            item.active = dlc_data["active"]
            item.version = dlc_data["version"]
            icon_path = os.path.join(paths.get_dlc_dir(), dlc, "icon.png")
            item.icon = os.path.exists(icon_path)


class ReloadIntern:
    """
    this class contains main methods which are in use by another methods which
    main function is based on the methods inside this class
    """

    @staticmethod
    def clear_list(ui_list) -> None:
        ui_list.clear()

    @staticmethod
    def load_user_files(ui_list, asset_type) -> None:
        """
        - ui_list: the ui list to which items will be added
        - UI list asset_type: USER_ASSETS | USER_PRESETS | USER_RIGS
        - loads the user items into the list
        - checks for collection restrictions: unimportant for assets
        - it sets the icon property to the corresponding id
        """
        user_files = paths.get_user_sub_assets(asset_type)
        user_icons = paths.get_user_sub_icons(asset_type)

        for file in user_files:
            item = ui_list.add()
            if "&&" in file:
                item.name, item.collection = file.split("&&")
            else:
                item.name = file

            if file in user_icons:
                item.icon = asset_type + ':'+ item.name

    @staticmethod
    def load_dlc_files(ui_list, asset_type):
        """
        - ui_list_name: UI_LIST_ASSETS | UI_LIST_PRESETS | UI_LIST_RIGS
        - UI list asset_type: ASSETS | PRESETS | RIGS
        - loads the dlc items into the list
        - it sets the icon property to the corresponding id
        """
        # filtering assets because they are read from the json file
        if asset_type == paths.ASSETS:
            __class__.load_dlc_assets(ui_list)
        else:
            __class__.load_dlc_presets_rigs(ui_list, asset_type)

    @staticmethod
    def load_dlc_assets(ui_list):
        """
        - loads the assets of the dlcs into the ui list
        - it sets the icon property to the corresponding id
        """
        asset_type = paths.ASSETS
        with open(paths.get_dlc_json(), 'r') as file:
            data = json.load(file)

        for dlc in paths.get_dlcs():
            asset_dir = paths.get_dlc_sub_assets_dir(dlc, asset_type)

            try:
                if not data[dlc]["active"] or not asset_dir:
                    return
            except:
                continue

            assets_json = paths.get_dlc_sub_assets_json(dlc, asset_type)
            assets_blend = paths.get_dlc_sub_assets_blend(dlc, asset_type)
            asset_icons = paths.get_dlc_sub_assets_icons(dlc, asset_type)

            if not assets_json or not assets_blend: continue

            with open(assets_json, 'r') as asset_file:
                asset_data = json.load(asset_file)

            for asset in asset_data:
                asset_sub_data = asset_data[asset]
                item = ui_list.add()
                item.name = asset
                item.type = asset_sub_data["type"]
                item.category = asset_sub_data["category"]
                item.dlc = dlc
                if asset in asset_icons:
                    item.icon = paths.DLC_ASSET_ICON\
                        + ':' + dlc\
                        + ':'+ item.name

    @staticmethod
    def load_dlc_presets_rigs(ui_list, asset_type):
        """
        - asset_type: ASSETS | PRESETS | RIGS -> returns a list
        - loads the rigs/presets of the dlcs into the ui list
        - it sets the icon property to the corresponding id
        """
        # dictionary to get corresponding user asses
        user_dlc = {
            paths.PRESETS : paths.DLC_PRESET_ICON,
            paths.RIGS : paths.DLC_RIG_ICON,
            }

        with open(paths.get_dlc_json(), 'r') as file:
            data = json.load(file)

        for dlc in paths.get_dlcs():
            asset_dir = paths.get_dlc_sub_assets_dir(dlc, asset_type)

            if not data[dlc]["active"] or not asset_dir: continue
            
            assets = paths.get_dlc_sub_assets(dlc, asset_type)
            asset_icons = paths.get_dlc_sub_assets_icons(dlc, asset_type)

            for asset in assets:
                item = ui_list.add()
                if "&&" in asset:
                    item.name, item.collection = asset.split("&&")
                else:
                    item.name = asset

                item.dlc = dlc
                if item.name in asset_icons:
                    item.icon = user_dlc[asset_type]\
                        + ':' + dlc\
                        + ':'+ item.name


#━━━━━━━━━━━━━━━    methods    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def reload_asset_list():
    """
    reloads the whole asset list
    """
    scene = "bpy.context.scene"
    asset_list = eval('.'.join([scene, paths.MCAM_PROP_GROUP, paths.UI_LIST_ASSETS]))
    ReloadIntern.clear_list(asset_list)
    ReloadIntern.load_dlc_files(asset_list, paths.ASSETS)
    ReloadIntern.load_user_files(asset_list, paths.USER_ASSETS)

def reload_preset_list():
    """
    reloads the whole preset list
    """
    scene = "bpy.context.scene"
    preset_list = eval('.'.join([scene, paths.MCAM_PROP_GROUP, paths.UI_LIST_PRESETS]))
    ReloadIntern.clear_list(preset_list)
    ReloadIntern.load_dlc_files(preset_list, paths.PRESETS)
    ReloadIntern.load_user_files(preset_list, paths.USER_PRESETS)

def reload_rig_list():
    """
    reloads the whole rig list
    """
    scene = "bpy.context.scene"
    rig_list = eval('.'.join([scene, paths.MCAM_PROP_GROUP, paths.UI_LIST_RIGS]))
    ReloadIntern.clear_list(rig_list)
    ReloadIntern.load_dlc_files(rig_list, paths.RIGS)
    ReloadIntern.load_user_files(rig_list, paths.USER_RIGS)

def reload_addon_preferences():
    addonpreferences.unregister()
    addonpreferences.register()