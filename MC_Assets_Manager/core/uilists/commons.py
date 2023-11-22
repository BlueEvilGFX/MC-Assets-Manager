import json
from MC_Assets_Manager.core.utils import paths, icons

def dlc_callback(asset_type) -> list:
    """
    args:
        asset_type enum of: paths.PRESETS | paths.RIGS
    description:
        - returns the enum item in a list
        reads the dlcs json file and returns an enum with filtering options
        - containing no filtering, user preset filtering and dlc filering
    """

    def callback(self, context):
        dlcs_json = paths.McAM.get_dlc_main_json()

        with open(dlcs_json, "r") as file:
            data = json.load(file)
            enum = [
                ("None", "None", "None"),
                ("User", "User", "User")
                ]
            for dlc in data:
                presets_path = paths.DLC.get_sub_asset_directory(dlc, asset_type)
                if presets_path and data[dlc]["active"]:
                    dlc_item = (dlc, dlc, '')
                    enum.append(dlc_item)
        return enum
    return callback

def get_icon(item, pcoll_id, default_icon):
    """
    args:
        item : list item : from UiList
        pcoll_id enum of: icons.PCOLL_RIG_ID | icons.PCOLL_PRESET_ID
        default_icon : default id of icon to be used
    """
    # check for custom icon
    if item.icon:
        pcoll = icons.mcam_icons[pcoll_id]
        default_icon = pcoll[item.icon].icon_id
    # check for dlc icon
    elif item.dlc:
        if item.dlc in icons.mcam_icons.get("DLCs", False):
            pcoll = icons.mcam_icons[icons.PCOLL_DLC_ID]
            default_icon = pcoll[item.dlc].icon_id
    return default_icon

def filter_items_name_dlc(self, context, data, propname) -> list:
    """
    returns two lists : filtered & ordered items
    """
    filtered = []
    ordered = []
    items = getattr(data, propname)

    # runs if you look for rigs with a specific name
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

    icon = "SORT_DESC" if self.use_filter_sort_reverse else "SORT_ASC"
    secondRow.prop(self, "use_filter_sort_reverse", text="", icon=icon)