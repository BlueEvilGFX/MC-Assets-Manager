from . import ui_list_assets
from . import ui_list_dlcs
from . import ui_list_presets
from . import ui_list_rigs
from . import ui_list_operators

from . import ui_list_utils

classes = (ui_list_assets, ui_list_dlcs, ui_list_presets, ui_list_rigs, ui_list_operators)

def register():
    for cls in classes:
        cls.register()

def unregister():
    for cls in reversed(classes):
        cls.unregister()