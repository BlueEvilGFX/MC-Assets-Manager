import bpy
from .icons import basicMCAM_icon_collection

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   shift a
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def menu_func(self, context):
    pcoll = basicMCAM_icon_collection["McAM"]
    ic = "McAM_copper_block"
    custom_icon = pcoll[ic].icon_id
    self.layout.menu("OBJECT_MT_McAssets_ShiftA_submenu", text = "MC Assets", icon_value = custom_icon)

class OBJECT_MT_McAssets_ShiftA_submenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_McAssets_ShiftA_submenu"
    bl_label = "MC Assets"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("mcam.preset_list_append", icon="COMMUNITY")
        col.operator("mcam.asset_list_append", icon="ASSET_MANAGER")
        col.operator("mcam.rig_list_append", icon="ARMATURE_DATA")

        paths = bpy.context.preferences.filepaths
        if len(paths.asset_libraries) > 0:
            col.operator("mcam.split_close_area_asset_browser", icon="ASSET_MANAGER")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(OBJECT_MT_McAssets_ShiftA_submenu)
    bpy.types.VIEW3D_MT_add.append(menu_func)
  
def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_MT_McAssets_ShiftA_submenu)