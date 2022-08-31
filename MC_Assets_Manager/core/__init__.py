from . import addonpreferences, operators, uilists, utils

def register():
    addonpreferences.register()
    utils.register()
    operators.register()
    uilists.register()

    utils.reload.reload_dlc_json()

def unregister():
    uilists.unregister()
    operators.unregister()
    utils.unregister()
    addonpreferences.unregister()
