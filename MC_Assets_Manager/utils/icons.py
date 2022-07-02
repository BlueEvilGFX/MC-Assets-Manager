import bpy
import os
import bpy.utils.previews
from . import utils

#━━━━━━━━━━━━━━━    functions    ━━━━━━━━━━━━━━━━━━━━━━

class ReadIcons:

    @staticmethod
    def readDLCIcons(pcoll):
        addon_path = utils.AddonPathManagement.getAddonPath()
        dlcDir = os.path.join(addon_path, "files", "DLCs")                              #   get path to DLCs

        for name in os.listdir(dlcDir):
            path = os.path.join(dlcDir, name, "icon.png")                               #   get path to icon.png
            if os.path.exists(path):
                pcoll.load(name, path, "IMAGE")

    @staticmethod
    def readPresetIcons(pcoll):
        addon_path = utils.AddonPathManagement.getAddonPath()
        dlcDir = os.path.join(addon_path, "files", "DLCs")                              #   get path to DLCs

        for name in os.listdir(dlcDir):
            icon_path = os.path.join(dlcDir, name, "presets", "icons")                  #   get path to icon directory
            
            if os.path.exists(icon_path):
                for icon in os.listdir(icon_path):
                    path = os.path.join(icon_path, icon)                                #   get path to icon
                    pcoll.load(name+"_"+os.path.splitext(icon)[0], path, "IMAGE")       #   load icon a: nameOfDLC_iconName
        
        own_icons_path = os.path.join(addon_path, "files", "own_presets", "icons")
        for icon in os.listdir(own_icons_path):
            path = os.path.join(own_icons_path, icon)                                   #   get path to icon
            pcoll.load("ownPreset_"+os.path.splitext(icon)[0], path, "IMAGE")           #   load icon a: ownPreset_iconName

    @staticmethod
    def readAssetIcons(pcoll):
        addon_path = utils.AddonPathManagement.getAddonPath()
        dlcDir = os.path.join(addon_path, "files", "DLCs")                              #   get path to DLCs

        for name in os.listdir(dlcDir):
            icon_path = os.path.join(dlcDir, name, "assets", "icons")                   #   get path to icon directory
            
            if os.path.exists(icon_path):
                for icon in os.listdir(icon_path):
                    path = os.path.join(icon_path, icon)                                #   get path to icon
                    pcoll.load(name+"_"+os.path.splitext(icon)[0], path, "IMAGE")       #   load icon a: nameOfDLC_iconName
        
        own_icons_path = os.path.join(addon_path, "files", "own_assets", "icons")
        for icon in os.listdir(own_icons_path):
            path = os.path.join(own_icons_path, icon)                                   #   get path to icon
            pcoll.load("ownAsset_"+os.path.splitext(icon)[0], path, "IMAGE")            #   load icon a: ownAsset_iconName

    @staticmethod
    def readRigIcons(pcoll):
        addon_path = utils.AddonPathManagement.getAddonPath()
        dlcDir = os.path.join(addon_path, "files", "DLCs")                              #   get path to DLCs

        for name in os.listdir(dlcDir):
            icon_path = os.path.join(dlcDir, name, "rigs", "icons")                   #   get path to icon directory
            
            if os.path.exists(icon_path):
                for icon in os.listdir(icon_path):
                    path = os.path.join(icon_path, icon)                                #   get path to icon
                    pcoll.load(name+"_"+os.path.splitext(icon)[0], path, "IMAGE")       #   load icon a: nameOfDLC_iconName
        
        own_icons_path = os.path.join(addon_path, "files", "own_rigs", "icons")
        for icon in os.listdir(own_icons_path):
            path = os.path.join(own_icons_path, icon)                                   #   get path to icon
            pcoll.load("ownRig_"+os.path.splitext(icon)[0], path, "IMAGE")              #   load icon a: ownRig_iconName

    @staticmethod
    def readBasicMcAMIcons(pcoll):
        addon_path = utils.AddonPathManagement.getAddonPath()
        iconsDir = os.path.join(addon_path, "icons")                                    #   get path to DLCs

        for icon in os.listdir(iconsDir):
            path = os.path.join(iconsDir, icon)                                         #   get path to icon  
            pcoll.load("McAM_"+os.path.splitext(icon)[0], path, "IMAGE")                #   load icon a: nameOfDLC_iconName


#━━━━━━━━━━━━━━━    decorator    ━━━━━━━━━━━━━━━━━━━━━━━


