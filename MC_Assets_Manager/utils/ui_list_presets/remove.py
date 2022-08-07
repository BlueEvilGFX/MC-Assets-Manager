import bpy
import os

from .. import utils
from .. import utils_list
from ..icons import reloadPresetIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_Remove(Operator):
    bl_idname = "mcam.preset_list_remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try: 
            item = scene.mcAssetsManagerProps.preset_list[scene.mcAssetsManagerProps.preset_index]             #   check if a preset is selected
            if scene.mcAssetsManagerProps.item_unlock and (item.path == "" or item.path == "$$$"):             #   check if remove unlocked and own
                return True
        except: return False

    @reloadPresetIcons(1)
    def execute(self, context):
        asset_type = "own_presets"
        list = context.scene.mcAssetsManagerProps.preset_list
        index = context.scene.mcAssetsManagerProps.preset_index
        
        utils_list.remove.execute(context, asset_type, list, index)
        self.report({'INFO'}, "preset successully removed")
        return{'FINISHED'}   

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(PRESET_OT_Remove)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_Remove)