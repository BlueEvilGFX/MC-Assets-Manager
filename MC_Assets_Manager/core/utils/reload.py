import os
import json
import bpy

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

#━━━━━━━━━━━━━━━    reload dlc list    ━━━━━━━━━━━━━━━━━━━━
def reload_dlc_list() -> None:
    """
    reads dlc.json file and reloads the items in the dlc ui list\n
    -> sets all data from the item propertygroup
    """
    dlc_json = paths.get_dlc_json()
    dlc_list = bpy.context.scene.mc_assets_manager_props
    dlc_list.clear()

    with open(dlc_json, 'r') as file:
        data = json.load(file)

        for dlc in data:
            dlc_data = data["dlc"]
            item = dlc_list.add()
            item.name = dlc
            item.type = dlc_data["type"]
            item.creator = dlc_data["creator"]
            item.active = dlc_data["active"]
            item.version = dlc_data["version"]


class ReloadIntern:
    """
    this class contains main methods which are in use by another methods which
    main function is based on the methods inside this class
    """

    @staticmethod
    def load_user_list(ui_list_name, type) -> None:
        """
        loads the user items into the UI list type: USER_ASSETS | USER_PRESETS
        | USER_RIGS
        - it sets the icon path to '$$$' if it exists
        """
        files_list = eval(f'bpy.context.scene.{paths.MCAM_PROP_GROUP}.{ui_list_name}')

        # reload user presets
        user_files = paths.get_user_sub_assets(type)
        user_icons = paths.get_user_sub_icons(type)
        for file in user_files:
            item = files_list.add()
            item.name = file
            if file in user_icons:
                item.path = "$$$"


#━━━━━━━━━━━━━━━    methods    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def reload_asset_list():
    pass

def reload_preset_list():
    pass

def reload_rig_list():
    pass





#━━━━━━━━━━━━━━━    reload preset list    ━━━━━━━━━━━━━━━━━
# def reload_user_list() -> None:
#     """
#     reloads the items in the preset ui list\n
#     - user_presets: if an icon for this preset exists, set the icon property to '$$$'
#     - dlc presets:
#     """
    # preset_list = bpy.context.scene.mc_assets_manager_props

    # reload user presets
    # user_presets = paths.get_user_sub_assets(paths.USER_PRESETS)
    # user_icons = paths.get_user_sub_icons(paths.USER_PRESETS)
    # for preset in user_presets:
        # item = preset_list.add()
        # item.name = preset
        # if preset in user_icons:
        #     item.path = "$$$"

# def reload_dlc_files_list() -> None:
#     #   reload dlc presets
#     dlc_list = paths.get_dlcs()
#     dlc_json = paths.get_dlc_json()
    
#     with open(dlc_json) as file:
#         data = json.load(file)

#         for dlc in dlc_list:
#             presets_dir = paths.get_dlc_sub_files_dir(dlc, paths.PRESETS)
#             if data[dlc]["active"] and presets_dir:
#                 presets = paths.get_dlc_sub_assets(dlc, paths.PRESETS)

                # for preset in presets:
                #     item = preset_list.add()
                #     item.name = os.path.splitext(p)[0]
                #     item.path = os.path.join(presets_dir, preset)
                #     item.icon = dlc + "_" + item.name