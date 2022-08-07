import bpy
import os
from .. import utils

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_APPEND(Operator):
    bl_description = "append a rig"
    bl_idname = "mcam.rig_list_append"
    bl_label = "append rig"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        utils.AddonReloadManagement.reloadRigList()
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.template_list("RIG_UL_List", "The_List", scene.mcAssetsManagerProps, "rig_list", scene.mcAssetsManagerProps, "rig_index")
        
    def execute(self, context):
        scene = context.scene
        item = scene.mcAssetsManagerProps.rig_list[scene.mcAssetsManagerProps.rig_index]
        collection = (item.collection != "")

        if item.path == "" or item.path == "$$$":
            name = item.name if not collection else f'{item.name}&&{item.collection}'
            blendfile = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_rigs", name + ".blend")
            file_name = name+".blend"
        else:
            blendfile = item.path
            file_name = item.name+".blend"

                
        if not collection:
            with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
                data_to.objects = data_from.objects
                data_to.collections = data_from.collections

            if data_to.collections:
                main_collection = None
                sub_collections = []
                
                for coll in data_to.collections:
                    if main_collection is None:
                        main_collection = coll
                    else:
                        sub_collections.append(coll)
                    bpy.context.scene.collection.children.link(coll)
                
                collection = bpy.context.view_layer.layer_collection.collection
                if collection:
                    for coll in sub_collections:
                        collection.children.unlink(coll)
            else:
                for obj in data_to.objects:
                    if obj is not None:
                        bpy.context.scene.collection.objects.link(obj)
        else:
            col_name = item.collection
            bpy.ops.wm.append(
                filepath=file_name,
                directory=f'{blendfile}\\Collection\\',
                filename=col_name,
                active_collection=True)

        self.report({'INFO'}, "rig successully appended")
        return{'FINISHED'}
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(RIG_OT_APPEND)

def unregister():
    bpy.utils.unregister_class(RIG_OT_APPEND)