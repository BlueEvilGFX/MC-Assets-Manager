import os
import json

import importlib

import bpy
from bpy.props import *
from bpy.types import PropertyGroup
from . import utils


class MCAssetsManagerProperties(PropertyGroup):

    class DlcListItem(PropertyGroup):
        """Group of properties representing the dlc item in the list."""

        def update_active(self,context):
            #   get paths and data
            dlc = self.name
            main_file = utils.AddonPathManagement.getDlcMainJson()

            with open(main_file, "r") as json_file:
                data = json.load(json_file)
                data[dlc]["active"] = self.active                                                   #   set active value of directory to value of prop

                init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]                         #   check init path and existence

                if init_exists:
                    module_name = ".files.DLCs."+dlc
                    package = os.path.splitext(__package__)[0]                                      #   get addon name as package --> MC_Assets_Manager

                    locals()[dlc] = importlib.import_module(name = module_name, package = package)  #   import module of dlc
                    try:
                        if self.active:                                                             #   if module active:
                            locals()[dlc].register()                                                #   register module
                        else:
                            locals()[dlc].unregister()                                              #   unregister module
                    except:
                        pass

            with open(main_file, "w") as json_file:
                json.dump(data, json_file, indent=4)  
            
            utils.AddonReloadManagement.reloadPresetList()

        name: StringProperty(
            name="Name",
            description="the name for this item",
            default="")

        type: StringProperty(
            name="Type",
            description="the type for this item",
            default="")

        creator: StringProperty(
            name="Creator",
            description="the creator for this item",
            default="")
        
        active: BoolProperty(
            name="",
            description="toggles the dlc on and off",
            default = False,
            update=update_active)

        version: StringProperty(
            name = "",
            description = "shows the version of the dlc",
            default = "")

    class PresetListItem(PropertyGroup):
        """Group of properties representing the preset item in the list."""

        name: StringProperty(
            name="Name",
            description="the name for this item",
            default=""
            )

        path: StringProperty(
                name="Path",
                description = "the path to the preset DLC, empty if no DLC",
                default = "")

        icon: StringProperty(
            name="icon",
            description = "the name of the icon, [dlc name +] preset name",
            default = "")

    class AssetListItem(PropertyGroup):
        """Group of properties representing the preset item in the list."""

        name: StringProperty(
            name="Name",
            description="the name for this item",
            default=""
            )

        type: StringProperty(
            name="type",
            description = "defines if it is an object or a collection",
            default = "")
            
        category: StringProperty(
            name="category",
            description = "defines the category",
            default = "")

        path: StringProperty(
            name="Path",
            description = "the path to the preset DLC, empty if no DLC",
            default = "")

        icon : StringProperty(
            name="icon",
            description = "the name of the icon, [dlc name +] preset name",
            default = "")

    class RigListItem(PropertyGroup):
        """Group of properties representing the preset item in the list."""

        name: StringProperty(
            name="Name",
            description="the name for this item",
            default=""
            )

        path: StringProperty(
            name="Path",
            description = "the path to the preset DLC, empty if no DLC",
            default = "")

        icon : StringProperty(
            name="icon",
            description = "the name of the icon, [dlc name +] preset name",
            default = "")
    
    dlc_index : IntProperty(name = "Index for dlc_list", default = 0)
    preset_index : IntProperty(name = "Index for preset_list", default = 0)
    asset_index : IntProperty(name = "Index for asset_list", default = 0)
    rig_index : IntProperty(name = "Index for asset_list", default = 0)
    item_unlock : BoolProperty(name = "(un)locked", default = False)

    preset_list : CollectionProperty(type = PresetListItem)
    asset_list : CollectionProperty(type = AssetListItem)
    dlc_list : CollectionProperty(type = DlcListItem)
    rig_list : CollectionProperty(type = RigListItem)

    def scanUIdlc(self, context):
        addon_path = utils.AddonPathManagement.getAddonPath()
        file = os.path.join(addon_path, "files", "dlcs.json")
    
        with open(file, "r") as json_file:
            data = json.load(json_file)
            enum = []
            for x in data:
                if utils.AddonPathManagement.getInitPath(x)[1] and data[x]["active"]:
                    d = (x, x, '')
                    enum.append(d)
        return enum
    scriptUIEnum : EnumProperty(items=scanUIdlc, name ="")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

classes = (
            MCAssetsManagerProperties.PresetListItem,
            MCAssetsManagerProperties.AssetListItem,
            MCAssetsManagerProperties.DlcListItem,
            MCAssetsManagerProperties.RigListItem,
            MCAssetsManagerProperties,
          )
          
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.mcAssetsManagerProps = bpy.props.PointerProperty(type=MCAssetsManagerProperties)


def unregister():
    del bpy.types.Scene.mcAssetsManagerProps
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)