import bpy

#━━━━━━━━━━━━━━━    constant variables     ━━━━━━━━━━━━━━━━━━━━━━━

ADDON_NAME = "[Minecraft Assets Manager]"
PACKAGE = __package__.split(".")[0]

#━━━━━━━━━━━━━━━    functions / classes    ━━━━━━━━━━━━━━━━━━━━━━━

class AddonPreferencesProperties:
    @staticmethod
    def getAddonName() -> str:
        return ADDON_NAME

    @staticmethod
    def getPackage() -> str:
        return PACKAGE

    @staticmethod
    def getAddonPropAccess() -> bpy:
        '''f'addon.{dlc_name}_propGroup'''
        return bpy.context.preferences.addons.get(PACKAGE).preferences