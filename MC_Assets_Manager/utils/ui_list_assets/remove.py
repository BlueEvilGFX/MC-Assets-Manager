import bpy
import os

from .. import utils
from .. import utils_list
from ..icons import reloadAssetIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_Remove(Operator):
    bl_idname = "mcam.asset_list_remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try: 
            item = scene.mcAssetsManagerProps.asset_list[scene.mcAssetsManagerProps.asset_index]                #   check if a asset is selected
            if scene.mcAssetsManagerProps.item_unlock and item.path == "":                                      #   check if remove unlocked and own
                return True
        except: return False

    @reloadAssetIcons(1)
    def execute(self, context):
        asset_type = "own_assets"
        list = context.scene.mcAssetsManagerProps.asset_list
        index = context.scene.mcAssetsManagerProps.asset_index

        utils_list.remove.execute(context, asset_type, list, index)
        self.report({'INFO'}, "asset successully removed")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(ASSET_OT_Remove)
  
def unregister():
    bpy.utils.unregister_class(ASSET_OT_Remove)
