import bpy

def show_settings(self, context, layout):
    layout = layout.row()
    column = layout.column()
    box = column.box()

    # ━━━━━━━━━━━━ reloading settings
    row = box.row()
    row.prop(self.main_props, "reload_all_during_startup", text="")
    row.label(text="reload all parts of the addon when starting Blender (loads: presets, assets & rigs)")

    # ━━━━━━━━━━━━ auto checking for addon updates
    #   ADDON UPDATER --> NO self.main_props
    row = box.row()
    row.prop(self, "auto_check_update", text="")
    row.label(text="auto checking for addon updates")

    # ━━━━━━━━━━━━ auto checking for dlc updates
    row = box.row()
    row.prop(self.main_props, "auto_check_dlc", text="")
    row.label(text="auto checking for DLC updates when starting Blender")

    # ━━━━━━━━━━━━ two DLC UIs in the n panel
    row = box.row()
    row.prop(self.main_props, "two_dlc_ui_panels", text="")
    row.label(text="displaying two DLC UIs in the n panel")

    # ━━━━━━━━━━━━ storage path
    row = box.row()
    row.prop(self.main_props, "storage_path")

    # ==================================================

    # ━━━━━━━━━━━━ asset browser settings McAM
    box = column.box()
    row = box.row()
    create_row = row.row()
    create_row.enabled = True
    paths = bpy.context.preferences.filepaths
    for i, library in enumerate(paths.asset_libraries):
        if library.name == "McAM":
            create_row.enabled = False
            break
    create_row.operator("mcam.create_asset_library", text="create asset library")

    remove_row = row.row()
    remove_row.enabled = not create_row.enabled
    remove_row.operator("mcam.remove_asset_library", text="remove asset library")

    # ━━━━━━━━━━━━ displaying all asset libraries
    if len(paths.asset_libraries) > 0:
        split = box.split(factor=0.35)
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

        for i, library in enumerate(paths.asset_libraries):
            row = name_col.row().box()
            row.label(text=library.name)

            row = path_col.row()
            subrow = row.row().box()
            subrow.label(text=library.path)

    # ==================================================

    # ━━━━━━━━━━━━ gap on the right side
    layout.label(text="", icon="BLANK1")