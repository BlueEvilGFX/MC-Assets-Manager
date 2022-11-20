# importing the classes which needs registering
from .dlc_add import DLC_OT_Add
from .dlc_remove import DLC_OT_Remove

from .reload_all import MCAM_OT_RELOAD_ALL

from .ui_list_reload import UI_LIST_OT_RELOAD
from .ui_list_add import UI_LIST_OT_ADD
from .ui_list_remove import UI_LIST_OT_REMOVE
from .ui_list_append import UI_LIST_OT_APPEND

from .asset_library import ASSET_LIBRARY_OPEN_ASSET_BROWSER

from . import github

def register():
    from bpy.utils import register_class
    register_class(DLC_OT_Add)
    register_class(DLC_OT_Remove)
    register_class(UI_LIST_OT_RELOAD)
    register_class(UI_LIST_OT_REMOVE)
    register_class(UI_LIST_OT_ADD)
    register_class(MCAM_OT_RELOAD_ALL)
    register_class(UI_LIST_OT_APPEND)
    register_class(ASSET_LIBRARY_OPEN_ASSET_BROWSER)
    github.register()

def unregister():
    from bpy.utils import unregister_class
    github.unregister()
    unregister_class(ASSET_LIBRARY_OPEN_ASSET_BROWSER)
    unregister_class(UI_LIST_OT_APPEND)
    unregister_class(MCAM_OT_RELOAD_ALL)
    unregister_class(UI_LIST_OT_ADD)
    unregister_class(UI_LIST_OT_REMOVE)
    unregister_class(UI_LIST_OT_RELOAD)
    unregister_class(DLC_OT_Remove)
    unregister_class(DLC_OT_Add)