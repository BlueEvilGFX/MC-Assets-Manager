import bpy


#━━━━━━━━━━━━━━━    functions / classes    ━━━━━━━━━━━━━━━━━━━━━━━
class AddonPreferencesProperties:
    @classmethod
    def getAddonName(cls) -> str:
        return "[Minecraft Assets Manager]"

    @classmethod
    def getPackage(cls) -> str:
        return __package__.split(".")[0]

    @classmethod
    def getAddonPropAcces(cls) -> bpy:
        '''f'addon.{dlc_name}_propGroup'''
        addon = bpy.context.preferences.addons.get(cls.getPackage()).preferences
        return addon