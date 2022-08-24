import bpy

from ...miscs import utils
from ...miscs.icons import reloadDLCIcons, reloadRigIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_Reload(Operator):
    bl_idname = "mcam.rig_list_reload"
    bl_label = "reload"

    @reloadDLCIcons(0)
    @reloadRigIcons(0)
    def execute(self, context):
        utils.AddonReloadManagement.reloadRigList()
        self.report({'INFO'}, "rig list successully reloaded") 
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(RIG_OT_Reload)

  
def unregister():
    bpy.utils.unregister_class(RIG_OT_Reload)