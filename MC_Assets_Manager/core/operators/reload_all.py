import bpy
from MC_Assets_Manager.core.utils import paths, reload
from MC_Assets_Manager.core import addonpreferences

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MCAM_OT_RELOAD_ALL(bpy.types.Operator):

    bl_idname = "mcam.main_reload"
    bl_label = "reload"

    def execute(self, context):
        reload.reload_dlc_json()
        bpy.ops.mcam.ui_list_reload(asset_type=paths.ASSETS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.PRESETS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.RIGS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.DLCS)
        addonpreferences.reload_addon_preferences()
        return {'FINISHED'}