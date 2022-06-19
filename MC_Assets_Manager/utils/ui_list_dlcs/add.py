from struct import pack
import bpy
import importlib
import os
import zipfile
from .. import utils
from ..icons import reloadDLCIcons, reloadPresetIcons

from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_OT_Add(Operator, ImportHelper):
    bl_idname = "dlc_list.add"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.dlc", options = {"HIDDEN"})
    files : CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    @reloadDLCIcons(1)
    @reloadPresetIcons(1)
    def add(self, path):
        preDirPath = utils.AddonPathManagement.getDlcDirPath()
        # add / import
        target = path
        handle = zipfile.ZipFile(target)
        handle.extractall(path = preDirPath)
        handle.close()

        self.report({'INFO'}, "dlc successully added")

    def execute(self, context):
        for file in self.files:
            file_name = file.name
            filepath = os.path.join(os.path.dirname(self.filepath), file_name)

            self.add(filepath)

            #   importing the __init__ file and call its register function from dlc if there is one
            # dlc = os.path.splitext(os.path.basename(self.filepath))[0]
            # existence = utils.AddonPathManagement.getInitPath(dlc)[0]
            # if existence:
            #     package = os.path.splitext(__package__)[0]
            #     package = os.path.splitext(package)[0]
            #     module_name = ".files.DLCs."+dlc
                # locals()[dlc] = importlib.import_module(name = module_name, package = package)

                # locals()[dlc].register()

        utils.AddonReloadManagement.reloadDlcJson()
        utils.AddonReloadManagement.reloadDlcList()

        dlc = os.path.splitext(os.path.basename(self.filepath))[0]
        init_path = utils.AddonPathManagement.getInitPath(dlc)[1]

        if init_path:
            bpy.ops.dlc_list.message('INVOKE_DEFAULT')

        return{'FINISHED'}

class MessageBox(bpy.types.Operator):
    bl_idname = "dlc_list.message"
    bl_label = ""
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 450)
 
    def draw(self, context):
        alert_row = self.layout
        alert_row.alert = True
        alert_row.operator(
            "wm.quit_blender",
            text="Restart blender and then activate the dlc in the addon preferences",
            icon="BLANK1")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(MessageBox)
    bpy.utils.register_class(DLC_OT_Add)
  
def unregister():
    bpy.utils.unregister_class(DLC_OT_Add)
    bpy.utils.unregister_class(MessageBox)