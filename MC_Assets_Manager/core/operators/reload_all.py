import bpy

class MCAM_OT_RELOAD_ALL(bpy.types.Operator):

    bl_idname = "mcam.main_reload"
    bl_label = "reload"

    def execute(self, context):

        return {'FINISHED'}