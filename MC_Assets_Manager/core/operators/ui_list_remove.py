import os

import bpy
from bpy.props import StringProperty
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
        Remover = AssetRemover(context, self.asset_type)
        Remover.main()
        return{'FINISHED'}


class AssetRemover:

    list_dictionary = {
        paths.USER_ASSETS : [
            paths.UI_LIST_ASSETS,
            paths.ASSETS
            ],
        paths.USER_PRESETS :[
            paths.UI_LIST_PRESETS,
            paths.PRESETS
            ],
        paths.USER_RIGS : [
            paths.UI_LIST_RIGS,
            paths.RIGS
            ]
    }

    def __init__(self, context, asset_type):
        self.scene = context.scene
        self.user_asset_type = asset_type
        index = asset_type.split("_")[-1][:-1] + "_index"
        self.item_index = eval(f"self.scene.mc_assets_manager_props.{index}")
        
    def main(self):
        asset_dir = paths.get_user_sub_asset_dir(self.user_asset_type)
        icon_dir = paths.get_user_sub_icon_dir(self.user_asset_type)
        scene = "bpy.context.scene"
        asset_list = eval('.'.join([
            scene,
            paths.MCAM_PROP_GROUP,
            self.list_dictionary[self.user_asset_type][0]
            ]))

        item = asset_list[self.item_index]
        name = item.name
        icon = name
        collection = item.collection

        if collection:
            name = name + "&&" + collection

        asset_path = os.path.join(asset_dir, name) + ".blend"
        icon_path = os.path.join(icon_dir, icon) + ".png"

        if os.path.exists(asset_path):
            os.remove(asset_path)

        if os.path.exists(icon_path):
            os.remove(icon_path)

        asset_type = self.list_dictionary[self.user_asset_type][1]
        bpy.ops.mcam.ui_list_reload(asset_type=asset_type)