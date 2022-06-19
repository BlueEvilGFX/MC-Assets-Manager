import bpy
import os
import zipfile

from .. import utils

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_Export(Operator, ExportHelper):
    bl_idname = "rig_list.export"
    bl_label = "export"

    filename_ext = ".zip"

    addonPath = utils.AddonPathManagement.getAddonPath()
    assetsList = utils.AddonPathManagement.getOwnRigs()

    @classmethod
    def poll(cls, context):
        path = os.path.join(cls.addonPath, "files", "own_rigs")
        files = os.listdir(path)
        return False if not files else True

    def execute(self, context):
        # get path & data
        path = os.path.join(self.addonPath, "files", "own_rigs")
        # export
        destination = self.filepath
        with zipfile.ZipFile(destination, 'w', compression = zipfile.ZIP_DEFLATED) as my_zip:
            for fileName in self.assetsList:
                filePath = os.path.join(path, fileName)
                my_zip.write(filePath, fileName)
        self.report({'INFO'}, "rigs successully exported")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(RIG_OT_Export)
  
def unregister():
    bpy.utils.unregister_class(RIG_OT_Export)