from . import icons
from . import operators
from . import connect
from . import ui


def register():
    icons.register()
    operators.register()

def unregister():
    operators.unregister()
    icons.unregister()