def reloadDLCIcons(placement):
    """"0 == before; 1 == afterwards"""
    def dec(fn):
        def wrapper(self, x):
            if placement == 1: func = fn(self, x)
            for pcoll in dlc_icon_collections.values():                                 #   remove all icons
                bpy.utils.previews.remove(pcoll)
            dlc_icon_collections.clear()
            pcoll = bpy.utils.previews.new()                                            #   create new icon pcoll
            ReadIcons.readDLCIcons(pcoll)
            dlc_icon_collections["DLCs"] = pcoll                                        #   assign to icon collection dictionary
            if placement == 0: func = fn(self, x)
            return func
        return wrapper
    return dec

#━━━━━━━━━━━━━━━

def reloadPresetIcons(placement):
    """"0 == before; 1 == afterwards"""
    def dec(fn):
        def wrapper(self, x):
            if placement == 1: func = fn(self, x)
            for pcoll in preset_icon_collections.values():                              #   remove all icons
                bpy.utils.previews.remove(pcoll)
            preset_icon_collections.clear()
            pcoll = bpy.utils.previews.new()                                            #   create new icon poll
            ReadIcons.readPresetIcons(pcoll)
            preset_icon_collections["Presets"] = pcoll                                  #   assign to icon collection dictionary
            if placement == 0: func = fn(self, x)
            return func
        return wrapper
    return dec

#━━━━━━━━━━━━━━━

def reloadAssetIcons(placement):
    """"0 == before; 1 == afterwards"""
    def dec(fn):
        def wrapper(self, x):
            if placement == 1: func = fn(self, x)
            for pcoll in asset_icon_collections.values():                               #   remove all icons
                bpy.utils.previews.remove(pcoll)
            asset_icon_collections.clear()
            pcoll = bpy.utils.previews.new()                                            #   create new icon poll
            ReadIcons.readAssetIcons(pcoll)
            asset_icon_collections["Assets"] = pcoll                                    #   assign to icon collection dictionary
            if placement == 0: func = fn(self, x)
            return func
        return wrapper
    return dec

#━━━━━━━━━━━━━━━

def reloadRigIcons(placement):
    """"0 == before; 1 == afterwards"""
    def dec(fn):
        def wrapper(self, x):
            if placement == 1: func = fn(self, x)
            for pcoll in rig_icon_collections.values():                                 #   remove all icons
                bpy.utils.previews.remove(pcoll)
            rig_icon_collections.clear()
            pcoll = bpy.utils.previews.new()                                            #   create new icon poll
            ReadIcons.readRigIcons(pcoll)
            rig_icon_collections["Rigs"] = pcoll                                        #   assign to icon collection dictionary
            if placement == 0: func = fn(self, x)
            return func
        return wrapper
    return dec

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

basicMCAM_icon_collection = {}
dlc_icon_collections = {}
preset_icon_collections = {}
asset_icon_collections = {}
rig_icon_collections = {}

def register():
    pcoll = bpy.utils.previews.new()
    ReadIcons.readBasicMcAMIcons(pcoll)
    basicMCAM_icon_collection["McAM"] = pcoll

    pcoll = bpy.utils.previews.new()
    ReadIcons.readDLCIcons(pcoll)
    dlc_icon_collections["DLCs"] = pcoll

    pcoll = bpy.utils.previews.new()
    ReadIcons.readPresetIcons(pcoll)
    preset_icon_collections["Presets"] = pcoll

    pcoll = bpy.utils.previews.new()
    ReadIcons.readAssetIcons(pcoll)
    asset_icon_collections["Assets"] = pcoll

    pcoll = bpy.utils.previews.new()
    ReadIcons.readAssetIcons(pcoll)
    asset_icon_collections["Rigs"] = pcoll 


def unregister():
    for pcoll in basicMCAM_icon_collection.values():
        bpy.utils.previews.remove(pcoll)

    for pcoll in dlc_icon_collections.values():
        bpy.utils.previews.remove(pcoll)

    for pcoll in preset_icon_collections.values():
        bpy.utils.previews.remove(pcoll)
    
    for pcoll in asset_icon_collections.values():
        bpy.utils.previews.remove(pcoll)

    for pcoll in rig_icon_collections.values():
        bpy.utils.previews.remove(pcoll)

    basicMCAM_icon_collection.clear()
    dlc_icon_collections.clear()
    preset_icon_collections.clear()
    asset_icon_collections.clear()
    rig_icon_collections.clear()