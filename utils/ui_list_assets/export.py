import bpy
from ..utils_list import export

from .. import utils

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_Export(Operator, ExportHelper):
    bl_idname = "mcam.asset_list_export"
    bl_label = "export"

    filename_ext = ".zip"

    assets = "own_assets"

    @classmethod
    def poll(cls, context):
        return export.poll(cls.assets)

    def execute(self, context):
        rigsList = utils.AddonPathManagement.getOwnAssets()
        export.execute(self, self.assets, rigsList)

        self.report({'INFO'}, "assets successully exported")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(ASSET_OT_Export)
  
def unregister():
    bpy.utils.unregister_class(ASSET_OT_Export)