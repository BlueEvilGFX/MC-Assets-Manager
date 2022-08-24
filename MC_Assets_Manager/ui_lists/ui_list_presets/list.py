import bpy
import os
import json

from ...miscs import utils
from ...miscs.icons import dlc_icon_collections, preset_icon_collections

from bpy.props import EnumProperty
from bpy.types import UIList

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_UL_List(UIList):
    """Preset UIList."""
    def dlcPresetsCallBack(self, context):
        addon_path = utils.AddonPathManagement.getAddonPath()
        file = os.path.join(addon_path, "files", "dlcs.json")
    
        with open(file, "r") as json_file:
            data = json.load(json_file)
            enum = [
                ("no dlc filtering", "no dlc filtering", "no dlc filtering"),
                ("own presets", "own presets", "own presets")
                ]
            for x in data:
                presets_path = os.path.join(addon_path, "files", "DLCs", x, "presets")
                presetDLC_exists = os.path.exists(presets_path)
                if presetDLC_exists and data[x]["active"]:
                    d = (x, x, '')
                    enum.append(d)
        return enum
        
    dlcPresetEnum : EnumProperty(items=dlcPresetsCallBack)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #   set icon
        if item.path == "":
            custom_icon = 15
        elif item.path == "$$$":
            try:
                pcoll = preset_icon_collections["Presets"]
                ic = "ownPreset_" + item.name
                custom_icon = pcoll[ic].icon_id
            except:
                custom_icon = 15
        else:
            # if this icon exists --> use it; else: use dlc icon
            try:
                pcoll = preset_icon_collections["Presets"]
                ic = item.icon
                custom_icon = pcoll[ic].icon_id 
            except:
                try:
                    pcoll = dlc_icon_collections["DLCs"]
                    ic = os.path.basename(os.path.dirname(os.path.dirname(item.path)))
                    custom_icon = pcoll[ic].icon_id
                except:
                    custom_icon = 15
                
        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.label(text=item.name, icon_value=custom_icon)
            row.label(text=str(os.path.basename(os.path.dirname(os.path.dirname(item.path)))))
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=custom_icon)
        
    def filter_items(self, context, data, propname):
        filtered = []
        ordered = []
        items = getattr(data, propname)

        if self.filter_name:
            filtered = [self.bitflag_filter_item] * len(items)
            for i, item in enumerate(items):
                if not self.filter_name.lower() in item.name.lower():
                    filtered[i] &= ~self.bitflag_filter_item
        
        if self.dlcPresetEnum != "no dlc filtering":
            filtered = [self.bitflag_filter_item] * len(items)

            for i, item in enumerate(items):
                if self.dlcPresetEnum == "own presets":
                    path = ""
                else:
                    dlcName = str(os.path.basename(os.path.dirname(os.path.dirname(item.path))))
                    if dlcName in item.path:
                        dlc_path = utils.AddonPathManagement.getDlcDirPath()
                        path = os.path.join(dlc_path, dlcName, "presets", item.name+".blend")

                if not item.path == path:
                    filtered[i] &= ~self.bitflag_filter_item

        return filtered, ordered

    def draw_filter(self, context, layout):
        main = layout.row().split(factor=0.7)
        firstRow = main.row(align=True)
        secondRow = main.row(align=True)

        firstRow.prop(self, "filter_name", text="")
        firstRow.prop(self, "use_filter_invert", text="", icon="ARROW_LEFTRIGHT")

        secondRow.prop(self, "dlcPresetEnum", text="")
        
        icon = "SORT_DESC" if self.use_filter_sort_reverse == True else "SORT_ASC"
        secondRow.prop(self, "use_filter_sort_reverse", text="", icon=icon)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    bpy.utils.register_class(PRESET_UL_List)
  
def unregister():
    bpy.utils.unregister_class(PRESET_UL_List)