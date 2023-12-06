import os
import bpy


class AssetTypes:
    # USER
    USER_ASSETS = 'user_assets'
    USER_PRESETS = 'user_presets'
    USER_RIGS = 'user_rigs'

    # DLC
    ASSETS = 'assets'
    PRESETS = 'presets' 
    RIGS = 'rigs'

    # dlcs
    DLCS = 'dlcs'


class IconTypes:
    DLC_MAIN_ICON = 'dlc'
    DLC_ASSET_ICON = 'dlc_asset'
    DLC_PRESET_ICON = 'dlc_preset'
    DLC_RIG_ICON = 'dlc_rig'


class PropertyGroups:
    MCAM_PROP_GROUP = "mc_assets_manager_props"
    UI_LIST_ASSETS = "asset_list"
    UI_LIST_PRESETS = "preset_list"
    UI_LIST_RIGS = "rig_list"
    UI_LIST_DLCS = "dlc_list"



class PathConstants:
    """
    Paths to addon main paths.
    """
    ADDON_DIRECTORY = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..')
    )
    PACKAGE = os.path.basename(ADDON_DIRECTORY)
    RESOURCES_DIRECTORY = os.path.join(ADDON_DIRECTORY, 'resources')
    RESOURCES_ICON_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, 'icons')
    STORAGE_DIRECTORY = os.path.join(ADDON_DIRECTORY, 'storage')


class McAM:
    @staticmethod
    def get_addon_properties() -> bpy.types.AddonPreferences:
        """
        Add .main_props if you are using the addon internal properties

        :return: AddonPreferences of McAM
        """
        return bpy.context.preferences.addons.get(PathConstants.PACKAGE).preferences
    
    @staticmethod
    def get_resource_icons() -> list:
        """
        :return: list with all mcam icons without extension.
        """
        return [
            os.path.splitext(icon)[0] 
            for icon in os.listdir(PathConstants.RESOURCES_ICON_DIRECTORY)
            if icon.endswith('.png')    
        ]
    
    @staticmethod
    def get_github_icon_directory() -> str:
        """
        :return: path to the github icon directory
        """
        return os.path.join(PathConstants.RESOURCES_DIRECTORY, 'github_icons')
    
    @staticmethod
    def get_github_icon_list() -> str:
        """
        :return: list with icons without extensions
        """
        return [
            os.path.splitext(icon)[0] 
            for icon in os.listdir(McAM.get_github_icon_directory())
            if icon.endswith('.png')
        ]

    @staticmethod
    def get_dlc_main_json() -> str:
        """
        :return: path to main_json which contains installed DLCs, status etc.
        """
        return os.path.join(PathConstants.RESOURCES_DIRECTORY, 'dlcs.json')


class User:
    @staticmethod
    def get_sub_asset_directory(asset_type: AssetTypes) -> str:
        """
        :param asset_type: Element in AssetTypes
        :return: path to storage sub directory
        """
        return os.path.join(PathConstants.STORAGE_DIRECTORY, asset_type)
        
    @staticmethod
    def get_sub_asset_list(asset_type: AssetTypes) -> list:
        """
        :param asset_type: Element in AssetTypes
        :return: list with assets without extension
        """
        dir = User.get_sub_asset_directory(asset_type)
        return [
            os.path.splitext(icon)[0] 
            for icon in os.listdir(dir)
            if icon.endswith('.blend')
        ]

    @staticmethod
    def get_sub_icon_directory(asset_type: AssetTypes) -> str:
        """
        :param asset_type: Element in AssetTypes
        :return: path to storage sub icon directory
        """
        return os.path.join(User.get_sub_asset_directory(asset_type), 'icons')

    @staticmethod
    def get_sub_icon_list(asset_type: AssetTypes) -> list:
        """
        :param asset_type: Element in AssetTypes
        :return: list with icons without extensions
        """
        dir = User.get_sub_icon_directory(asset_type)
        return [
            os.path.splitext(icon)[0] 
            for icon in os.listdir(dir)
            if icon.endswith('.png')
        ]
    
    @staticmethod
    def get_sub_asset_blend(name: str, asset_type: AssetTypes):
        """
        :param name: asset name
        :param asset_type: Element in AssetTypes
        :return: path to asset blend file from given asset with name
        """
        return os.path.join(User.get_sub_asset_directory(asset_type), name + ".blend")


