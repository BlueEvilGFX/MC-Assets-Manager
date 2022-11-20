from . import (asset_dict, github_connect, hotkeys, icons, paths, properties,
               reload)


def register():
    properties.register()
    icons.register()
    hotkeys.register()

def unregister():
    hotkeys.unregister()
    icons.unregister()
    properties.unregister()