import bpy
from bpy.types import Menu

from MC_Assets_Manager.core.ui import shift_a_menu

addon_keymaps = []

class EMPTY_MT_PIE_MCAM(Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "EMPTY_MT_mcam_main"
    bl_label = "McAM"

    def draw(self, context):
        element = self.layout.menu_pie()
        shift_a_menu.OBJECT_MT_McAssets_ShiftA_submenu.list_operators(element)

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