import bpy

from .. import utils
from ..utils_list import add
from ..icons import reloadRigIcons

from bpy.props import StringProperty, CollectionProperty
from bpy.types import  Operator
from bpy_extras.io_utils import ImportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_Add(Operator, ImportHelper):
    bl_idname = "mcam.rig_list_add"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.blend;*.zip;*.rar", options = {"HIDDEN"})
    files : CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    @reloadRigIcons(1)
    def execute(self, context):
        rigs_path = utils.AddonPathManagement.getOwnRigsDirPath()
        add.execute(self, rigs_path)

        utils.AddonReloadManagement.reloadRigList()
        self.report({'INFO'}, "rig successully added")
        
        return{'FINISHED'}


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(RIG_OT_Add)
  
def unregister():
    bpy.utils.unregister_class(RIG_OT_Add)
