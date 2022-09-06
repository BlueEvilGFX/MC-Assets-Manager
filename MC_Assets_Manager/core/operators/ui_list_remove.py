import os
import shutil
import zipfile

import bpy
from bpy.props import CollectionProperty, StringProperty
from bpy.types import Operator
from MC_Assets_Manager.core.utils import icons, paths, reload
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UI_LIST_OT_REMOVE(Operator):
    """
    description:
        operator wich removes an item from a list
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """
    bl_idname = "mcam.ui_list_remove"
    bl_label = "remove"

    asset_type : StringProperty()

    def execute(self, context):
        Remover = AssetRemover(self, context, self.asset_type)
        Remover.main()
        reload.reload_asset_list()
        icons.reload_asset_icons()
        self.report({'INFO'}, "asset successully added")
        return{'FINISHED'}


class AssetRemover:
    def __init__(self, context, asset_type):
        self.scene = context.scene
        self.user_asset_type = asset_type
        index = asset_type.split("_")[-1] + "index"
        self.item_index = eval(f"self.scene.mc_assets_manager_props.{index}")
        
    def main():
        pass

# def execute(context, asset_type, list, index):
#     # get path & data
#     path = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", asset_type)
#     files = [file for file in os.listdir(path) if not file == "icons"]
#     file_path = os.path.join(path, files[index])
#     icon_name = os.path.splitext(files[index])[0]+".png"
#     icon_path = os.path.join(path, "icons", icon_name)
#     # remove
#     os.remove(file_path)
#     if os.path.exists(icon_path):
#         os.remove(icon_path)
#     list.remove(index)
#     index = min(max(0, index - 1), len(list) - 1)