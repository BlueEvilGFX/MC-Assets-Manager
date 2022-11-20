import bpy
from bpy.types import Menu

from MC_Assets_Manager.core.utils import paths

addon_keymaps = []

class EMPTY_MT_PIE_MCAM(Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "EMPTY_MT_mcam_main"
    bl_label = "McAM"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        asset = pie.operator("mcam.ui_list_append", icon="COMMUNITY", text = "append asset")
        asset.asset_type = paths.ASSETS

        preset = pie.operator("mcam.ui_list_append", icon="ASSET_MANAGER", text = "append preset")
        preset.asset_type = paths.PRESETS

        rig = pie.operator("mcam.ui_list_append", icon="ARMATURE_DATA", text = "append rig")
        rig.asset_type = paths.RIGS

        pie.operator("mcam.split_close_area_asset_browser", icon="ASSET_MANAGER")

def register():
    bpy.utils.register_class(EMPTY_MT_PIE_MCAM)
    # Add the hotkey
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Screen', space_type='EMPTY')
        kmi = km.keymap_items.new("wm.call_menu_pie", type='A', value='PRESS', alt=True, shift=True)
        kmi.properties.name = "EMPTY_MT_mcam_main"
        addon_keymaps.append((km, kmi))

def unregister():
    # Remove the hotkey
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(EMPTY_MT_PIE_MCAM)