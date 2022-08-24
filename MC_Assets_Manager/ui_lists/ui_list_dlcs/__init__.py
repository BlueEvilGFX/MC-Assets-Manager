from . import list
from . import reload
from . import add
from . import remove

def register():
    list.register()
    reload.register()
    add.register()
    remove.register()

def unregister():
    remove.unregister()
    add.unregister()
    reload.unregister()
    list.unregister()