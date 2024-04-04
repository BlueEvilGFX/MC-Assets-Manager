import json
import os
import bpy

from MC_Assets_Manager.core.utils import paths
from MC_Assets_Manager.core import addonpreferences


#━━━━━━━━━━━━━━━    reload dlc json    ━━━━━━━━━━━━━━━━━━━━
def reload_dlc_json() -> None:
    """
    reloads the dlc main json file which stores all dlc data:
    - gets all installed dlcs from the dlc dir
    - reads every single data.json file
    - writes the data to the dlc.json file
    - sets the active status: if dlc new: set to True else set to stored state
    """
    dlc_json = paths.McAM.get_dlc_main_json()
    dlc_list = paths.DLC.get_dlcs_list()
    dlc_dict = {}

    with open(dlc_json, 'r') as file:
        data = json.load(file)

        for dlc in dlc_list:
            # sets the active status of the dlc accordingly:
            # new -> True else  -> use stored
            dlc_sub_json = paths.DLC.get_sub_json(dlc)
            with open(dlc_sub_json, 'r') as sub_file:
                dlc_dict[dlc] = json.load(sub_file)
                dlc_dict[dlc]["active"] = True if data.get(dlc) is None\
                                                else data[dlc]["active"]
    
    with open(dlc_json, "w") as file:
        json.dump(dlc_dict, file, indent=4)

#━━━━━━━━━━━━━━━    reload dlc list    ━━━━━━━━━━━━━━━━━━━━
def reload_dlc_list() -> None:
    """
    reads dlc.json file and reloads the items in the dlc ui list\n
    -> sets all data from the item propertygroup
    """
    reload_dlc_json()
    dlc_json = paths.McAM.get_dlc_main_json()
    dlc_list = getattr(bpy.context.scene.mc_assets_manager_props, paths.PropertyGroups.UI_LIST_DLCS)
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
            item.ui = dlc_data.get("ui", True)
            item.version = dlc_data["version"]
            icon_path = os.path.join(paths.DLC.get_directory(), dlc, "icon.png")
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

        # add stored files
        user_files = paths.User.get_sub_asset_list(asset_type)
        user_icons = paths.User.get_sub_icon_list(asset_type)

        for file in user_files:
            item = ui_list.add()
            if "&&" in file:
                item.name, item.collection = file.split("&&")
            else:
                item.name = file

            if file in user_icons:
                item.icon = asset_type + ':'+ item.name
        
        # add linked files
        json_file = paths.User.get_links_json()
        with open(json_file, "r") as file:
            data = json.load(file) 
        
        invalid_links = False
        for asset in data[asset_type]:
            # invalid path -> remove
            if not os.path.exists(asset):
                invalid_links = True
                data[asset_type].remove(asset)
            item = ui_list.add()
            item.link = asset # filepath
            asset = os.path.splitext(asset)[0] # remove .blend extension
            if "&&" in asset:
                item.name, item.collection = os.path.basename(asset).split("&&")
            else:
                item.name = os.path.basename(asset)

        # if invalid links detectedm push changes
        if invalid_links:
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)

                
    @staticmethod
    def load_dlc_files(ui_list, asset_type):
        """
        - ui_list_name: UI_LIST_ASSETS | UI_LIST_PRESETS | UI_LIST_RIGS
        - UI list asset_type: ASSETS | PRESETS | RIGS
        - loads the dlc items into the list
        - it sets the icon property to the corresponding id
        """
        # filtering assets because they are read from the json file
        if asset_type == paths.AssetTypes.ASSETS:
            __class__.load_dlc_assets(ui_list)
        else:
            __class__.load_dlc_presets_rigs(ui_list, asset_type)

    @staticmethod
    def load_dlc_assets(ui_list):
        """
        - loads the assets of the dlcs into the ui list
        - it sets the icon property to the corresponding id
        """
        asset_type = paths.AssetTypes.ASSETS
        with open(paths.McAM.get_dlc_main_json(), 'r') as file:
            data = json.load(file)

        for dlc in paths.DLC.get_dlcs_list():
            asset_dir = paths.DLC.get_sub_asset_directory(dlc, asset_type)

            try:
                if not data[dlc]["active"] or not asset_dir:
                    continue
            except:
                continue

            assets_json = paths.DLC.get_sub_asset_json(dlc, asset_type)
            assets_blend = paths.DLC.get_sub_asset_blend(dlc, asset_type)
            asset_icons = paths.DLC.get_sub_icon_list(dlc, asset_type)

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
                    item.icon = paths.IconTypes.DLC_ASSET_ICON\
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
            paths.AssetTypes.PRESETS : paths.IconTypes.DLC_PRESET_ICON,
            paths.AssetTypes.RIGS : paths.IconTypes.DLC_RIG_ICON,
            }

        with open(paths.McAM.get_dlc_main_json(), 'r') as file:
            data = json.load(file)

        for dlc in paths.DLC.get_dlcs_list():
            asset_dir = paths.DLC.get_sub_asset_directory(dlc, asset_type)

            if not data[dlc]["active"] or not asset_dir: continue
            
            assets = paths.DLC.get_sub_asset_list(dlc, asset_type)
            asset_icons = paths.DLC.get_sub_icon_list(dlc, asset_type)

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
    prop_group = getattr(bpy.context.scene, paths.PropertyGroups.MCAM_PROP_GROUP)
    asset_list = getattr(prop_group, paths.PropertyGroups.UI_LIST_ASSETS)
    ReloadIntern.clear_list(asset_list)
    ReloadIntern.load_dlc_files(asset_list, paths.AssetTypes.ASSETS)
    ReloadIntern.load_user_files(asset_list, paths.AssetTypes.USER_ASSETS)

def reload_preset_list():
    prop_group = getattr(bpy.context.scene, paths.PropertyGroups.MCAM_PROP_GROUP)
    preset_list = getattr(prop_group, paths.PropertyGroups.UI_LIST_PRESETS)
    ReloadIntern.clear_list(preset_list)
    ReloadIntern.load_dlc_files(preset_list, paths.AssetTypes.PRESETS)
    ReloadIntern.load_user_files(preset_list, paths.AssetTypes.USER_PRESETS)

def reload_rig_list():
    prop_group = getattr(bpy.context.scene, paths.PropertyGroups.MCAM_PROP_GROUP)
    rig_list = getattr(prop_group, paths.PropertyGroups.UI_LIST_RIGS)
    ReloadIntern.clear_list(rig_list)
    ReloadIntern.load_dlc_files(rig_list, paths.AssetTypes.RIGS)
    ReloadIntern.load_user_files(rig_list, paths.AssetTypes.USER_RIGS)

def reload_addon_preferences():
    addonpreferences.unregister()
    addonpreferences.register()