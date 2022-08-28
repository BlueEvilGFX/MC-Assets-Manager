from . import paths
from . import properties
from . import reload
from . import icons

def register():
    properties.register()
    icons.register()

def unregister():
    icons.unregister()
    properties.unregister()