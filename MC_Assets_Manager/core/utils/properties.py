import importlib
import json
import traceback

import bpy
from bpy.props import *
from bpy.types import PropertyGroup

from . import paths, reload


class UpdateFunctionsIntern:
    """
    this class contains the update functions for the property groups
    """
    @staticmethod
    def update_active(self,context):
        """
        function that will re-set the active statuses of the dlc.json file
        and the properties inside blender.
        """
        dlc_name = self.name
        dlc_json = paths.McAM.get_dlc_main_json()
        
        with open(dlc_json, "r") as file:
            data = json.load(file)
        
        init_path = paths.DLC.get_sub_init(dlc_name)
    	
        # dlc has a script and is active
        if init_path and data[dlc_name]["active"] == True:
            try:
                locals()[dlc_name] = importlib.import_module(
                    name = f'.storage.dlcs.{dlc_name}',
                    package = paths.PathConstants.PACKAGE
                    )

                # register / unregister DLCs
                try:
                    if self.active:
                        locals()[dlc_name].register()
                    else:
                        locals()[dlc_name].unregister()
                except:
                    # most likely if blender starts and sth unregistered cannot
                    # be unregistered at all
                    pass

                # blenders prop dlc status value
                data[dlc_name]["active"] = self.active
                
            except Exception:
                print(traceback.format_exc())
                # error -> set active status to False
                if self.active:
                    self.active = False
                data[dlc_name]["active"] = False
        else:
            data[dlc_name]['active'] = self.active

        # write active status to json file
        with open(dlc_json, "w") as file:
            json.dump(data, file, indent=4)  

        reload.reload_addon_preferences()
        reload.reload_asset_list()
        reload.reload_preset_list()
        reload.reload_rig_list()

    @staticmethod
    def scan_ui_dlc(self, context):
        """
        function that returns the active scripted DLCs
        as enum items.
        """
        dlc_json = paths.McAM.get_dlc_main_json()
    
        with open(dlc_json, "r") as json_file:
            data = json.load(json_file)
            enum = []
            for dlc in data:
                if paths.DLC.get_sub_init(dlc)and data[dlc]["active"]:
                    enum_item = (dlc, dlc, '')
                    enum.append(enum_item)
        return enum

   
class MCAssetsManagerProperties(PropertyGroup):
    """
    the main class containing all McAM related scene properties:
    - UI_LIST_ASSETS_ITEMS
    - UI_LIST_PRESETS_ITEMS
    - UI_LIST_RIGS_ITEMS
    - and more
    """
    
    class DLCListItem(PropertyGroup):
        """
        group of properties representing a dlc item in the ui list\n
        name | type | creator | active | version
        """
        name : StringProperty() # type: ignore
        type : StringProperty() # type: ignore
        creator : StringProperty() # type: ignore
        active : BoolProperty(default = True, update = UpdateFunctionsIntern.update_active) # type: ignore
        version: StringProperty() # type: ignore
        icon : BoolProperty() # type: ignore
    
    class AssetListItem(PropertyGroup):
        """
        group of properties representing an asset item in the ui list\n
        name | type | category | dlc | icon | collection\n
        --> dlc: name of dlc to which the item belongs
        --> collection not needed! category --> object or collection
        --> icon: name of file | if no icon --> empty
        """
        name : StringProperty() # type: ignore
        type : StringProperty() # type: ignore
        category : StringProperty() # type: ignore
        dlc : StringProperty() # type: ignore
        icon : StringProperty() # type: ignore
        collection : StringProperty() # type: ignore
        link : StringProperty() # type: ignore


    class PresetListItem(PropertyGroup):
        """
        group of properties representing a preset item in the ui list
        - name, collection
        --> dlc: name of dlc to which the item belongs
        --> icon: name of file | if no icon --> empty
        """
        name : StringProperty() # type: ignore
        dlc : StringProperty() # type: ignore
        icon : StringProperty() # type: ignore
        collection : StringProperty() # type: ignore
        link : StringProperty() # type: ignore


    class RigListItem(PropertyGroup):
        """
        group of properties representing a rig item in the ui list
        - name, collection
        --> dlc: name of dlc to which the item belongs
        --> icon: name of file | if no icon --> empty
        """
        name : StringProperty() # type: ignore
        dlc : StringProperty() # type: ignore
        icon : StringProperty() # type: ignore
        collection : StringProperty() # type: ignore
        link : StringProperty() # type: ignore

    
    dlc_index : IntProperty(name = "Index for dlc_list", default = 0) # type: ignore
    preset_index : IntProperty(name = "Index for preset_list", default = 0) # type: ignore
    asset_index : IntProperty(name = "Index for asset_list", default = 0) # type: ignore
    rig_index : IntProperty(name = "Index for asset_list", default = 0) # type: ignore
    item_unlock : BoolProperty(name = "(un)locked", default = False) # type: ignore

    preset_list : CollectionProperty(type = PresetListItem) # type: ignore
    asset_list : CollectionProperty(type = AssetListItem) # type: ignore
    dlc_list : CollectionProperty(type = DLCListItem) # type: ignore
    rig_list : CollectionProperty(type = RigListItem) # type: ignore

    scriptUIEnum : EnumProperty(items=UpdateFunctionsIntern.scan_ui_dlc, name ="") # type: ignore
    scriptUIEnum2 : EnumProperty(items=UpdateFunctionsIntern.scan_ui_dlc, name="") # type: ignore

def get_addon_prop():
    """
    returns the properties access to the addon: get_addon_prop().get(property)
    """
    addon = bpy.context.preferences.addons.get(paths.PACKAGE).preferences
    return addon

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

classes = (
    MCAssetsManagerProperties.DLCListItem,
    MCAssetsManagerProperties.AssetListItem,
    MCAssetsManagerProperties.PresetListItem,
    MCAssetsManagerProperties.RigListItem,
    MCAssetsManagerProperties
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.mc_assets_manager_props = PointerProperty(type=MCAssetsManagerProperties)

def unregister():
    del bpy.types.Scene.mc_assets_manager_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
