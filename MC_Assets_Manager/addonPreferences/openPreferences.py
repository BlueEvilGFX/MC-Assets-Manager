import bpy
import addon_utils
from ..utils import utils

class OpenAddonPrefs(bpy.types.Operator):
    bl_idname = "mcam.openaddonprefs"
    bl_label = ""
    bl_description = "opens the user preferences for this addon"

    def execute(self, context):
        search = [addon.bl_info.get("name") for addon in addon_utils.modules() if addon.bl_info['name'] == utils.AddonPreferencesProperties.getAddonName()][0]
        package = utils.AddonPreferencesProperties.getPackage()
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers['WinMan']['addon_search'] = search
        bpy.ops.preferences.addon_expand(module = package)
        
        prefProps = utils.AddonPreferencesProperties.getAddonPropAcces()
        prefProps.menu = "2"
        prefProps.online_menu = "1"
        from ..utils.github_dlcs.operators import set_news
        set_news(False)
        return {'FINISHED'}