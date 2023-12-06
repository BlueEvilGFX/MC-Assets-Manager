import bpy
from MC_Assets_Manager.core.utils import paths, reload
from MC_Assets_Manager.core import addonpreferences
import time

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MCAM_OT_RELOAD_ALL(bpy.types.Operator):

    bl_idname = "mcam.main_reload"
    bl_label = "reload"

    def execute(self, context):
        start = time.time()
        reload.reload_dlc_json()
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.ASSETS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.PRESETS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.RIGS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.DLCS)
        addonpreferences.reload_addon_preferences()
        elapsed_time = round((time.time()-start)*1000, 2)
        self.report({'INFO'}, f'successfully reloaded all asset lists - {elapsed_time}ms')
        return {'FINISHED'}