from . import icons, paths, properties, reload, asset_dict


def register():
    properties.register()
    icons.register()
    # # load dlc list: needed for addon to be loaded properly
    # reload.reload_dlc_json()
    # reload.reload_dlc_list()

def unregister():
    icons.unregister()
    properties.unregister()
