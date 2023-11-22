import bpy
from bpy.props import StringProperty
from MC_Assets_Manager.core.utils import icons, paths, reload

class UI_LIST_OT_RELOAD(bpy.types.Operator):
    """
    description:
        operator wich reloads a ui list
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of paths.ASSETS | paths.PRESETS 
        | paths.RIGS | paths.DLCs
    """
    bl_idname = "mcam.ui_list_reload"
    bl_label = "reload"

    asset_type : StringProperty()

    def execute(self, context):
        if self.asset_type == paths.AssetTypes.ASSETS:
            reload.reload_asset_list()
            icons.reload_asset_icons()
            # self.report({'INFO'}, f'successfully reloaded asset list')
            return {'FINISHED'}

        if self.asset_type == paths.AssetTypes.PRESETS:
            reload.reload_preset_list()
            icons.reload_preset_icons()
            # self.report({'INFO'}, f'successfully reloaded preset list')
            return {'FINISHED'}
        
        if self.asset_type == paths.AssetTypes.RIGS:
            reload.reload_rig_list()
            icons.reload_rig_icons()
            # self.report({'INFO'}, f'successfully reloaded rig list')
            return {'FINISHED'}

        if self.asset_type == paths.AssetTypes.DLCS:
            reload.reload_dlc_list()
            icons.reload_dlc_icons()
            # self.report({'INFO'}, f'successfully reloaded dlc list')
            return {'FINISHED'}
            
        return{'CANCELLED'}