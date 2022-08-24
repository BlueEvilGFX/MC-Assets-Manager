import bpy

from ..ui_list_utils import export
from ...miscs import utils

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_Export(Operator, ExportHelper):
    bl_idname = "mcam.rig_list_export"
    bl_label = "export"

    filename_ext = ".zip"

    assets = "own_rigs"

    @classmethod
    def poll(cls, context):
        return export.poll(cls.assets)

    def execute(self, context):
        rigsList = utils.AddonPathManagement.getOwnRigs()
        export.execute(self, self.assets, rigsList)

        self.report({'INFO'}, "rigs successully exported")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(RIG_OT_Export)
  
def unregister():
    bpy.utils.unregister_class(RIG_OT_Export)