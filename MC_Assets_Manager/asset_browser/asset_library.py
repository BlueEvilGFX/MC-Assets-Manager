import bpy
from bpy.types import Operator

from ..miscs import utils


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MAIN_OT_CREATE_ASSET_LIBRARY(Operator):
    '''Operator class which gets the icon'''

    bl_idname = "mcam.create_asset_library"
    bl_label = "add"

    def execute(self, context):
        bpy.ops.preferences.asset_library_add()

        paths = bpy.context.preferences.filepaths

        for i, library in enumerate(paths.asset_libraries):
            if library.name == "":
                library.name = "McAM"
                library.path = utils.AddonPathManagement.getStorageDirPath()
                break
        return{'FINISHED'}

class MAIN_OT_REMOVE_ASSET_LIBRARY(Operator):
    '''Operator class which gets the icon'''

    bl_idname = "mcam.remove_asset_library"
    bl_label = "remove"


    def execute(self, context):
        paths = bpy.context.preferences.filepaths

        for i, library in enumerate(paths.asset_libraries):
            if library.name == "McAM":
                library.name = "McAM"
                bpy.ops.preferences.asset_library_remove(index=i)
                break
        return{'FINISHED'}

asset_area = None
class MAIN_OT_OPEN_ASSET_BROWSER_IN_SPLIT(Operator):
    '''
    Splits the current area and opens the addon browser
    &&
    Closes the window over which the mouse is hovering 
    '''

    bl_idname = "mcam.split_close_area_asset_browser"
    bl_label = "asset browser"

    def execute(self, context):
        global asset_area

        if asset_area is not None:
            try:
                bpy.ops.screen.area_close({"area": asset_area})
            except:
                print("McAM: cannot close asset browser area")
            asset_area = None
        elif bpy.context.area.ui_type == 'ASSETS':
            try:
                bpy.ops.screen.area_close()
            except:
                print("McAM: cannot close asset browser area")
        else:
            try:
                bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
                asset_area = bpy.context.screen.areas[-1]
                asset_area.ui_type = 'ASSETS'
            except:
                print("McAM: cannot open new area: asset browser")
        return{'FINISHED'}

def register():
    bpy.utils.register_class(MAIN_OT_CREATE_ASSET_LIBRARY)
    bpy.utils.register_class(MAIN_OT_REMOVE_ASSET_LIBRARY)
    bpy.utils.register_class(MAIN_OT_OPEN_ASSET_BROWSER_IN_SPLIT)

def unregister():
    bpy.utils.unregister_class(MAIN_OT_OPEN_ASSET_BROWSER_IN_SPLIT)
    bpy.utils.unregister_class(MAIN_OT_REMOVE_ASSET_LIBRARY)
    bpy.utils.unregister_class(MAIN_OT_CREATE_ASSET_LIBRARY)