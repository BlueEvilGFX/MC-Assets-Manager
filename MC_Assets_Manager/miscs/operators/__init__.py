from . import addon_reloader_ops
from . import scriptUIEnum_switch_ops

def register():
    addon_reloader_ops.register()
    scriptUIEnum_switch_ops.register()


def unregister():
    scriptUIEnum_switch_ops.unregister()
    addon_reloader_ops.unregister()