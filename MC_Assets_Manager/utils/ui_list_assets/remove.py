import bpy
import os

from .. import utils

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_Remove(Operator):
    bl_idname = "asset_list.remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try: 
            item = scene.mcAssetsManagerProps.asset_list[scene.mcAssetsManagerProps.asset_index]                #   check if a asset is selected
            if scene.mcAssetsManagerProps.item_unlock and item.path == "":                                      #   check if remove unlocked and own
                return True
        except: return False

    def execute(self, context):
        # get path & data
        path = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_assets")
        files = os.listdir(path)
        asset_list = context.scene.mcAssetsManagerProps.asset_list
        index = context.scene.mcAssetsManagerProps.asset_index
        # remove
        os.remove(os.path.join(path, files[index]))
        asset_list.remove(index)
        context.scene.mcAssetsManagerProps.asset_index = min(max(0, index - 1), len(asset_list) - 1)
        self.report({'INFO'}, "asset successully removed")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(ASSET_OT_Remove)
  
def unregister():
    bpy.utils.unregister_class(ASSET_OT_Remove)
