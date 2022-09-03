import bpy
from bpy.types import UIList
from MC_Assets_Manager.core.utils import icons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_UL_List(UIList):
    """DLC UIList"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # icon
        if item.icon:
            pcoll = icons.mcam_icons[icons.PCOLL_DLC_ID]
            custom_icon = pcoll[item.name].icon_id
        else:
            custom_icon = 51

        # draw
        row = layout.row()
        row.label(text=item.name, icon_value=custom_icon)
        row.label(text=item.type)
        row.label(text=item.creator)
        row.prop(item, "active", text="")