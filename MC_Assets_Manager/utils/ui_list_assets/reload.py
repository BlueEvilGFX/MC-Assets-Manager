import bpy

from .. import utils
from ..icons import reloadDLCIcons, reloadAssetIcons

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_Reload(Operator):
    bl_idname = "mcam.asset_list_reload"
    bl_label = "reload"

    @reloadDLCIcons(0)
    @reloadAssetIcons(0)
    def execute(self, context):
        utils.AddonReloadManagement.reloadAssetList()
        self.report({'INFO'}, "asset list successully reloaded") 
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(ASSET_OT_Reload)

  
def unregister():
    bpy.utils.unregister_class(ASSET_OT_Reload)