from bpy.props import EnumProperty
import os
from bpy.types import UIList
from MC_Assets_Manager.core.utils import icons, paths

from . import commons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PRESET_UL_List(UIList):
    """Preset UIList"""
    filter_enum : EnumProperty(items=commons.dlc_callback(paths.AssetTypes.PRESETS)) # type: ignore

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):        
        # draw
        custom_icon = commons.get_icon(item, icons.PCOLL_PRESET_ID, 51)
        row = layout.row()
        row.label(text=item.name, icon_value=custom_icon)
        row.label(text=item.dlc)
        if item.link:
            row.operator(
                "mcam.ui_list_open_dir",
                text = "",
                icon = "LINKED"
            ).asset_type = os.path.dirname(item.link)
        
    def filter_items(self, context, data, propname):
        return commons.filter_items_name_dlc(self, context, data, propname)

    def draw_filter(self, context, layout):
        commons.draw_filter(self, context, layout)