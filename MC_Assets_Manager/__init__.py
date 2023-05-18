from . import addon_updater_ops

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                       bl_info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bl_info = {
    "name": "[Minecraft Assets Manager]",
    "author": "BlueEvilGFX",
    "version": (0, 3, 5),
    "blender": (3, 2, 2),
    }  
    
# ━━━━━━━
if "core" in locals():
    import importlib
    importlib.reload(core)
else:
    from . import core
# ━━━━━━━

def register():
    addon_updater_ops.register(bl_info)
    core.register()

def unregister():
    core.unregister()
    addon_updater_ops.unregister()
    
if __name__ == "__main__":
    register(bl_info)