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
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        asset = col.operator("mcam.ui_list_append", icon="COMMUNITY")
        asset.asset_type = paths.ASSETS

        preset = col.operator("mcam.ui_list_append", icon="ASSET_MANAGER")
        preset.asset_type = paths.PRESETS

        rig = col.operator("mcam.ui_list_append", icon="ARMATURE_DATA")
        rig.asset_type = paths.RIGS

        # col.operator("mcam.ui_list_append", icon="ASSET_MANAGER")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(OBJECT_MT_McAssets_ShiftA_submenu)
    bpy.types.VIEW3D_MT_add.append(menu_func)
  
def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_MT_McAssets_ShiftA_submenu)