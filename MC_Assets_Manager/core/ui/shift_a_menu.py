import bpy
from MC_Assets_Manager.core.utils import icons, paths

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   shift a
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def menu_func(self, context):
    pcoll = icons.mcam_icons[icons.PCOLL_MCAM_ID]
    ic = "copper_block"
    custom_icon = pcoll[ic].icon_id
    self.layout.menu(
        "OBJECT_MT_McAssets_ShiftA_submenu",
        text = "MC Assets",
        icon_value = custom_icon
        )

class OBJECT_MT_McAssets_ShiftA_submenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_McAssets_ShiftA_submenu"
    bl_label = "MC Assets"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        self.list_operators(col)

    @staticmethod
    def list_operators(element):
        # asset
        element.operator(
            "mcam.ui_list_append_asset",
            icon="COMMUNITY",
            text = "append asset"
        )

        # preset
        element.operator(
            "mcam.ui_list_append_preset",
            icon="DOCUMENTS",
            text = "append preset"
        )

        # rig
        element.operator(
            "mcam.ui_list_append_rig",
            icon="ARMATURE_DATA",
            text = "append rig"
        )

        # asset browser
        element.operator(
            "mcam.split_close_area_asset_browser",
            icon="ASSET_MANAGER"
        )

        # reload
        element.operator(
            "mcam.main_reload",
            icon="FILE_REFRESH"
        )


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(OBJECT_MT_McAssets_ShiftA_submenu)
    bpy.types.VIEW3D_MT_add.append(menu_func)
  
def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_MT_McAssets_ShiftA_submenu)