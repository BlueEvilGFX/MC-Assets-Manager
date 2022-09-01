from . import icons, paths, properties, reload


def register():
    properties.register()
    icons.register()

def unregister():
    icons.unregister()
    properties.unregister()
