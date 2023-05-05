import os

import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from MC_Assets_Manager.core.utils import paths, asset_dict

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
        self.scene = context.scene
        index = self.asset_type.split("_")[-1][:-1] + "_index"
        item_index = eval(f"self.scene.mc_assets_manager_props.{index}")

        asset_dir = paths.get_user_sub_asset_dir(self.asset_type)
        icon_dir = paths.get_user_sub_icon_dir(self.asset_type)
        scene = "bpy.context.scene"
        asset_list = eval('.'.join([
            scene,
            paths.MCAM_PROP_GROUP,
            asset_dict.get_asset_types(
                self.asset_type,
                asset_dict.Selection.ui_list
                )
            ]))

        item = asset_list[item_index]
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

        asset_type = asset_dict.get_asset_types(
            self.asset_type,
            asset_dict.Selection.raw_type
            )
        bpy.ops.mcam.ui_list_reload(asset_type=asset_type)
        return{'FINISHED'}