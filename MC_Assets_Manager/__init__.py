#   initializing setup and addon updater
from . import setup
from . import addon_updater_ops

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                       bl_info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bl_info = {
    "name": "[Minecraft Assets Manager]",
    "author": "BlueEvilGFX",
    "version": (0, 2, 2),
    "blender": (3, 2, 2),
    }  
    
# ━━━━━━━
if "load_modules" in locals():          #   check if already loaded
    import importlib
    importlib.reload(load_modules)      #   reload module
else:
    from . import load_modules          #   load module
# ━━━━━━━

def register():
    addon_updater_ops.register(bl_info)
    load_modules.register()

def unregister():
    load_modules.unregister()
    addon_updater_ops.unregister()
    
if __name__ == "__main__":
    register(bl_info)