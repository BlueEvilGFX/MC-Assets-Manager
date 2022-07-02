import bpy
from bpy.app.handlers import persistent
from . import addon_updater_ops

import importlib, os
from .utils import utils

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@persistent
def load_handler(dummy):
    utils.AddonReloadManagement.reloadDlcList()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class McAMDlc(bpy.types.Panel):
    bl_label = "DLCs | Scripts"
    bl_idname = "SCENE_PT_MCAM_DLC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "McAM"

    def draw(self, context):
        layout = self.layout

        addon_updater_ops.update_notice_box_ui(self, layout)

        def header():
            box = layout.box()
            row = box.row()
            row.prop(context.scene.mcAssetsManagerProps, "scriptUIEnum")
            row.operator("mcam.dlc_list_reload", text = "", icon = "FILE_REFRESH")
        header()

        def showDLCsUI():
            dlc_list = context.scene.mcAssetsManagerProps.dlc_list
            if dlc_list:
                #   get paths and more
                addon_path = utils.AddonPathManagement.getAddonPath()
                dlc_paths = os.path.join(addon_path, "files", "DLCs")
                dlc_list = os.listdir(dlc_paths)
 
                for dlc in dlc_list:
                    index = context.scene.mcAssetsManagerProps.dlc_index
                    active = context.scene.mcAssetsManagerProps.dlc_list[index].active              #   read active status of dlc
                    init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]                     #   check init path and existence

                    if active and init_exists:                                                      #   if dlc exists & active & init file (script based)
                        if dlc in locals():                                                         #   if already loaded
                            importlib.reload(eval(dlc))                                             #   reload module
                        else:
                            module_name = ".files.DLCs."+dlc                                        #   get module name for importing
                            locals()[dlc] = importlib.import_module(name = module_name, package = __package__) 
                        
                        dlc_name = os.path.splitext(locals()[dlc].__name__)[-1][1:]                 #   get dlc name from selection
                        enumSelection = context.scene.mcAssetsManagerProps.scriptUIEnum             #   get seletion from enum

                        if enumSelection == dlc_name and active:                                    #   if selection is dlc from iteration
                            row = self.layout.row()
                            row.label(text="")
                            row.scale_y = 0.5
                            locals()[dlc].Panel.draw(self, context)                                 #   draw addon preferences from dlc
        showDLCsUI()

def register():
    bpy.app.handlers.load_post.append(load_handler)
    bpy.utils.register_class(McAMDlc)

def unregister():
    bpy.utils.unregister_class(McAMDlc)
    bpy.app.handlers.load_post.remove(load_handler)