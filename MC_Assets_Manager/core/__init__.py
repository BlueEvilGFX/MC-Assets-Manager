import bpy
from bpy.app.handlers import persistent
from MC_Assets_Manager.core import (addonpreferences, operators, ui, uilists,
                                    utils)


@persistent
def load_handler(dummy):
    bpy.ops.mcam.main_reload()

def register():
    addonpreferences.register()
    utils.register()
    operators.register()
    uilists.register()
    ui.register()

    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    ui.unregister()
    uilists.unregister()
    operators.unregister()
    utils.unregister()
    addonpreferences.unregister()