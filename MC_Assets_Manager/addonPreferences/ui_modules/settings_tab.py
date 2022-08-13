def show_settings(self, context, layout):
    layout = layout.row()
    box = layout.box()

    # ━━━━━━━━━━━━ reloading settings
    row = box.row()
    row.prop(self, "reload_all_during_startup", text="")
    row.label(text="reload all parts of the addon when starting Blender (loads: presets, assets & rigs)")

    # ━━━━━━━━━━━━ auto checking for dlc updates
    row = box.row()
    row.prop(self, "auto_check_dlc", text="")
    row.label(text="auto checking for DLC updates when starting Blender")

    # ━━━━━━━━━━━━ two DLC UIs in the n panel
    row = box.row()
    row.prop(self, "two_dlc_ui_panels", text="")
    row.label(text="displaying two DLC UIs in the n panel")
    

    # ━━━━━━━━━━━━ gap on the right side
    layout.label(text="", icon="BLANK1")