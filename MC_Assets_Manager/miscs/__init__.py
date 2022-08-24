#   import all files with registering functions
from . import icons
from . import operators
from . import properties
from . import github_dlcs
from . import shift_a_menu

from . import hotkeys

#   import other files : utils as directly addressed file
from .utils import *

# classes = (icons, operators, properties, github_dlcs)
classes = (icons, operators, properties, github_dlcs, shift_a_menu, hotkeys)

def register():
    for cls in classes:
        cls.register()

def unregister():
    for cls in reversed(classes):
        cls.unregister()