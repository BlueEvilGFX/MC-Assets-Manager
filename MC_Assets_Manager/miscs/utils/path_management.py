import os
import bpy

#━━━━━━━━━━━━━━━    functions / classes    ━━━━━━━━━━━━━━━━━━━━━━━
class AddonPathManagement:

    #━━━━━━━━━━━━━━━    addonPath / files path
    @staticmethod
    def getAddonPath():
        '''get addon main path'''
        file_path = os.path.realpath(__file__)
        sub_utils_path = os.path.dirname(file_path)
        utils_path = os.path.dirname(sub_utils_path)
        path = os.path.dirname(utils_path)
        return path

    @classmethod
    def getStorageDirPath(cls):
        '''get files dir path'''
        addon = bpy.context.preferences.addons.get("MC_Assets_Manager")
        try:
            storage_path = addon.preferences.main_props.storage_path
        except:
            storage_path = ""

        if storage_path == "" or storage_path is None:
            return os.path.join(cls.getAddonPath(), "files")
        return storage_path

    #━━━━━━━━━━━━━━━    dlcs
    @classmethod
    def getDLCInitPath(cls, dlc) -> tuple:
        '''get init file path[0] and check existence[1]'''
        path = os.path.join(cls.getStorageDirPath(), "DLCs", dlc, "__init__.py")
        existence = os.path.exists(path)                                                #   init path & existence
        return path, existence

    @classmethod
    def getDlcMainJson(cls) -> os.path:
        '''get main dlc json file'''
        dlcJsonPath = os.path.join(cls.getStorageDirPath(), "dlcs.json")                  #   get main dlc json file
        return dlcJsonPath

    @classmethod
    def getDlcDirPath(cls) -> os.path:
        '''get path to the dlc directory of the addon'''
        dlcDirPath = os.path.join(cls.getStorageDirPath(), "DLCs")                        #   get path to dlc dir
        return dlcDirPath

    @classmethod
    def getDlcList(cls) -> list:
        '''get list of dlcs'''
        path = cls.getDlcDirPath()
        #   gets only list of directories
        dlcList = [dlc for dlc in os.listdir(path) if os.path.isdir(os.path.join(path, dlc))]
        return dlcList

    @classmethod
    def getDlcDataJson(cls, dlc) -> os.path:
        '''get path to dlcs data.json file'''
        dlcDataJson = os.path.join(cls.getDlcDirPath(), dlc, "data.json")               #   get dlcs data.json file
        return dlcDataJson

    #━━━━━━━━━━━━━━━    presets
    @classmethod
    def getOwnPresetsDirPath(cls) -> os.path:
        '''get path to own presets'''
        path = os.path.join(cls.getStorageDirPath(), "own_presets")                       #   get path to own presets dir
        return path

    @classmethod
    def getOwnPresets(cls) -> list:
        '''get list of own presets'''
        dirList = os.listdir(cls.getOwnPresetsDirPath())
        ownPresetList = [preset for preset in dirList if preset.endswith(".blend")]     #   get list of own presets
        return ownPresetList

    #━━━━━━━━━━━━━━━    assets
    @classmethod
    def getOwnAssetsDirPath(cls) -> os.path:
        '''get path to own assets'''
        path = os.path.join(cls.getStorageDirPath(), "own_assets")                        #   get path to own assets dir
        return path

    @classmethod
    def getOwnAssets(cls) -> list:
        '''get list of own assets'''
        dirList = os.listdir(cls.getOwnAssetsDirPath())
        ownAssetList = [asset for asset in dirList if asset.endswith(".blend")]         #   get list of own assets
        return ownAssetList

    @classmethod
    def getAssetsCategoriesJson(cls) -> os.path:
        '''get path to dlcs data.json file'''
        categoryJsonFile = os.path.join(cls.getStorageDirPath(), "assetCategories.json")  #   get assets category json file
        return categoryJsonFile

    #━━━━━━━━━━━━━━━    rigs
    @classmethod
    def getOwnRigsDirPath(cls) -> os.path:
        '''get path to own rigs'''
        path = os.path.join(cls.getStorageDirPath(), "own_rigs")                          #    get path to own rigs dir
        return path

    @classmethod
    def getOwnRigs(cls) -> list:
        '''get list of own rigs'''
        dirList = os.listdir(cls.getOwnRigsDirPath())
        ownRigList = [rig for rig in dirList if rig.endswith(".blend")]                 #   get list of own assets
        return ownRigList