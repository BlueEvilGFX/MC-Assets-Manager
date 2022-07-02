import bpy
from .. import utils
from ..icons import reloadDLCIcons, reloadPresetIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_OT_Reload(Operator):
    bl_idname = "mcam.dlc_list_reload"
    bl_label = "reload"

    @reloadDLCIcons(0)
    @reloadPresetIcons(0)
    def execute(self, context):
        utils.AddonReloadManagement.reloadDlcList()
        self.report({'INFO'}, "dlc list successully reloaded") 
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(DLC_OT_Reload)
  
def unregister():
    bpy.utils.unregister_class(DLC_OT_Reload)