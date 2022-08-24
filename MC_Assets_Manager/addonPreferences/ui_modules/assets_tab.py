def assets_tab(self, context, layout, scene):
    lowerEnum = layout.row()
    lowerEnum.prop(self.main_props, "assets_menu", expand = True)
    # lowerEnum.label(text="", icon = "BLANK1")
    lowerEnum.operator("mcam.add_main_file", text="", icon="RNA_ADD")
    smallHeader = layout.row()

    sm = smallHeader.column()
    smBox = sm.box()
    smr = smBox.row()
    smr.scale_y = 0.5
    smr.label(text="Name")
    smr.label(text="Source")

    right = smallHeader.row().column()

    # ━━━━━━━━━━━━ presets
    if self.main_props.assets_menu == "0":
        layout.label(text="hi")

        row = sm
        row.template_list("PRESET_UL_List", "The_List", scene.mcAssetsManagerProps, "preset_list", scene.mcAssetsManagerProps, "preset_index")

        colMain = right.column()
        colFir = colMain.column()
        colFir.operator("mcam.preset_list_reload", text = "", icon = "FILE_REFRESH")
        colSec = colMain.column(align = True)
        colSec.operator("mcam.preset_list_add", text = "", icon = "ADD")
        colSec.operator("mcam.preset_list_remove", text = "", icon = "REMOVE") 

        colThi = colMain.column(align = True)
        if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
        else: lock = "UNLOCKED"
        colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)

        colFou = colMain.column(align = True)
        colFou.operator("mcam.preset_list_export", text = "", icon = "EXPORT")
    # ━━━━━━━━━━━━ assets
    elif self.main_props.assets_menu == "1":
        row = sm
        smr.label(text="Category")
        row.template_list("ASSET_UL_List", "The_List", scene.mcAssetsManagerProps, "asset_list", scene.mcAssetsManagerProps, "asset_index")
        colMain = right.column()
        colFir = colMain.column()
        colFir.operator("mcam.asset_list_reload", text = "", icon = "FILE_REFRESH")
        colSec = colMain.column(align = True)
        colSec.operator("mcam.asset_list_add", text = "", icon = "ADD")
        colSec.operator("mcam.asset_list_remove", text = "", icon = "REMOVE")

        colThi = colMain.column(align = True)
        if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
        else: lock = "UNLOCKED"
        colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)

        colFou = colMain.column(align = True)
        colFou.operator("mcam.asset_list_export", text = "", icon = "EXPORT")
    # ━━━━━━━━━━━━ rigs
    elif self.main_props.assets_menu == "2":
        row = sm
        row.template_list("RIG_UL_List", "The_List", scene.mcAssetsManagerProps, "rig_list", scene.mcAssetsManagerProps, "rig_index")
        colMain = right.column()
        colFir = colMain.column()
        colFir.operator("mcam.rig_list_reload", text = "", icon = "FILE_REFRESH")
        colSec = colMain.column(align = True)
        colSec.operator("mcam.rig_list_add", text = "", icon = "ADD")
        colSec.operator("mcam.rig_list_remove", text = "", icon = "REMOVE")

        colThi = colMain.column(align = True)
        if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
        else: lock = "UNLOCKED"
        colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)

        colFou = colMain.column(align = True)
        colFou.operator("mcam.rig_list_export", text = "", icon = "EXPORT")