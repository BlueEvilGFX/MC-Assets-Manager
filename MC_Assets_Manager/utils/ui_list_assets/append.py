import bpy
import os
from .. import utils

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_OT_APPEND(Operator):
    bl_description = "append an asset"
    bl_idname = "asset_list.append"
    bl_label = "append asset"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        utils.AddonReloadManagement.reloadAssetList()
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.template_list("ASSET_UL_List", "The_List", scene.mcAssetsManagerProps, "asset_list", scene.mcAssetsManagerProps, "asset_index")
        
    def execute(self, context):
        scene = context.scene
        item = scene.mcAssetsManagerProps.asset_list[scene.mcAssetsManagerProps.asset_index]
        if item.path == "":
            blendfile = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_assets", item.name + ".blend")

            with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
                data_to.objects = data_from.objects

            for coll in data_to.objects:
                if coll is not None:
                    bpy.context.scene.collection.objects.link(coll)

        else:
            blendfile = item.path
            pathHalf = os.path.join(blendfile, item.type)
            pathFull = os.path.join(pathHalf, item.name)
            bpy.ops.wm.append(filepath=pathFull, filename=item.name,directory=pathHalf,link=False)
            
        self.report({'INFO'}, "asset successully appended")
        return{'FINISHED'}
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(ASSET_OT_APPEND)

def unregister():
    bpy.utils.unregister_class(ASSET_OT_APPEND)