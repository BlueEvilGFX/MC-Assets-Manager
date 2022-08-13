import bpy

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MAIN_OT_SCRIPT_UI_ENUM_SWITCH(Operator):
    bl_idname = "mcam.switch_ui_enum"
    bl_label = ""

    def execute(self, context):
        selection_1 = context.scene.mcAssetsManagerProps.scriptUIEnum
        context.scene.mcAssetsManagerProps.scriptUIEnum = context.scene.mcAssetsManagerProps.scriptUIEnum2
        context.scene.mcAssetsManagerProps.scriptUIEnum2 = selection_1
        return{'FINISHED'}

def register():
    bpy.utils.register_class(MAIN_OT_SCRIPT_UI_ENUM_SWITCH)

def unregister():
    bpy.utils.unregister_class(MAIN_OT_SCRIPT_UI_ENUM_SWITCH)