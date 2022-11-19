import os

import bpy


class AddonPathsIntern:
    """
    this class is used to set the constants below:
    - UTILS_DIR
    - CORE_DIR
    - ADDON_DIR
    - PACKAGE
    """

    @staticmethod
    def get_utils_dir() -> os.path:
        current_file = os.path.realpath(__file__)
        return os.path.dirname(current_file)

    @staticmethod
    def get_core_dir() -> os.path:
        return os.path.dirname(UTILS_DIR)

    @staticmethod
    def get_addon_dir() -> os.path:
        """
        returns the main addon path: .../MC_Assets_Manager/
        """
        return os.path.dirname(CORE_DIR)

    @staticmethod
    def get_addon_name() -> str:
        return os.path.basename(ADDON_DIR)

    @staticmethod
    def get_resources_dir() -> os.path:
        return os.path.join(ADDON_DIR, "resources")

    @staticmethod
    def get_resources_icon_dir() -> os.path:
        return os.path.join(RESOURCES_DIR, "icons")


#━━━━━━━━━━━━━━━    constants    ━━━━━━━━━━━━━━━━━━━━━━━━━━
UTILS_DIR = AddonPathsIntern.get_utils_dir()
CORE_DIR = AddonPathsIntern.get_core_dir()
ADDON_DIR = AddonPathsIntern.get_addon_dir()
PACKAGE = AddonPathsIntern.get_addon_name()
RESOURCES_DIR = AddonPathsIntern.get_resources_dir()
RESOURCES_ICON_DIR = AddonPathsIntern.get_resources_icon_dir()

# user assets
USER_ASSETS = "user_assets"
USER_PRESETS = "user_presets"
USER_RIGS = "user_rigs"

# dlc assets
ASSETS = "assets"
PRESETS = "presets"
RIGS = "rigs"

DLCS = "dlcs"

# name of the property inside the main property group of McAM
MCAM_PROP_GROUP = "mc_assets_manager_props"
UI_LIST_ASSETS = "asset_list"
UI_LIST_PRESETS = "preset_list"
UI_LIST_RIGS = "rig_list"
UI_LIST_DLCS = "dlc_list"

# icons
DLC_MAIN_ICON = "dlc"
DLC_ASSET_ICON = "dlc_asset"
DLC_PRESET_ICON = "dlc_preset"
DLC_RIG_ICON = "dlc_rig"

MCAM_ICON = "McAM_"

#━━━━━━━━━━━━━━━    getter: addon preferences properties    
def get_addon_properties() -> bpy:
    """
    gives access to the addon properties\n
    add .main_props if you are using the addon internal properties
    """
    return bpy.context.preferences.addons.get(PACKAGE).preferences

#━━━━━━━━━━━━━━━    getter: resources    
def get_resources_icons() -> list:
    """
    returns a list with all the mcam icons without extension
    """
    dir = RESOURCES_ICON_DIR
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".png")]

#━━━━━━━━━━━━━━━    getter: dirs    ━━━━━━━━━━━━━━━━━━━━━━━
def get_storage_dir() -> os.path:
    """
    returns the path to the storage dir:\n
    either default or set through addon preferences
    """
    # try:
    #     storage_dir = ADDON_PROP_ACCESS.preferences.main_props.storage_path
    # except:
    #     storage_dir = ""

    # if storage_dir == "" or storage_dir is None:
    #     return os.path.join(ADDON_DIR, "storage")
    # return storage_dir
    return os.path.join(ADDON_DIR, "storage")

#━━━━━━━━━━━━━━━    user files
def get_user_sub_asset_dir(asset_type) -> os.path:
    """
    asset_type: USER_ASSETS | USER_PRESETS | USER_RIGS -> returns the path
    to its storage sub dir
    """
    return os.path.join(get_storage_dir(), asset_type)

def get_user_sub_assets(asset_type) -> list:
    """
    asset_type: USER_ASSETS | USER_PRESETS | USER_RIGS -> returns a list
    with all the user 'assets' without extension
    """
    dir = get_user_sub_asset_dir(asset_type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".blend")]

def get_user_sub_icon_dir(asset_type) -> os.path:
    """
    asset_type: USER_ASSETS | USER_PRESETS | USER_RIGS -> returns the path
    to its storage sub icon dir
    """
    return os.path.join(get_user_sub_asset_dir(asset_type), "icons")

