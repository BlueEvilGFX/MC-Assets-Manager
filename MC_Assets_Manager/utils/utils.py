import os
import json
import bpy


#━━━━━━━━━━━━━━━    functions / classes    ━━━━━━━━━━━━━━━━━━━━━━━


class AddonPathManagement():

    #━━━━━━━━━━━━━━━    addonPath
    @staticmethod
    def getAddonPath():
        '''get addon main path'''
        file_path = os.path.realpath(__file__)
        utils_path = os.path.dirname(file_path)
        path = os.path.dirname(utils_path)
        return path

    #━━━━━━━━━━━━━━━    dlcs
    @classmethod
    def getInitPath(cls, dlc) -> tuple:
        '''get init file path[0] and check existence[1]'''
        path = os.path.join(cls.getAddonPath(), "files", "DLCs", dlc, "__init__.py")
        existence = os.path.exists(path)                                                #   init path & existence
        return path, existence

    @classmethod
    def getDlcMainJson(cls) -> os.path:
        '''get main dlc json file'''
        dlcJsonPath = os.path.join(cls.getAddonPath(), "files", "dlcs.json")            #   get main dlc json file
        return dlcJsonPath

    @classmethod
    def getDlcDirPath(cls) -> os.path:
        '''get path to the dlc directory of the addon'''
        dlcDirPath = os.path.join(cls.getAddonPath(), "files", "DLCs")                  #   get path to dlc dir
        return dlcDirPath

    @classmethod
    def getDlcList(cls) -> tuple:
        '''get list of dlcs'''
        dlcList = os.listdir(cls.getDlcDirPath())                                       #   get list of dlcs
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
        path = os.path.join(cls.getAddonPath(), "files", "own_presets")                 #   get path to own presets dir
        return path

    @classmethod
    def getOwnPresets(cls) -> list:
        '''get list of own presets'''
        ownAssetList = os.listdir(cls.getOwnPresetsDirPath())                           #   get list of own presets
        return ownAssetList

    #━━━━━━━━━━━━━━━    assets
    @classmethod
    def getOwnAssetsDirPath(cls) -> os.path:
        '''get path to own assets'''
        path = os.path.join(cls.getAddonPath(), "files", "own_assets")                  #   get path to own assets dir
        return path

    @classmethod
    def getOwnAssets(cls) -> list:
        '''get list of own assets'''
        ownAssetList = os.listdir(cls.getOwnAssetsDirPath())                            #   get list of own assets
        return ownAssetList

    @classmethod
    def getAssetsCategoriesJson(cls) -> os.path:
        '''get path to dlcs data.json file'''
        categoryJsonFile = os.path.join(cls.getAddonPath(), "files", "assetCategories.json")       #   get assets category json file
        return categoryJsonFile

    #━━━━━━━━━━━━━━━    rigs
    @classmethod
    def getOwnRigsDirPath(cls) -> os.path:
        '''get path to own rigs'''
        path = os.path.join(cls.getAddonPath(), "files", "own_rigs")                  #    get path to own rigs dir
        return path

    @classmethod
    def getOwnRigs(cls) -> list:
        '''get list of own rigs'''
        ownAssetList = os.listdir(cls.getOwnRigsDirPath())                            #   get list of own rigs
        return ownAssetList



