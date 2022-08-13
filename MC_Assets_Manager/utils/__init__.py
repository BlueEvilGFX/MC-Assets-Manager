#   import all files with registering functions
from . import icons
from . import operators
from . import properties

from . import ui_list_assets
from . import ui_list_dlcs
from . import ui_list_presets
from . import ui_list_rigs
from . import github_dlcs

from . import utils_list

#   import other files : utils as directly addressed file
from .utils import *

classes = (icons, operators, properties, ui_list_assets, ui_list_dlcs, ui_list_presets, ui_list_rigs, github_dlcs)

def register():
    for cls in classes:
        cls.register()

def unregister():
    for cls in reversed(classes):
        cls.unregister()