def get_user_sub_icons(asset_type) -> list:
    """
    returns a list with all the user sub icons without extension
    """
    dir = get_user_sub_icon_dir(asset_type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".png")]

#━━━━━━━━━━━━━━━    dlc files
def get_dlc_dir() -> os.path:
    """
    returns the dlc dir based on the storage
    """
    return os.path.join(get_storage_dir(), "dlcs")

def get_dlc_sub_dir(dlc) -> os.path:
    """
    returns the path to the dlc with the given name
    """
    return os.path.join(get_dlc_dir(), dlc)

def get_dlc_json() -> os.path:
    """
    return the path to the dlc.json which stores following data:
    - name of dlcs installed
    - active status
    - version
    - creator
    """
    return os.path.join(RESOURCES_DIR, "dlcs.json")

def get_dlc_init(dlc) -> os.path:
    """
    takes a dlc name as input variable and returns its __init__.py file path\n
    returns the path if it exists, else it returns an empty string
    """
    init_path = os.path.join(get_dlc_dir(), dlc, "__init__.py")
    if os.path.exists(init_path):
        return init_path
    return ""

def get_dlcs() -> list:
    """
    returns all installed dlc names  in a list
    """
    dir = get_dlc_dir()
    return [dlc for dlc in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, dlc))]

def get_dlc_sub_json(dlc) -> os.path:
    """
    returns the path to the data.json file of a dlc
    """
    return os.path.join(get_dlc_dir(), dlc, "data.json")

def get_dlc_sub_assets_dir(dlc, asset_type) -> os.path:
    """
    takes the dlc name and its asset asset_type as input
    asset_type: ASSETS | PRESETS | RIGS -> returns the path
    to its storage sub dir
    returns "" if path does not exist
    """
    assets_dir = os.path.join(get_dlc_dir(), dlc, asset_type)
    if os.path.exists(assets_dir):
        return assets_dir
    return ""

def get_dlc_sub_assets(dlc, asset_type) -> list:
    """
    takes the dlc name and its asset asset_type as input
    asset_type: ASSETS | PRESETS | RIGS -> returns a list
    with all the user sub assets without extension
    returns ""  if path does not exist
    """
    dir = get_dlc_sub_assets_dir(dlc, asset_type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".blend")]

def get_dlc_sub_assets_icon_dir(dlc ,asset_type) -> os.path:
    """
    asset_type: ASSETS | PRESETS | RIGS -> returns the path
    to its storage sub icon dir
    -> returns "" if path path does not exist
    """
    icon_dir = os.path.join(get_dlc_sub_assets_dir(dlc, asset_type), "icons")
    if os.path.exists(icon_dir):
        return icon_dir
    return ""

def get_dlc_sub_assets_icons(dlc, asset_type) -> list:
    """
    asset_type: ASSETS | PRESETS | RIGS -> returns a list
    returns a list with all the user sub icons without extension\n
    returns an empty list if the path does not exist
    """
    icon_dir = get_dlc_sub_assets_icon_dir(dlc, asset_type)
    if not os.path.exists(icon_dir):
        return []

    dir = get_dlc_sub_assets_icon_dir(dlc, asset_type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".png")]


def get_dlc_asset_categories() -> os.path:
    """
    returns the path to the asset_categories.json file
    """
    return os.path.join(RESOURCES_DIR, "asset_categories.json")

def get_dlc_sub_assets_json(dlc, asset_type) -> os.path:
    """
    asset_type: ASSETS | PRESETS | RIGS -> returns the path
    to the assets json of a dlc\n
    returns "" if it doesnt exist
    """
    assets_json = os.path.join(get_dlc_dir(), dlc, asset_type, "assets.json")
    if os.path.exists(assets_json):
        return assets_json
    return ""

def get_dlc_sub_assets_blend(dlc, asset_type) -> os.path:
    """
    asset_type: ASSETS | PRESETS | RIGS -> returns the path
    to the assets blend file of a dlc\n
    returns "" if it doesnt exist
    """
    assets_blend = os.path.join(get_dlc_dir(), dlc, asset_type, "assets.blend")
    if os.path.exists(assets_blend):
        return assets_blend
    return ""
