# importing the classes which needs registering
from . import github
from .asset_library import ASSET_LIBRARY_OPEN_ASSET_BROWSER
from .dlc_add import DLC_OT_Add
from .dlc_remove import DLC_OT_Remove
from .reload_all import MCAM_OT_RELOAD_ALL
from .ui_list_add import UI_LIST_OT_ADD
from .ui_list_append import UI_LIST_OT_APPEND
from .ui_list_export import UI_LIST_OT_EXPORT, UI_LIST_OT_EXPORT_ALL
from .ui_list_reload import UI_LIST_OT_RELOAD
from .ui_list_remove import UI_LIST_OT_REMOVE

classes = [
    DLC_OT_Add,
    DLC_OT_Remove,
    UI_LIST_OT_RELOAD,
    UI_LIST_OT_REMOVE,
    UI_LIST_OT_ADD,
    UI_LIST_OT_APPEND,
    MCAM_OT_RELOAD_ALL,
    ASSET_LIBRARY_OPEN_ASSET_BROWSER,
    UI_LIST_OT_EXPORT,
    UI_LIST_OT_EXPORT_ALL
]


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    github.register()

def unregister():
    from bpy.utils import unregister_class
    github.unregister()
    for cls in reversed(classes):
        unregister_class(cls)