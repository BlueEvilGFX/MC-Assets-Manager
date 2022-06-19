import bpy
import os

from .. import utils

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_OT_APPEND(Operator):
    bl_description = "append a preset"
    bl_idname = "preset_list.append"
    bl_label = "append preset"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        utils.AddonReloadManagement.reloadPresetList()
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.template_list("PRESET_UL_List", "The_List", scene.mcAssetsManagerProps, "preset_list", scene.mcAssetsManagerProps, "preset_index")
        
    def execute(self, context):
        scene = context.scene
        item = scene.mcAssetsManagerProps.preset_list[scene.mcAssetsManagerProps.preset_index]
        if item.path == "":
            blendfile = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "own_presets", item.name + ".blend")
        else:
            blendfile = item.path

        with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
            data_to.collections = data_from.collections

        for coll in data_to.collections:
            if coll is not None:
                bpy.context.scene.collection.children.link(coll)
        self.report({'INFO'}, "preset successully appended")
        return{'FINISHED'}
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(PRESET_OT_APPEND)
  
def unregister():
    bpy.utils.unregister_class(PRESET_OT_APPEND)