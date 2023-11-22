import importlib
import traceback

import bpy
import addon_utils

from MC_Assets_Manager import addon_updater_ops
from MC_Assets_Manager.core.utils import paths

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class McAMDlc(bpy.types.Panel):
    bl_label = "DLCs | Scripts"
    bl_idname = "SCENE_PT_MCAM_DLC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "McAM"

    def draw(self, context):
        McAMProps = context.scene.mc_assets_manager_props
        layout = self.layout

        addon_updater_ops.update_notice_box_ui(self, layout)
        self.ui_notice_dlc_update(self, layout)

        # get data
        script_dlcs = []

        for dlc in McAMProps.dlc_list:
            if paths.DLC.get_sub_init(dlc.name) and dlc.active:
                script_dlcs.append(dlc.name)

        # return if no scripted dlc is installed since nothing will be shown
        if not script_dlcs:
            # layout.label(text="no script based DLC is installed")
            return

        # ━━━━━━━━━━━━ import all DLC UIs
        for dlc in script_dlcs:
            if dlc in locals():
                importlib.reload(dlc)
            else:
                module_name = ".storage.dlcs."+dlc
                locals()[dlc] = importlib.import_module(
                    name = module_name,
                    package = paths.PathConstants.PACKAGE
                    )

        # ━━━━━━━━━━━━ 1
        enum_selection_1 = McAMProps.scriptUIEnum
        row = layout.box().row()
        row.prop(McAMProps, "scriptUIEnum")
        rr = row
        self.displayOperator(rr)
        try:
            locals()[enum_selection_1].Panel.draw(self, context)
        except Exception as e: 
            print(f"McAM: UI - DLC-Panel-1 - Error: {enum_selection_1}")
            print(str(e))
            traceback.print_exc()
        
        # ━━━━━━━━━━━━ 2 UI pananls check
        preferences = paths.McAM.get_addon_properties().main_props
        if not preferences.two_dlc_ui_panels: return

        self.layout.label(text="")
        self.layout.label(text="")
        # ━━━━━━━━━━━━ 2
        enum_selection_2 = McAMProps.scriptUIEnum2
        row = self.layout.box().row()
        row.prop(McAMProps, "scriptUIEnum2")
        rr = row
        self.displayOperator(rr)
        try:
            locals()[enum_selection_2].Panel.draw(self, context)
        except Exception as e: 
            print(f"McAM: UI - DLC-Panel-1 - Error: {enum_selection_2}")
            print(str(e))
            traceback.print_exc()

    # ━━━━━━━━━━━━ 

    def ui_notice_dlc_update(self, reference, element=None) -> None:
        from MC_Assets_Manager.core.utils.github_connect import GitHubReader

        github_reader = GitHubReader()
        # guard clause
        if not github_reader:
            return
        if not github_reader.news:
            return
        
        layout = reference.layout.box() if element is None else element
        box = layout.box()
        row = box.row()
        row.label(text="NEW DLCS OR DLCS UPDATABLE")
        row.operator("mcam.githubignore")
        row.operator("mcam.openaddonprefs", icon="PROPERTIES")
        box.operator("mcam.githubupdateinstallall")

    # ━━━━━━━━━━━━ 

    def displayOperator(self, row):
            row.operator(
                "mcam.switch_ui_enum",
                text = "",
                icon = "ARROW_LEFTRIGHT"
                )

class MAIN_OT_SCRIPT_UI_ENUM_SWITCH(bpy.types.Operator):
    bl_idname = "mcam.switch_ui_enum"
    bl_label = ""

    def execute(self, context):
        mcam_prop = context.scene.mc_assets_manager_props
        mcam_prop.scriptUIEnum,  mcam_prop.scriptUIEnum2 =\
            mcam_prop.scriptUIEnum2,  mcam_prop.scriptUIEnum
        return{'FINISHED'}

class OpenAddonPrefs(bpy.types.Operator):
    bl_idname = "mcam.openaddonprefs"
    bl_label = ""
    bl_description = "opens the user preferences for this addon"

    def execute(self, context):
        from MC_Assets_Manager import bl_info
        search = [
            addon.bl_info.get("name") for addon in addon_utils.modules()
            if addon.bl_info['name'] == bl_info["name"]
        ][0]
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers['WinMan']['addon_search'] = search
        bpy.ops.preferences.addon_expand(module = paths.PathConstants.PACKAGE)
        
        pref_props = paths.McAM.get_addon_properties().main_props
        pref_props.menu = "Online"
        pref_props.online_menu = "Github"

        from MC_Assets_Manager.core.utils import github_connect
        github_connect.GitHubReader()._news = False
        return {'FINISHED'}
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(MAIN_OT_SCRIPT_UI_ENUM_SWITCH)
    bpy.utils.register_class(OpenAddonPrefs)
    bpy.utils.register_class(McAMDlc)

def unregister():
    bpy.utils.unregister_class(McAMDlc)
    bpy.utils.unregister_class(OpenAddonPrefs)
    bpy.utils.unregister_class(MAIN_OT_SCRIPT_UI_ENUM_SWITCH)