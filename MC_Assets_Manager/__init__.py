import os
import importlib
from . import addon_updater_ops

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                       bl_info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bl_info = {
    "name": "[Minecraft Assets Manager]",
    "author": "BlueEvilGFX",
    "version": (0, 4, 5),
    "blender": (4, 0, 0),
    }  
    
# ━━━━━━━

if "core" in locals():
    import importlib
    importlib.reload(core)
else:
    from . import core


## THOMAS DLC DEV ONLY
if "ui" in locals():
    import importlib
    importlib.reload(ui)
    importlib.reload(utils)
    importlib.reload(properties)
    importlib.reload(operators)
else:
    from .storage.dlcs.Thomas_Rig_Legacy import ui
    from .storage.dlcs.Thomas_Rig_Legacy import utils
    from .storage.dlcs.Thomas_Rig_Legacy import properties
    from .storage.dlcs.Thomas_Rig_Legacy import operators

# ━━━━━━━
def register():
    addon_updater_ops.register(bl_info)
    core.register()

def unregister():
    core.unregister()
    addon_updater_ops.unregister()
    
if __name__ == "__main__":
    register(bl_info)