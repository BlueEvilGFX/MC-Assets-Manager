from bpy.props import EnumProperty
from bpy.types import UIList
from MC_Assets_Manager.core.utils import icons, paths

from . import commons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_UL_List(UIList):
    """Rig UIList"""
    filter_enum : EnumProperty(items=commons.dlc_callback(paths.RIGS))

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # draw
        custom_icon = commons.get_icon(item, icons.PCOLL_RIG_ID, 172)
        row = layout.row()
        row.label(text=item.name, icon_value=custom_icon)
        row.label(text=item.dlc)
    
    def filter_items(self, context, data, propname):
        return commons.filter_items_name_dlc(self, context, data, propname)

    def draw_filter(self, context, layout):
        commons.draw_filter(self, context, layout)