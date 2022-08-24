import bpy
import os

from . import main_add

from bpy.props import StringProperty, CollectionProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Main_ADD_EXEC_DATA = None

class MAIN_OT_ADD_FILE(Operator, ImportHelper):
    '''Operator class which gets the file path'''
    
    bl_idname = "mcam.add_main_file"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.blend;*.zip;*.rar", options = {"HIDDEN"})
    files : CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})
    
    icon : BoolProperty(default=False)
    add_to : EnumProperty(default = None, items = [ ("0", "Presets", ""),
                                                    ("1", "Assets", ""),
                                                    ("2", "Rigs", "")])
    asset_types = {"0" : "own_presets", "1" : "own_assets", "2" : "own_rigs"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "add_to", expand=True)

        layout.prop(self, "icon", text="custom icon usage")
        layout.alert = True
        if self.icon:
            layout.label(text="• icon must be named identically to the file name")
        layout.label(text="• does not support asset packages")

    def execute(self, context):
        global Main_ADD_EXEC_DATA
        Main_ADD_EXEC_DATA = main_add.Main_ADD_EXEC()

        asset_files = [file.name for file in self.files]
        asset_type = self.asset_types[self.add_to]
        asset_source_dir = os.path.dirname(self.filepath) 

        Main_ADD_EXEC_DATA.set_asset_files(asset_files, asset_type, asset_source_dir, self)
        Main_ADD_EXEC_DATA.set_icon_init(self.icon)

        if self.icon:
            bpy.ops.mcam.add_main_icon('INVOKE_DEFAULT')
        else:
            Main_ADD_EXEC_DATA.execute()
        return{'FINISHED'}

class MAIN_OT_ADD_ICON(Operator, ImportHelper):
    '''Operator class which gets the icon'''

    bl_idname = "mcam.add_main_icon"
    bl_label = "add"
                                                    
    filter_glob : StringProperty(default = "*.png", options = {"HIDDEN"})
    files : CollectionProperty( name='File paths',
                                type=bpy.types.OperatorFileListElement,
                                options={'HIDDEN', 'SKIP_SAVE'})
    
    def draw(self, context):
        layout = self.layout
        layout.alert = True
        layout.label(text="icon must be named identically to the file name")

    def execute(self, context):
        global Main_ADD_EXEC_DATA

        icon_source_dir = os.path.dirname(self.filepath) 

        Main_ADD_EXEC_DATA.set_icon_files([file.name for file in self.files],icon_source_dir, self)
        Main_ADD_EXEC_DATA.execute()

        return{'FINISHED'}

def register():
    bpy.utils.register_class(MAIN_OT_ADD_ICON)
    bpy.utils.register_class(MAIN_OT_ADD_FILE)

def unregister():
    bpy.utils.unregister_class(MAIN_OT_ADD_FILE)
    bpy.utils.unregister_class(MAIN_OT_ADD_ICON)