class AddonReloadManagement:

    addonPath = AddonPathManagement.getAddonPath()
    dlcMainJson = AddonPathManagement.getDlcMainJson()

    #━━━━━━━━━━━━━━━    reload dlc json
    @classmethod
    def reloadDlcJson(cls) -> None:
        '''reload main dlc json file from addon'''
        dlcList = AddonPathManagement.getDlcList()   
        dlcJsonList = {}

        with open(cls.dlcMainJson) as mainJson:                                         #   open dlc main file -> retrieving all dlc data
            mainData = json.load(mainJson)
            for dlc in dlcList:
                dlcFile = AddonPathManagement.getDlcDataJson(dlc)

                with open(dlcFile, 'r') as dlcJson:                                     #   open dlc data file -> retrieving original data
                    data = json.load(dlcJson)                                           #   writing this data to dir dlcMainFile
                    dlcJsonList[dlc] = data

                    if mainData.get(dlc) is None:                                       #   if does not exist : newly added DLC
                        init_check = AddonPathManagement.getInitPath(dlc)[1]            #   if dlc is script based : deactivate
                        dlcJsonList[dlc]["active"] = False if init_check==True else True
                    else:
                        active = mainData[dlc]["active"]
                        dlcJsonList[dlc]["active"] = active                             #   use active status from before

        with open(cls.dlcMainJson, "w") as jsonFile:
            json.dump(dlcJsonList, jsonFile, indent=4)

    #━━━━━━━━━━━━━━━    reload dlc list
    @classmethod
    def reloadDlcList(cls) -> None:
        '''reload dlc ui list'''
        # get data
        dlc_list = bpy.context.scene.mcAssetsManagerProps.dlc_list                          #   get dlc_list property
        dlc_list.clear()

        #   reload dlc list from dlcs.json                                                      ━━━━━━━━━━━━━━━
        with open(cls.dlcMainJson, "r") as json_file:
            data = json.load(json_file)
                
            for dlc in data:
                item = dlc_list.add()                                                       #   add new entry to dlc list
                item.name = dlc                                                             #   set name
                item.type = data[dlc]["type"]                                               #   set type
                item.creator = data[dlc]["creator"]                                         #   set creator
                item.active = data[dlc]["active"]                                           #   set status
                item.version = data[dlc]["version"]                                         #   set version

    #━━━━━━━━━━━━━━━    reload preset list
    @classmethod
    def reloadPresetList(cls) -> None:
        '''reload preset ui list'''
        # get data - presets && DLCs                                   
        own_presets_list = AddonPathManagement.getOwnPresets()
        #   ━━━━━━━━━━━━━━━                                                                     ━━━━━━━━━━━━━━━
        dlc_dir = AddonPathManagement.getDlcDirPath()
        dlc_list = AddonPathManagement.getDlcList()
        preset_list = bpy.context.scene.mcAssetsManagerProps.preset_list                    #   get preset_list property
        preset_list.clear()
        
        #   add own presets
        for p in own_presets_list:
            item = preset_list.add()                                                        #   add file to preset_list 
            item.name = os.path.splitext(p)[0]                                              #   set name


        #   reload dlc presets from dlc presets[dlc_json_file]                                  ━━━━━━━━━━━━━━━
        with open(cls.dlcMainJson, "r") as json_file:
            data = json.load(json_file)

            for dlc in dlc_list:
                preset_dir_path = os.path.join(dlc_dir, dlc, "presets")                     #   get path to presets directory of dlc
                has_presets = os.path.exists(preset_dir_path)                               #   if dlc has presets

                if data[dlc]["active"] and has_presets:
                    pr_pa = os.path.join(cls.addonPath, "files", "DLCs", dlc, "presets")    #   get directory of preset dlc
                    presets = os.listdir(pr_pa)                                             #   get list of presets of the dlc

                    for p in presets:
                        if p.endswith(".blend"):
                            item = preset_list.add()                                        #   add preset to ui list
                            item.name = os.path.splitext(p)[0]                              #   set name
                            item.path = os.path.join(pr_pa, p)                              #   set path
                            item.icon = dlc + "_" + item.name                               #   set icon path [dlcName & preset.name]

    #━━━━━━━━━━━━━━━    reload asset list
    @classmethod
    def reloadAssetList(cls) -> None:
        '''reload asset ui list'''
        # get data - assets && DLCs                                   
        own_assets_list = AddonPathManagement.getOwnAssets()
        #   ━━━━━━━━━━━━━━━                                                                     ━━━━━━━━━━━━━━━
        dlc_dir = AddonPathManagement.getDlcDirPath()
        dlc_list = AddonPathManagement.getDlcList()
        asset_list = bpy.context.scene.mcAssetsManagerProps.asset_list                      #   get preset_list property
        asset_list.clear()
        
        #   add own assets
        for p in own_assets_list:
            item = asset_list.add()                                                         #   add file to preset_list 
            item.name = os.path.splitext(p)[0]                                              #   set name


        #   reload dlc assets from dlc assets[dlc_json_file]                                  ━━━━━━━━━━━━━━━
        with open(cls.dlcMainJson, "r") as json_file:
            data = json.load(json_file)

            for dlc in dlc_list:
                asset_dir_path = os.path.join(dlc_dir, dlc, "assets")                       #   get path to assets directory of dlc
                has_assets = os.path.exists(asset_dir_path)                                 #   if dlc has assets

                if data[dlc]["active"] and has_assets:
                    assetsJson = os.path.join(asset_dir_path, "assets.json")                #   get assets Json

                    with open(assetsJson, "r") as assets_json:
                        assets = json.load(assets_json)

                        for a in assets:
                            item = asset_list.add()                                         #   add preset to ui list
                            item.name = a                                                   #   set name
                            item.type = assets[a]["type"]                                   #   set collection or object
                            item.category = assets[a]["category"]                           #   set category
                            item.path = os.path.join(asset_dir_path, "assets.blend")        #   set path
                            item.icon = dlc + "_" + item.name                               #   set icon path [dlcName & asset.name]
        
    #━━━━━━━━━━━━━━━    reload rig list
    @classmethod
    def reloadRigList(cls) -> None:
        '''reload rig ui list'''
        # get data - assets && DLCs                                   
        own_assets_list = AddonPathManagement.getOwnRigs()
        #   ━━━━━━━━━━━━━━━                                                                     ━━━━━━━━━━━━━━━
        dlc_dir = AddonPathManagement.getDlcDirPath()
        dlc_list = AddonPathManagement.getDlcList()
        rig_list = bpy.context.scene.mcAssetsManagerProps.rig_list                          #   get preset_list property
        rig_list.clear()
        
        #   add own assets
        for p in own_assets_list:
            item = rig_list.add()                                                           #   add file to preset_list 
            item.name = os.path.splitext(p)[0]                                              #   set name


        #   reload dlc rigs from dlc assets[dlc_json_file]                                      ━━━━━━━━━━━━━━━
        with open(cls.dlcMainJson, "r") as json_file:
            data = json.load(json_file)

            for dlc in dlc_list:
                rig_dir_path = os.path.join(dlc_dir, dlc, "rigs")                           #   get path to rigs directory of dlc
                has_rigs = os.path.exists(rig_dir_path)                                     #   if dlc has rigs

                if data[dlc]["active"] and has_rigs:
                    # pr_pa = os.path.join(cls.addonPath, "files", "DLCs", dlc, "rigs")    #   get directory of rig dlc
                    rigs = os.listdir(rig_dir_path)                                             #   get list of rigs of the dlc

                    for p in rigs:
                        if p.endswith(".blend"):
                            item = rig_list.add()                                           #   add preset to ui list
                            item.name = os.path.splitext(p)[0]                              #   set name
                            item.path = os.path.join(rig_dir_path, p)                       #   set path
                            item.icon = dlc + "_" + item.name                               #   set icon path [dlcName & preset.name]