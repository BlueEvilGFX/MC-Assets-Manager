import bpy
import os
import zipfile

from .. import utils

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_Export(Operator, ExportHelper):
    bl_idname = "preset_list.export"
    bl_label = "export"

    filename_ext = ".zip"

    addonPath = utils.AddonPathManagement.getAddonPath()
    presetsList = utils.AddonPathManagement.getOwnPresets()

    @classmethod
    def poll(cls, context):
        path = os.path.join(cls.addonPath, "files", "own_presets")
        files = os.listdir(path)
        return False if not files else True

    def execute(self, context):
        # get path & data
        path = os.path.join(self.addonPath, "files", "own_presets")
        # export
        destination = self.filepath
        with zipfile.ZipFile(destination, 'w', compression = zipfile.ZIP_DEFLATED) as my_zip:
            for fileName in self.presetsList:
                filePath = os.path.join(path, fileName)
                my_zip.write(filePath, fileName)
        self.report({'INFO'}, "presets successully exported")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(PRESET_OT_Export)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_Export)