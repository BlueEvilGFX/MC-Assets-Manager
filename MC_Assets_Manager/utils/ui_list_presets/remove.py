import bpy
import os

from .. import utils

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_Remove(Operator):
    bl_idname = "preset_list.remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try: 
            item = scene.mcAssetsManagerProps.preset_list[scene.mcAssetsManagerProps.preset_index]             #   check if a preset is selected
            if scene.mcAssetsManagerProps.item_unlock and item.path == "":                                     #   check if remove unlocked and own
                return True
        except: return False


    def execute(self, context):
        # get path & data
        path = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_presets")
        files = os.listdir(path)
        preset_list = context.scene.mcAssetsManagerProps.preset_list
        index = context.scene.mcAssetsManagerProps.preset_index
        # remove
        os.remove(os.path.join(path, files[index]))
        preset_list.remove(index)
        context.scene.mcAssetsManagerProps.preset_index = min(max(0, index - 1), len(preset_list) - 1)
        self.report({'INFO'}, "preset successully removed")
        return{'FINISHED'}   

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(PRESET_OT_Remove)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_Remove)