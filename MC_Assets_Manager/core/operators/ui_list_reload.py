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
        function = {
            paths.ASSETS : [
                reload.reload_asset_list(),
                icons.reload_asset_icons()
                ],
            paths.PRESETS : [
                reload.reload_preset_list(),
                icons.reload_preset_icons()
                ],
            paths.RIGS : [
                reload.reload_rig_list(),
                icons.reload_rig_icons()
                ],
            paths.DLCS : [
                reload.reload_dlc_list(),
                icons.reload_dlc_icons()
                ]
            }
        
        return {'FINISHED'}\
            if function.get(self.asset_type, True)\
            else {'CANCELLED'}
