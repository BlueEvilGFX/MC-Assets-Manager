import json
import os

from bpy.props import EnumProperty
from bpy.types import UIList
from MC_Assets_Manager.core.utils import icons, paths

from . import commons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ASSET_UL_List(UIList):
    """Asset UIList."""
    # filter enum for normal dlc filtering
    filter_enum : EnumProperty(items=commons.dlc_callback(paths.AssetTypes.ASSETS)) # type: ignore

    # filtering for categories -> categories written in json file
    category_file = paths.DLC.get_asset_categories_json()
    with open(category_file, "r") as file:
        data = json.load(file)
        categories = [("None", "None", "None")]
        for x in data:
            d = (x, x, '')
            categories.append(d)
    
    category_enum : EnumProperty(items=categories) # type: ignore

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # draw
        custom_icon = commons.get_icon(item, icons.PCOLL_ASSET_ID, 56)
        row = layout.row()
        row.label(text=item.name, icon_value=custom_icon)
        row.label(text=item.dlc)
        row.label(text=item.category)
        if item.link:
            row.operator(
                "mcam.ui_list_open_dir",
                text = "",
                icon = "LINKED"
            ).asset_type = os.path.dirname(item.link)
    
    def filter_items(self, context, data, propname):
        filtered, ordered = commons.filter_items_name_dlc(self, context,
                                                          data, propname)
        
        items = getattr(data, propname)
        if self.category_enum != "None":
            filtered = [self.bitflag_filter_item] * len(items)

            for i, item in enumerate(items):
                if not item.category == self.category_enum:
                    filtered[i] &= ~self.bitflag_filter_item

        return filtered, ordered

    def draw_filter(self, context, layout):
        main = layout.row().split(factor=0.6)
        left = main.column()
        firstRow = left.row(align=True)
        secondRow = main.row(align=True)
        column = secondRow.column()
        right = secondRow.row(align=True)
        right.scale_y = 2

        firstRow.prop(self, "filter_name", text="")
        firstRow.prop(self, "use_filter_invert", text="", icon="ARROW_LEFTRIGHT")

        left.alignment = "RIGHT"
        left.label(text="category:")
    
        column.prop(self, "filter_enum", text="")
        column.prop(self, "category_enum", text="")

        icon = "SORT_DESC" if self.use_filter_sort_reverse is True else "SORT_ASC"
        right.prop(self, "use_filter_sort_reverse", text="", icon=icon)