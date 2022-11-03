from . import icons, paths, properties, reload, asset_dict


def register():
    properties.register()
    icons.register()

def unregister():
    icons.unregister()
    properties.unregister()