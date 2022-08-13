import bpy
from . import addon_updater_ops

import importlib
from .utils import utils
from .utils import github_dlcs

from .load_modules import PACKAGE_NAME



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class McAMDlc(bpy.types.Panel):
    bl_label = "DLCs | Scripts"
    bl_idname = "SCENE_PT_MCAM_DLC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "McAM"

    def draw(self, context):
        McAMProps = context.scene.mcAssetsManagerProps
        layout = self.layout

        addon_updater_ops.update_notice_box_ui(self, layout)
        github_dlcs.ui.ui_notice_dlc_update(self)

        dlc_list = McAMProps.dlc_list

        #   check if dlc list is accessible
        if not dlc_list: return

        #   get data
        dlc_list = utils.AddonPathManagement.getDlcList()
        script_dlc_list = [dlc for dlc in dlc_list if utils.AddonPathManagement.getInitPath(dlc)[1]]

        # ━━━━━━━━━━━━ import all DLC UIs
        for dlc in script_dlc_list:
            if dlc in locals():
                importlib.reload(eval(dlc))
            else:
                module_name = ".files.DLCs."+dlc                                       
                locals()[dlc] = importlib.import_module(name = module_name, package = PACKAGE_NAME)

        def displayOperator(row):
            row.scale_x = 0.8
            row.operator("mcam.dlc_list_reload", text = "", icon = "FILE_REFRESH")
            row.operator("mcam.switch_ui_enum", text = "", icon = "ARROW_LEFTRIGHT")

        # ━━━━━━━━━━━━ 1
        enum_selection_1 = McAMProps.scriptUIEnum
        row = layout.box().row()
        row.prop(McAMProps, "scriptUIEnum")
        rr = row
        displayOperator(rr)
        try: locals()[enum_selection_1].Panel.draw(self, context)
        except: print("McAM: UI - DLC-Panel - Error")
        
        # ━━━━━━━━━━━━ 2 UI pananls check
        preferences = utils.AddonPreferencesProperties.getAddonPropAccess()
        if not preferences.two_dlc_ui_panels: return

        self.layout.label(text="")
        # ━━━━━━━━━━━━ 2
        enum_selection_2 = McAMProps.scriptUIEnum2
        row = self.layout.box().row()
        row.prop(McAMProps, "scriptUIEnum2")
        rr = row
        displayOperator(rr)
        try: locals()[enum_selection_2].Panel.draw(self, context)
        except: print("McAM: UI - DLC-Panel - Error")

def register():
    bpy.utils.register_class(McAMDlc)

def unregister():
    bpy.utils.unregister_class(McAMDlc)