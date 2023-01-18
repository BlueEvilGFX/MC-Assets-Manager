import bpy

def draw_settings_tab(self, context):
    """
    draws <settings>
    """
    layout = self.layout
    box = layout.box()

    # auto addon updater -> theDuckCow!
    row = box.row()
    row.prop(
        self,
        "auto_check_update",
        text="checks automatically for addon updates")

    # auto dlc update checker
    row = box.row()
    row.prop(
        self.main_props,
        "auto_check_dlc",
        text="checks for DLC updates during startup "
        )

    # two UIs in the n panel
    row = box.row()
    row.prop(
        self.main_props,
        "two_dlc_ui_panels",
        text="displaying two DLC UIs in the n panel")

    # import
    row = box.row()
    row.operator(
        "mcam.add_asset_compound",
        text  = "import asset compound",
        icon = "IMPORT"
    )
    # export all
    row.operator(
        "mcam.ui_list_export_all",
        text = "export all",
        icon = "EXPORT"
    )

    # experimental: option deactivated
    # # storage path
    # row = box.row()
    # row.prop(self.main_props, "storage_path")

    # ━━━━━━━━━━━━ asset browser settings McAM
    asset_box = box.column()
    row = asset_box.row()
    crt_row = row.row()
    crt_row.enabled = True
    paths = bpy.context.preferences.filepaths
    for library in paths.asset_libraries:
        if library.name == "McAM":
            crt_row.enabled = False
            break
    crt_row.operator("mcam.create_asset_library", text="create asset library")

    rmv_row = row.row()
    rmv_row.enabled = not crt_row.enabled
    rmv_row.operator("mcam.remove_asset_library", text="remove asset library")

    # ━━━━━━━━━━━━ displaying all asset libraries
    if len(paths.asset_libraries) > 0:
        split = asset_box.split(factor=0.35)
        name_col = split.column()
        name_col.scale_y = 0.6
        path_col = split.column()
        path_col.scale_y = 0.6

        row = name_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Name")

        row = path_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Path")

        for library in paths.asset_libraries:
            row = name_col.row().box()
            row.label(text=library.name)

            row = path_col.row()
            subrow = row.row().box()
            subrow.label(text=library.path)