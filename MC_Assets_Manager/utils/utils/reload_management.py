import os
import json
import bpy
from .path_management import AddonPathManagement

#━━━━━━━━━━━━━━━    functions / classes    ━━━━━━━━━━━━━━━━━━━━━━━

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
                        dlcJsonList[dlc]["active"] = True
                        # init_check = AddonPathManagement.getInitPath(dlc)[1]            #   if dlc is script based : deactivate
                        # dlcJsonList[dlc]["active"] = False if init_check==True else True
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
        addon_path = AddonPathManagement.getAddonPath()
        icon_dir = os.path.join(addon_path, "files", "own_presets", "icons")
        icons = [icon for icon in os.listdir(icon_dir)]
        for p in own_presets_list:
            item = preset_list.add()                                                        #   add file to preset_list 
            item.name = os.path.splitext(p)[0]                                              #   set name
            if item.name+".png" in icons:                                                   #   set to $$$ if icon exists
                item.path = "$$$"


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
        addon_path = AddonPathManagement.getAddonPath()
        icon_dir = os.path.join(addon_path, "files", "own_assets", "icons")
        icons = [icon for icon in os.listdir(icon_dir)]
        for p in own_assets_list:
            item = asset_list.add()                                                         #   add file to preset_list 
            item.name = os.path.splitext(p)[0]                                              #   set name
            if item.name+".png" in icons:                                                   #   set to $$$ if icon exists
                item.path = "$$$"

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
        own_rig_list = AddonPathManagement.getOwnRigs()
        #   ━━━━━━━━━━━━━━━                                                                     ━━━━━━━━━━━━━━━
        dlc_dir = AddonPathManagement.getDlcDirPath()
        dlc_list = AddonPathManagement.getDlcList()
        rig_list = bpy.context.scene.mcAssetsManagerProps.rig_list                          #   get preset_list property
        rig_list.clear()
        
        #   add own rigs
        addon_path = AddonPathManagement.getAddonPath()
        icon_dir = os.path.join(addon_path, "files", "own_rigs", "icons")
        icons = [icon for icon in os.listdir(icon_dir)]
        for p in own_rig_list:
            item = rig_list.add()                                                           #   add file to preset_list 
            file_name = os.path.splitext(p)[0]                                              #   get whole file_name
            if "&&" in file_name:                                                           #   check if collection restriction
                item.name, item.collection = file_name.split("&&")                          #   set the collection to append
            else:
                item.name = file_name
            if file_name+".png" in icons:                                                   #   set to $$$ if icon exists
                item.path = "$$$"

        #   reload dlc rigs from dlc assets[dlc_json_file]                                      ━━━━━━━━━━━━━━━
        with open(cls.dlcMainJson, "r") as json_file:
            data = json.load(json_file)

            for dlc in dlc_list:
                rig_dir_path = os.path.join(dlc_dir, dlc, "rigs")                           #   get path to rigs directory of dlc
                has_rigs = os.path.exists(rig_dir_path)                                     #   if dlc has rigs

                if data[dlc]["active"] and has_rigs:
                    rigs = os.listdir(rig_dir_path)                                         #   get list of rigs of the dlc

                    for p in rigs:
                        if p.endswith(".blend"):
                            item = rig_list.add()                                           #   add preset to ui list
                            item.path = os.path.join(rig_dir_path, p)                       #   set path
                            file_name = os.path.splitext(p)[0]                              #   get whole file_name
                            if "&&" in file_name:                                           #   check if collection restriction
                                item.name, item.collection = file_name.split("&&")          #   set the collection to append
                            else:
                                item.name = file_name
                            item.icon = f'{dlc}_{file_name}'