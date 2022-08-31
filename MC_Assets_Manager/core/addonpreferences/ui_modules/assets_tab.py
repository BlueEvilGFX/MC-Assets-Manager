from ...utils import paths

def assets_tab(self, context, layout, scene):
    lowerEnum = layout.row()
    lowerEnum.prop(self.main_props, "assets_menu", expand = True)
    # lowerEnum.label(text="", icon = "BLANK1")
    # lowerEnum.operator("mcam.add_main_file", text="", icon="RNA_ADD")
    smallHeader = layout.row()

    sm = smallHeader.column()
    smBox = sm.box()
    smr = smBox.row()
    smr.scale_y = 0.5
    smr.label(text="Name")
    smr.label(text="Source")

    right = smallHeader.row().column()

    # ━━━━━━━━━━━━ presets
    if self.main_props.assets_menu == "Presets":
        row = sm
        row.template_list("PRESET_UL_List", "The_List", scene.mc_assets_manager_props, "preset_list", scene.mc_assets_manager_props, "preset_index")

        colMain = right.column()
        colFir = colMain.column()
        reloader = colFir.operator("mcam.ui_list_reload", text = "", icon = "FILE_REFRESH")
        reloader.asset_type = paths.PRESETS

        # colSec = colMain.column(align = True)
        # colSec.operator("mcam.preset_list_add", text = "", icon = "ADD")
        # colSec.operator("mcam.preset_list_remove", text = "", icon = "REMOVE") 

        # colThi = colMain.column(align = True)
        # if context.scene.mc_assets_manager_props.item_unlock == False: lock = "LOCKED"
        # else: lock = "UNLOCKED"
        # colThi.prop(context.scene.mc_assets_manager_props, "item_unlock", text="", icon=lock)

        # colFou = colMain.column(align = True)
        # colFou.operator("mcam.preset_list_export", text = "", icon = "EXPORT")

    # ━━━━━━━━━━━━ assets
    elif self.main_props.assets_menu == "Assets":
        row = sm
        smr.label(text="Category")
        row.template_list("ASSET_UL_List", "The_List", scene.mc_assets_manager_props, "asset_list", scene.mc_assets_manager_props, "asset_index")
        
        colMain = right.column()
        colFir = colMain.column()
        colFir.operator("mcam.asset_list_reload", text = "", icon = "FILE_REFRESH")
        colSec = colMain.column(align = True)
        colSec.operator("mcam.asset_list_add", text = "", icon = "ADD")
        colSec.operator("mcam.asset_list_remove", text = "", icon = "REMOVE")

        colThi = colMain.column(align = True)
        if context.scene.mc_assets_manager_props.item_unlock == False: lock = "LOCKED"
        else: lock = "UNLOCKED"
        colThi.prop(context.scene.mc_assets_manager_props, "item_unlock", text="", icon=lock)

        colFou = colMain.column(align = True)
        colFou.operator("mcam.asset_list_export", text = "", icon = "EXPORT")

    # ━━━━━━━━━━━━ rigs
    elif self.main_props.assets_menu == "Rigs":
        row = sm
        row.template_list("RIG_UL_List", "The_List", scene.mc_assets_manager_props, "rig_list", scene.mc_assets_manager_props, "rig_index")
        
        colMain = right.column()
        colFir = colMain.column()
        colFir.operator("mcam.rig_list_reload", text = "", icon = "FILE_REFRESH")
        colSec = colMain.column(align = True)
        colSec.operator("mcam.rig_list_add", text = "", icon = "ADD")
        colSec.operator("mcam.rig_list_remove", text = "", icon = "REMOVE")

        colThi = colMain.column(align = True)
        if context.scene.mc_assets_manager_props.item_unlock == False: lock = "LOCKED"
        else: lock = "UNLOCKED"
        colThi.prop(context.scene.mc_assets_manager_props, "item_unlock", text="", icon=lock)

        colFou = colMain.column(align = True)
        colFou.operator("mcam.rig_list_export", text = "", icon = "EXPORT")