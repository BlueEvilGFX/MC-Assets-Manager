import importlib
import json
import bpy
from bpy.props import *
from bpy.types import PropertyGroup

from . import paths
from . import reload

class UpdateFunctionsInternal:
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
        dlc_json = paths.get_dlc_json()

        # reading status and reload if necessary
        with open(dlc_json, "r") as file:
            data = json.load(file)

        # writes blenders prop dlc status value to the data dict
        data[dlc_name]["active"] = self.active
        
        init_path = paths.get_dlc_init(dlc_name)

        if init_path:
            locals()[dlc_name] = importlib.import_module(
                name = f'.storage.dlcs.{dlc_name}',
                package = paths.PACKAGE
                )

            # register / unregister them
            try:
                if self.active:
                    locals()[dlc_name].register()
                else:
                    locals()[dlc_name].unregister()
            except:
                pass
            addonPreferences.reload()

        # write active status to json file
        with open(dlc_json, "w") as file:
            json.dump(data, file, indent=4)  
        
        reload.reload_asset_list()
        reload.reload_asset_list()
        reload.reload_preset_list()

    @staticmethod
    def scan_ui_dlc(self, context):
        """
        function that returns the active scripted DLCs
        as enum items.
        """
        dlc_json = paths.get_dlc_json()
    
        with open(dlc_json, "r") as json_file:
            data = json.load(json_file)
            enum = []
            for dlc in data:
                if paths.get_dlc_init(dlc)and data[dlc]["active"]:
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
        name : StringProperty()
        type : StringProperty()
        creator : StringProperty()
        active : BoolProperty(default = True, update = UpdateFunctionsInternal.update_active)
        version: StringProperty()
    
    class AssetListItem(PropertyGroup):
        """
        group of properties representing an asset item in the ui list\n
        name | type | category | dlc | icon | collection\n
        --> dlc: name of dlc to which the item belongs
        --> collection not needed! category --> object or collection
        --> icon: name of file | if no icon --> empty
        """
        name : StringProperty()
        type : StringProperty()
        category : StringProperty()
        dlc : StringProperty()
        icon : StringProperty()
        collection : StringProperty()


    class PresetListItem(PropertyGroup):
        """
        group of properties representing a preset item in the ui list
        - name, collection
        --> dlc: name of dlc to which the item belongs
        --> icon: name of file | if no icon --> empty
        """
        name : StringProperty()
        dlc : StringProperty()
        icon : StringProperty()
        collection : StringProperty()


    class RigListItem(PropertyGroup):
        """
        group of properties representing a rig item in the ui list
        - name, collection
        --> dlc: name of dlc to which the item belongs
        --> icon: name of file | if no icon --> empty
        """
        name : StringProperty()
        dlc : StringProperty()
        icon : StringProperty()
        collection : StringProperty()

    
    dlc_index : IntProperty(name = "Index for dlc_list", default = 0)
    preset_index : IntProperty(name = "Index for preset_list", default = 0)
    asset_index : IntProperty(name = "Index for asset_list", default = 0)
    rig_index : IntProperty(name = "Index for asset_list", default = 0)
    item_unlock : BoolProperty(name = "(un)locked", default = False)

    preset_list : CollectionProperty(type = PresetListItem)
    asset_list : CollectionProperty(type = AssetListItem)
    dlc_list : CollectionProperty(type = DLCListItem)
    rig_list : CollectionProperty(type = RigListItem)

    scriptUIEnum : EnumProperty(items=UpdateFunctionsInternal.scan_ui_dlc, name ="")
    scriptUIEnum2 : EnumProperty(items=UpdateFunctionsInternal.scan_ui_dlc, name="")


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
    
    # assigning the McAM prop group to a scene pointer property
    left_side = f'bpy.types.Scene{paths.MCAM_PROP_GROUP}'
    right_side = f'{PointerProperty(type=MCAssetsManagerProperties)}'
    eval(f'{left_side} : {right_side}')

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)