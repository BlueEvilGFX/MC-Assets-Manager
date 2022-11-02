from MC_Assets_Manager.core.utils import paths, asset_dict

def draw_assets_tab(self, context):
    """
    draws the <asset_type> ui list with all its operators according to the
    selection in the <assets_menu> property
    """
    # gets the current navigation in the sub category assets
    navigator = self.main_props.assets_menu
    if not navigator in ["Assets", "Presets", "Rigs"]:
        return

    layout = self.layout
    # categories: assets, presets, rigs
    categories = self.layout.row()
    categories.prop(self.main_props, "assets_menu", expand = True)

    # info header for the assets including name, source
    info_header = layout.row()
    left_info_header = info_header.column()
    right_info_header = info_header.row()
    header_box = left_info_header.box()
    header_labels = header_box.row()
    header_labels.scale_y = 0.5
    header_labels.label(text = "Name")
    header_labels.label(text = "Source")

    props = context.scene.mc_assets_manager_props

    # main
    if navigator == "Assets":
        header_labels.label(text = "Category")

    main = left_info_header
    ul_class, index = asset_dict.get_ul_class(navigator.lower())
    asset_type = asset_dict.get_asset_types(
        navigator.lower(),asset_dict.Selection.ui_list
        )

    main.template_list(
        ul_class, "The_List", props,
        asset_type, props, index
        )

    # operators
    main_right = right_info_header.column()
    first = main_right.column(align = True)
    second = main_right.column(align = True)
    third = main_right.column(align = True)
    fourth = main_right.column(align = True)

    reloader_comp = first.row()
    reloader = reloader_comp.operator(
        "mcam.ui_list_reload",
        text = "",
        icon = "FILE_REFRESH"
        )

    adder_comp = second.row(align = True)
    adder = adder_comp.operator(
        "mcam.ui_list_add",
        text = "",
        icon = "ADD"
        )
    remover_comp = second.row(align = True)
    remover_comp.enabled = polling_remove(self, context, asset_type)
    remover = remover_comp.operator(
        "mcam.ui_list_remove",
        text = "",
        icon = "REMOVE"
        )
    
    lock = get_lock_icon(context)
    third.prop(
        context.scene.mc_assets_manager_props,
        "item_unlock",
        text="",
        icon=lock
        )

    if navigator == "Assets":
        # operator settings
        reloader.asset_type = paths.ASSETS
        adder.asset_type = paths.USER_ASSETS
        remover.asset_type = paths.USER_ASSETS

    elif navigator == "Presets":
        # operator settings
        reloader.asset_type = paths.PRESETS
        adder.asset_type = paths.USER_PRESETS
        remover.asset_type = paths.USER_PRESETS

    elif navigator == "Rigs":
        # operator settings
        reloader.asset_type = paths.RIGS
        adder.asset_type = paths.USER_RIGS
        remover.asset_type = paths.USER_RIGS

def get_lock_icon(context):
    """
    returns "UNLOCKED" if the property item_unlock is True\
        else "LOCKED"
    """
    return "UNLOCKED" if context.scene.mc_assets_manager_props.item_unlock\
        else "LOCKED"
        
def polling_remove(self, context, asset_type) -> bool:
    """
    args:
        self: addon preferences instance self
        context: addon preferences context
        asset_type: enum of: 
            paths.UI_LIST_ASSETS |
            paths.UI_LIST_PRESETS | 
            paths.UI_LIST_RIGS
    description:
        polling method for the remove operator
        returns the 'enabled' status for the operator\n
        checks:
            a) if item not a dlc item\n
            b) lock is unklocked
    """
    scene = context.scene
    try:
        # gets the type: 'asset' |'preset' |'rig' + _index'
        index_prop = asset_type.split("_")[0] + "_index"
        item_list = asset_type

        index = eval(f"scene.mc_assets_manager_props.{index_prop}")
        item = eval(f"scene.mc_assets_manager_props.{item_list}[{index}]")

        if scene.mc_assets_manager_props.item_unlock and item.dlc == "":
            return True
        return False
    except:
        return False