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


#━━━━━━━━━━━━━━━    constants    ━━━━━━━━━━━━━━━━━━━━━━━━━━
UTILS_DIR = AddonPathsIntern.get_utils_dir()
CORE_DIR = AddonPathsIntern.get_core_dir()
ADDON_DIR = AddonPathsIntern.get_addon_dir()
PACKAGE = AddonPathsIntern.get_addon_name()
ADDON_PROP_ACCESS = bpy.context.preferences.addons.get(PACKAGE).preferences

USER_ASSETS = "user_assets"
USER_PRESETS = "uer_presets"
USER_RIGS = "user_rigs"

ASSETS = "assets"
PRESETS = "presets"
RIGS = "rigs"

# name of the property inside the main property group of McAM
MCAM_PROP_GROUP = "mc_assets_manager_props"
UI_LIST_ASSETS = "asset_list"
UI_LIST_PRESETS = "preset_list"
UI_LIST_RIGS = "rig_list"


#━━━━━━━━━━━━━━━    getter: dirs    ━━━━━━━━━━━━━━━━━━━━━━━
def get_storage_dir() -> os.path:
    """
    returns the path to the storage dir:\n
    either default or set through addon preferences
    """
    addon = bpy.context.preferences.addons.get()
    try:
        storage_dir = addon.preferences.main_props.storage_path
    except:
        storage_dir = ""

    if storage_dir == "" or storage_dir is None:
        return os.pah.join(ADDON_DIR, "storage")
    return storage_dir

#━━━━━━━━━━━━━━━    user files
def get_user_sub_dir(type) -> os.path:
    """
    type: USER_ASSETS | USER_PRESETS | USER_RIGS -> returns the path
    to its storage sub dir
    """
    return os.path.join(get_storage_dir(), type)

def get_user_sub_assets(type) -> list:
    """
    type: USER_ASSETS | USER_PRESETS | USER_RIGS -> returns a list
    with all the user 'assets' without extension
    """
    dir = get_user_sub_dir(type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".blend")]

def get_user_sub_icon_dir(type) -> os.path:
    """
    type: USER_ASSETS | USER_PRESETS | USER_RIGS -> returns the path
    to its storage sub icon dir
    """
    return os.path.join(get_user_sub_dir(type), "icons")

def get_user_sub_icons(type) -> list:
    """
    returns a list with all the user sub icons without extension
    """
    dir = get_user_sub_icon_dir(type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".png")]

#━━━━━━━━━━━━━━━    dlc files
def get_dlc_dir() -> os.path:
    """
    returns the dlc dir based on the storage
    """
    return os.path.join(get_storage_dir(), "dlcs")

def get_dlc_json() -> os.path:
    """
    return the path to the dlc.json which stores following data:
    - name of dlcs installed
    - active status
    - version
    - creator
    """
    return os.path.join(get_storage_dir(), "dlcs.json")

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

def get_dlc_sub_files_dir(dlc, type) -> os.path:
    """
    takes the dlc name and its asset type as input
    type: ASSETS | PRESETS | RIGS -> returns the path
    to its storage sub dir
    returns "" if path does not exist
    """
    assets_dir = os.path.join(get_dlc_dir(), dlc, type)
    if os.path.exists(assets_dir):
        return assets_dir
    return ""

def get_dlc_sub_assets(dlc, type) -> list:
    """
    takes the dlc name and its asset type as input
    type: ASSETS | PRESETS | RIGS -> returns a list
    with all the user sub assets without extension
    returns ""  if path does not exist
    """
    dir = get_dlc_sub_files_dir(dlc, type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".blend")]

def get_dlc_sub_assets_icon_dir(dlc ,type) -> os.path:
    """
    type: ASSETS | PRESETS | RIGS -> returns the path
    to its storage sub icon dir
    """
    return os.path.join(get_dlc_sub_files_dir(dlc, type), "icons")

def get_dlc_sub_assets_icons(dlc, type) -> list:
    """
    type: ASSETS | PRESETS | RIGS -> returns a list
    returns a list with all the user sub icons without extension
    """
    dir = get_dlc_sub_assets_icon_dir(dlc, type)
    return [os.path.splitext(icon)[0] for icon in os.listdir(dir)
            if icon.endswith(".png")]


def get_asset_categories() -> os.path:
    """
    returns the path to the asset_categories.json file
    """
    return os.path.join(get_storage_dir(), "asset_categories.json")
