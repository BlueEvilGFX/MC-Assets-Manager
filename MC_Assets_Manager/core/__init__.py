from . import addonpreferences, operators, uilists, utils, ui

def register():
    addonpreferences.register()
    utils.register()
    operators.register()
    uilists.register()
    ui.register()

def unregister():
    ui.unregister()
    uilists.unregister()
    operators.unregister()
    utils.unregister()
    addonpreferences.unregister()
