# importing the classes which needs registering
from .reload_all import MCAM_OT_RELOAD_ALL
from .ui_list_reload import UI_LIST_OT_RELOAD
from .ui_list_add import UI_LIST_OT_ADD
from .ui_list_remove import UI_LIST_OT_REMOVE
from .ui_list_append import UI_LIST_OT_APPEND


def register():
    from bpy.utils import register_class
    register_class(UI_LIST_OT_RELOAD)
    register_class(UI_LIST_OT_REMOVE)
    register_class(UI_LIST_OT_ADD)
    register_class(MCAM_OT_RELOAD_ALL)
    register_class(UI_LIST_OT_APPEND)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(UI_LIST_OT_APPEND)
    unregister_class(MCAM_OT_RELOAD_ALL)
    unregister_class(UI_LIST_OT_ADD)
    unregister_class(UI_LIST_OT_REMOVE)
    unregister_class(UI_LIST_OT_RELOAD)