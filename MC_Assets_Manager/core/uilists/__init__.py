import bpy

from . import dlcs, presets


def register():
    bpy.utils.register_class(dlcs.DLC_UL_List)
    bpy.utils.register_class(presets.PRESET_UL_List)


def unregister():
    bpy.utils.unregister_class(presets.PRESET_UL_List)
    bpy.utils.unregister_class(dlcs.DLC_UL_List)