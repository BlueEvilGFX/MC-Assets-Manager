import bpy
from bpy.types import Operator

from .icons import reloadDLCIcons, reloadPresetIcons, reloadAssetIcons, reloadRigIcons
from . import utils

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ADDON_OT_RELOAD(Operator):
    bl_idname = "mcam.main_reload"
    bl_label = "reload"
    
    @reloadDLCIcons(0)
    @reloadPresetIcons(0)
    @reloadAssetIcons(0)
    @reloadRigIcons(0)
    def execute(self, context):

        utils.AddonReloadManagement.reloadDlcJson()
        utils.AddonReloadManagement.reloadDlcList()
        utils.AddonReloadManagement.reloadPresetList()
        utils.AddonReloadManagement.reloadAssetList()
        utils.AddonReloadManagement.reloadRigList()

        self.report({'INFO'}, "addon successully reloaded")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register(): 
    bpy.utils.register_class(ADDON_OT_RELOAD)

def unregister():
    bpy.utils.unregister_class(ADDON_OT_RELOAD)