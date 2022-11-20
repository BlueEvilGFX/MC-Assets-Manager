import bpy
from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_LIBRARY_OPEN_ASSET_BROWSER(Operator):
    """
    splits the current area and opens the addon browser
    &&
    closes the window over which the mouse is hovering
    """

    bl_idname = "mcam.split_close_area_asset_browser"
    bl_label = "asset browser"

    def execute(self, context):
        ui_type = bpy.context.area.ui_type
        if ui_type == 'ASSETS':
            try:
                bpy.ops.screen.area_close()
            except:
                print("McAM: cannot close asset browser area")
        else:
            try:
                bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
                asset_area = bpy.context.screen.areas[-1]
                asset_area.ui_type = 'ASSETS'
            except:
                print("McAM: cannot open new area: asset browser")
        return{'FINISHED'}