import bpy
from bpy.types import Operator

from MC_Assets_Manager.core.utils import paths

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_LIBRARY_OPEN_ASSET_BROWSER(Operator):
    """
    splits the current area and opens the addon browser
    &&
    closes the window over which the mouse is hovering
    """

    bl_idname = "mcam.split_close_area_asset_browser"
    bl_label = "asset browser"

    def execute(self, context):
        ui_type = bpy.context.area.ui_type
        if ui_type == 'ASSETS':
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

class MAIN_OT_CREATE_ASSET_LIBRARY(Operator):
    """
    creates the asset library 'McAM'
    """

    bl_idname = "mcam.create_asset_library"
    bl_label = "create"

    @classmethod
    def poll(cls, context):
        libraries = bpy.context.preferences.filepaths
        for lib in libraries.asset_libraries:
            if lib.name == "McAM":
                return False
        return True

    def execute(self, context):
        bpy.ops.preferences.asset_library_add()
        library = bpy.context.preferences.filepaths.asset_libraries[-1]
        library.name = "McAM"
        library.path = paths.get_storage_dir()
        return {'FINISHED'}

class MAIN_OT_REMOVE_ASSET_LIBRARY(Operator):
    """
    removes the asset library "McAM"
    """

    bl_idname = "mcam.remove_asset_library"
    bl_label = "remvoe"

    @classmethod
    def poll(cls, context):
        filepaths = bpy.context.preferences.filepaths
        for library in filepaths.asset_libraries:
            if library.name == "McAM":
                return True
        return False

    def execute(self, context):
        filepaths = bpy.context.preferences.filepaths
        for i, library in enumerate(filepaths.asset_libraries):
            if library.name == "McAM":
                bpy.ops.preferences.asset_library_remove(index=i)
        return {'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(ASSET_LIBRARY_OPEN_ASSET_BROWSER)
    bpy.utils.register_class(MAIN_OT_CREATE_ASSET_LIBRARY)
    bpy.utils.register_class(MAIN_OT_REMOVE_ASSET_LIBRARY)

def unregister():
    bpy.utils.unregister_class(MAIN_OT_REMOVE_ASSET_LIBRARY)
    bpy.utils.unregister_class(MAIN_OT_CREATE_ASSET_LIBRARY)
    bpy.utils.unregister_class(ASSET_LIBRARY_OPEN_ASSET_BROWSER)