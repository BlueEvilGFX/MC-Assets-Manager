from . import addon_reloader_ops
from . import main_add_ops
from . import scriptUIEnum_switch_ops

def register():
    addon_reloader_ops.register()
    main_add_ops.register()
    scriptUIEnum_switch_ops.register()


def unregister():
    scriptUIEnum_switch_ops.unregister()
    main_add_ops.unregister()
    addon_reloader_ops.unregister()