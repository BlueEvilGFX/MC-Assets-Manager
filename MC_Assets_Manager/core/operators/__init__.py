# importing the classes which needs registering
from .reload_ui_list import UI_LIST_OT_RELOAD
from .reload_all import MCAM_OT_RELOAD_ALL


def register():
    from bpy.utils import register_class
    register_class(UI_LIST_OT_RELOAD)
    register_class(MCAM_OT_RELOAD_ALL)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(MCAM_OT_RELOAD_ALL)
    unregister_class(UI_LIST_OT_RELOAD)