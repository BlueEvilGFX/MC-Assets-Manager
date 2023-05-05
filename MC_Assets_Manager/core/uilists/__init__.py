import bpy

from . import assets, dlcs, presets, rigs


def register():
    bpy.utils.register_class(assets.ASSET_UL_List)
    bpy.utils.register_class(dlcs.DLC_UL_List)
    bpy.utils.register_class(presets.PRESET_UL_List)
    bpy.utils.register_class(rigs.RIG_UL_List)


def unregister():
    bpy.utils.unregister_class(rigs.RIG_UL_List)
    bpy.utils.unregister_class(presets.PRESET_UL_List)
    bpy.utils.unregister_class(dlcs.DLC_UL_List)
    bpy.utils.unregister_class(assets.ASSET_UL_List)