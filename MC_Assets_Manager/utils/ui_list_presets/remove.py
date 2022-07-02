import bpy
import os

from .. import utils
from ..icons import reloadRigIcons

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

    @reloadRigIcons(1)
    def execute(self, context):
        # get path & data
        path = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_presets")
        files = [file for file in os.listdir(path) if not file == "icons"]
        preset_list = context.scene.mcAssetsManagerProps.preset_list
        index = context.scene.mcAssetsManagerProps.preset_index
        file_path = os.path.join(path, files[index])
        icon_name = os.path.splitext(files[index])[0]+".png"
        icon_path = os.path.join(path, "icons", icon_name)
        # remove
        os.remove(file_path)
        if os.path.exists(icon_path):
            os.remove(icon_path)
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