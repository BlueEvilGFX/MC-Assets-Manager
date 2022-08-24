import bpy

from ...miscs import utils
from ..ui_list_utils import add
from ...miscs.icons import reloadPresetIcons

from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_Add(Operator, ImportHelper):
    bl_idname = "mcam.preset_list_add"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.blend;*.zip;*.rar", options = {"HIDDEN"})
    files : CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    @reloadPresetIcons(1)
    def execute(self, context):
        presets_path = utils.AddonPathManagement.getOwnPresetsDirPath()
        add.execute(self, presets_path)

        utils.AddonReloadManagement.reloadPresetList()
        self.report({'INFO'}, "rig successully added")
        
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(PRESET_OT_Add)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_Add)