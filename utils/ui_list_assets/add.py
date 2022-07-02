import bpy

from .. import utils
from ..utils_list import add
from ..icons import reloadAssetIcons

from bpy.props import StringProperty, CollectionProperty
from bpy.types import  Operator
from bpy_extras.io_utils import ImportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_Add(Operator, ImportHelper):
    bl_idname = "mcam.asset_list_add"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.blend;*.zip;*.rar", options = {"HIDDEN"})
    files : CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    @reloadAssetIcons(1)
    def execute(self, context):
        assets_path = utils.AddonPathManagement.getOwnAssetsDirPath()
        add.execute(self, assets_path)

        utils.AddonReloadManagement.reloadAssetList()
        self.report({'INFO'}, "asset successully added")
        
        return{'FINISHED'}


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(ASSET_OT_Add)
  
def unregister():
    bpy.utils.unregister_class(ASSET_OT_Add)