class DLC:
    @staticmethod
    def get_directory() -> str:
        """
        :return: path to storage dlc directory
        """
        return os.path.join(PathConstants.STORAGE_DIRECTORY, 'dlcs')
    
    @staticmethod
    def get_sub_directory(dlc: str) -> str:
        """
        :param dlc: dlc name
        :return: path to directory of the given dlc
        """
        return os.path.join(DLC.get_directory(), dlc)

    @staticmethod
    def get_sub_init(dlc: str) -> str:
        """
        :param dlc: dlc name
        :return: path to init file of given dlc, return '' if not existent
        """
        init_path = os.path.join(DLC.get_sub_directory(dlc), '__init__.py')
        return init_path if os.path.exists(init_path) else ''


    @staticmethod
    def get_dlcs_list() -> list:
        """
        :return: names of all installed dlcs"""
        return os.listdir(DLC.get_directory())

    @staticmethod
    def get_sub_json(dlc: str) -> str:
        """
        :param dlc: dlc name
        :return: path to dlc json which contains information about given dlc
        """
        return os.path.join(DLC.get_sub_directory(dlc), 'data.json')
    
    @staticmethod
    def get_sub_asset_directory(dlc: str, asset_type: AssetTypes) -> str:
        """
        :param dlc: dlc name
        :param asset_type: Element in AssetTypes
        :return: path to asset directory of given dlc, return '' if not existent 
        """
        asset_directory = os.path.join(DLC.get_sub_directory(dlc), asset_type)
        return asset_directory if os.path.exists(asset_directory) else ''

    @staticmethod
    def get_sub_asset_list(dlc: str, asset_type: AssetTypes) -> list:
        """
        :param dlc: dlc name
        :param asset_type: Element in AssetTypes
        :return: list with assets without extensions
        """
        dir = DLC.get_sub_asset_directory(dlc, asset_type)
        return [
            os.path.splitext(icon)[0]
            for icon in os.listdir(dir)
            if icon.endswith('.blend')
        ]

    @staticmethod
    def get_sub_main_icon_directory(dlc: str) -> str:
        """
        :return: path to storage sub main icon of dlc directory, return '' if not existent
        """
        icon_dir = os.path.join(DLC.get_sub_directory(dlc), "icons")
        if os.path.exists(icon_dir):
            return icon_dir
        return ''
    
    @staticmethod
    def get_sub_main_icon_list(dlc:str) -> list:
        """
        :param dlc: dlc name
        :return: list with icons without extensions
        """
        icon_dir = DLC.get_sub_main_icon_directory(dlc)
        if icon_dir == '':
            return []
        
        return [
            os.path.splitext(icon)[0]
            for icon in os.listdir(icon_dir)
            if icon.endswith(".png")
        ]

    @staticmethod
    def get_sub_icon_directory(dlc: str, asset_type: AssetTypes) -> str:
        """
        :param asset_type: Element in AssetTypes
        :return: path to storage sub icon of dlc and asset directory, return '' if not existent
        """
        icon_dir = os.path.join(DLC.get_sub_asset_directory(dlc, asset_type), "icons")
        if os.path.exists(icon_dir):
            return icon_dir
        return ''

    @staticmethod
    def get_sub_icon_list(dlc: str, asset_type: AssetTypes) -> list:
        """
        :param dlc: dlc name
        :param asset_type: Element in AssetTypes
        :return: list with icons without extensions
        """
        icon_dir = DLC.get_sub_icon_directory(dlc, asset_type)
        if icon_dir == '':
            return []
        
        return [
            os.path.splitext(icon)[0]
            for icon in os.listdir(icon_dir)
            if icon.endswith(".png")
        ]

    @staticmethod
    def get_asset_categories_json() -> str:
        """
        :return: path to asset_categories.json
        """
        return os.path.join(PathConstants.RESOURCES_DIRECTORY, 'asset_categories.json')

    @staticmethod
    def get_sub_asset_json(dlc: str, asset_type:AssetTypes) -> str:
        """
        :param dlc: dlc name
        :param asset_type: Element in AssetTypes
        :return: path to asset json from given dlc, return '' if not existent
        """
        asset_json = os.path.join(DLC.get_sub_asset_directory(dlc, asset_type), 'assets.json')
        return asset_json if os.path.exists(asset_json) else ''

    @staticmethod
    def get_sub_asset_blend(dlc: str, asset_type: AssetTypes):
        """
        :param dlc: dlc name
        :param asset_type: Element in AssetTypes
        :return: path to asset blend file from given dlc and asset, return '' if not existent
        """
        assets_blend = os.path.join(DLC.get_sub_asset_directory(dlc, asset_type), 'assets.blend')
        return assets_blend if os.path.exists(assets_blend) else ''