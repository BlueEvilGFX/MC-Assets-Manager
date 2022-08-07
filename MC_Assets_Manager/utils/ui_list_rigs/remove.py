import bpy
import os

from .. import utils
from .. import utils_list
from ..icons import reloadRigIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_Remove(Operator):
    bl_idname = "mcam.rig_list_remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try: 
            item = scene.mcAssetsManagerProps.rig_list[scene.mcAssetsManagerProps.rig_index]                    #   check if a rig is selected
            if scene.mcAssetsManagerProps.item_unlock and item.path == "":                                      #    check if remove unlocked and own
                return True
        except: return False

    @reloadRigIcons(1)
    def execute(self, context):
        asset_type = "own_rigs"
        list = context.scene.mcAssetsManagerProps.rig_list
        index = context.scene.mcAssetsManagerProps.rig_index
        
        utils_list.remove.execute(context, asset_type, list, index)
        self.report({'INFO'}, "rig successully removed")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(RIG_OT_Remove)
  
def unregister():
    bpy.utils.unregister_class(RIG_OT_Remove)
