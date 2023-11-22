import bpy

from MC_Assets_Manager.core.utils import paths


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

    # ━━━━━━━━━━━━ operators

    box = layout.box()

    # open asset dirs
    row = box.row()
    row.label(text="open:", icon = "FILEBROWSER")
    row.operator(
        "mcam.ui_list_open_dir",
        text = "assets",
        icon = "DOCUMENTS"
    ).asset_type = paths.AssetTypes.USER_ASSETS
    row.operator(
        "mcam.ui_list_open_dir",
        text = "presets",
        icon = "OUTLINER_OB_ARMATURE"
    ).asset_type = paths.AssetTypes.USER_PRESETS
    row.operator(
        "mcam.ui_list_open_dir",
        text = "rigs",
        icon = "ARMATURE_DATA"
    ).asset_type = paths.AssetTypes.USER_RIGS

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

    box = layout.box()
    row = box.row()
    libraries = bpy.context.preferences.filepaths.asset_libraries

    row.operator("mcam.create_asset_library", text="create asset library")
    row.operator("mcam.remove_asset_library", text="remove asset library")

    if any(lib.name == "McAM" for lib in libraries):
        row.label(icon="CHECKBOX_HLT")
    else:
        row.label(icon="CHECKBOX_DEHLT")