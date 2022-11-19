from . import icons, paths, properties, reload, asset_dict, github_connect


def register():
    properties.register()
    icons.register()

def unregister():
    icons.unregister()
    properties.unregister()