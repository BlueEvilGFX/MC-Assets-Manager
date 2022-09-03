from . import addonpreferences, operators, uilists, utils

def register():
    addonpreferences.register()
    utils.register()
    operators.register()
    uilists.register()

def unregister():
    uilists.unregister()
    operators.unregister()
    utils.unregister()
    addonpreferences.unregister()
