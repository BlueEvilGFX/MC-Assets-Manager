import bpy

from .. import utils
from ..icons import reloadDLCIcons, reloadPresetIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_Reload(Operator):
    bl_idname = "preset_list.reload"
    bl_label = "reload"

    @reloadDLCIcons(0)
    @reloadPresetIcons(0)
    def execute(self, context):
        utils.AddonReloadManagement.reloadPresetList()
        self.report({'INFO'}, "preset list successully reloaded") 
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(PRESET_OT_Reload)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_Reload)