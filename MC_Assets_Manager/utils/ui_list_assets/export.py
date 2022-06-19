import bpy
import os
import zipfile

from .. import utils

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_Export(Operator, ExportHelper):
    bl_idname = "asset_list.export"
    bl_label = "export"

    filename_ext = ".zip"

    addonPath = utils.AddonPathManagement.getAddonPath()
    assetsList = utils.AddonPathManagement.getOwnAssets()

    @classmethod
    def poll(cls, context):
        path = os.path.join(cls.addonPath, "files", "own_assets")
        files = os.listdir(path)
        return False if not files else True

    def execute(self, context):
        # get path & data
        path = os.path.join(self.addonPath, "files", "own_assets")
        # export
        destination = self.filepath
        with zipfile.ZipFile(destination, 'w', compression = zipfile.ZIP_DEFLATED) as my_zip:
            for fileName in self.assetsList:
                filePath = os.path.join(path, fileName)
                my_zip.write(filePath, fileName)
        self.report({'INFO'}, "assets successully exported")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(ASSET_OT_Export)
  
def unregister():
    bpy.utils.unregister_class(ASSET_OT_Export)