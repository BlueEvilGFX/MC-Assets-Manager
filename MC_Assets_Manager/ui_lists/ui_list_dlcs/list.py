import bpy

from ...miscs.icons import dlc_icon_collections

from bpy.types import UIList

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_UL_List(UIList):
    """DLC UIList"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        #   set icon
        try: 
            pcoll = dlc_icon_collections["DLCs"]
            ic = item.name
            custom_icon = pcoll[ic].icon_id
        except:
            custom_icon = 51

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.label(text=item.name, icon_value=custom_icon)
            row.label(text=item.type)
            row.label(text=item.creator)
            row.prop(item, "active")

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=custom_icon)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         
def register():
    bpy.utils.register_class(DLC_UL_List)
  
def unregister():
    bpy.utils.unregister_class(DLC_UL_List)