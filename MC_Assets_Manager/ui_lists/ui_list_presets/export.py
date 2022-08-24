import bpy

from ...miscs import utils
from ..ui_list_utils import export

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_Export(Operator, ExportHelper):
    bl_idname = "mcam.preset_list_export"
    bl_label = "export"

    filename_ext = ".zip"

    assets = "own_presets"

    @classmethod
    def poll(cls, context):
        return export.poll(cls.assets)

    def execute(self, context):
        presetsList = utils.AddonPathManagement.getOwnPresets()
        export.execute(self, self.assets, presetsList)

        self.report({'INFO'}, "presets successully exported")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(PRESET_OT_Export)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_Export)