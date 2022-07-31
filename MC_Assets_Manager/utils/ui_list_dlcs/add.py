import bpy
import os
import zipfile
from .. import utils
from ..icons import reloadDLCIcons, reloadPresetIcons
from ... import addonPreferences

from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_OT_Add(Operator, ImportHelper):
    bl_idname = "mcam.dlc_list_add"
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

    def execute(self, context):
        for file in self.files:
            file_name = file.name
            filepath = os.path.join(os.path.dirname(self.filepath), file_name)

            self.add(filepath)

        utils.AddonReloadManagement.reloadDlcJson()
        utils.AddonReloadManagement.reloadDlcList()

        dlc = os.path.splitext(os.path.basename(self.filepath))[0]
        init_path = utils.AddonPathManagement.getInitPath(dlc)[1]

        if init_path:
            addonPreferences.reload()
        self.report({'INFO'}, "dlc successully added")

        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(DLC_OT_Add)
  
def unregister():
    bpy.utils.unregister_class(DLC_OT_Add)