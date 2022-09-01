import json

import bpy
from bpy.props import EnumProperty
from bpy.types import UIList

from ..utils import icons, paths

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_UL_List(UIList):
    """Preset UIList."""
    def dlc_presets_callback(self, context) -> bpy.types.EnumProperty:
        """
        reads the dlcs json file and returns an enum with filtering options
        containing no filtering, user preset filtering and dlc filering
        """
        dlcs_json = paths.get_dlc_json()
    
        with open(dlcs_json, "r") as file:
            data = json.load(file)
            enum = [
                ("None", "None", "None"),
                ("User", "User", "User")
                ]
            for dlc in data:
                presets_path = paths.get_dlc_sub_assets_dir(dlc, paths.PRESETS)
                if presets_path and data[dlc]["active"]:
                    dlc_item = (dlc, dlc, '')
                    enum.append(dlc_item)
        return enum
        
    filter_enum : EnumProperty(items=dlc_presets_callback)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        custom_icon = 51
        # check for own custom icon
        if item.icon:
            pcoll = icons.mcam_icons[icons.PCOLL_PRESET_ID]
            custom_icon = pcoll[item.icon].icon_id
        # check for dlc icon
        elif item.dlc:
            if item.dlc in icons.mcam_icons.get("DLCs", False):
                pcoll = icons.mcam_icons[icons.PCOLL_DLC_ID]
                custom_icon = pcoll[item.dlc].icon_id
        
        # draw
        row = layout.row()
        row.label(text=item.name, icon_value=custom_icon)
        row.label(text=item.dlc)
        
    def filter_items(self, context, data, propname):
        filtered = []
        ordered = []
        items = getattr(data, propname)

        # runs if you look for presets with a specific name
        if self.filter_name:
            filtered = [self.bitflag_filter_item] * len(items)
            for i, item in enumerate(items):
                if not self.filter_name.lower() in item.name.lower():
                    filtered[i] &= ~self.bitflag_filter_item
        
        # runs if you look for a preset in a specific 'collection'
        if self.filter_enum != "None":
            filtered = [self.bitflag_filter_item] * len(items)
            filter_key = self.filter_enum\
                if not self.filter_enum == "User"\
                else ""

            for i, item in enumerate(items):
                if not item.dlc == filter_key:
                    filtered[i] &= ~self.bitflag_filter_item

        return filtered, ordered

    def draw_filter(self, context, layout):
        main = layout.row().split(factor=0.7)
        firstRow = main.row(align=True)
        secondRow = main.row(align=True)

        firstRow.prop(self, "filter_name", text="")
        firstRow.prop(self, "use_filter_invert", text="", icon="ARROW_LEFTRIGHT")

        secondRow.prop(self, "filter_enum", text="")
        
        icon = "SORT_DESC" if self.use_filter_sort_reverse == True else "SORT_ASC"
        secondRow.prop(self, "use_filter_sort_reverse", text="", icon=icon)
