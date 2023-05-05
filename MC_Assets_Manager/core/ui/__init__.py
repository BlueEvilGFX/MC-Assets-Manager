from . import shift_a_menu
from . import n_panel

def register():
    shift_a_menu.register()
    n_panel.register()

def unregister():
    n_panel.unregister()
    shift_a_menu.unregister()