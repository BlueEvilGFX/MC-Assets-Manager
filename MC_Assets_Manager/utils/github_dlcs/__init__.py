from . import icons, operators, ui, connect, auto_check

def register():
    icons.register()
    operators.register()

def unregister():
    operators.unregister()
    icons.unregister()