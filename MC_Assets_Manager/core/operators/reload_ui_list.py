import bpy
from bpy.props import StringProperty

from ..utils import paths
from ..utils import icons
from ..utils import reload

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
                icons.reload_preset_icons()
                ],
            paths.DLCS : [
                reload.reload_dlc_list(),
                icons.reload_dlc_icons()
                ]
            }
        
        function.get(self.asset_type, {'CANCELLED'})
        return {'FINISHED'}