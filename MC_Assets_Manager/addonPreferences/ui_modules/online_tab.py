from ... import addon_updater_ops
from ...utils import github_dlcs
from ...utils.icons import basicMCAM_icon_collection

def online_tab(self, context, layout):
    pcoll = basicMCAM_icon_collection["McAM"]
    smallHeader = layout.row()
    smallHeader.prop(self, "online_menu", expand = True)
    smallHeader.label(text="", icon="BLANK1")

    row = layout.row()
    if self.online_menu == "0":
        addon_updater_ops.update_settings_ui(self, context, row)
    elif self.online_menu == "1":
        github_dlcs.ui.display_github_dlc(self, context, row)

    colMain = row.column(align=True)
    custom_icon = pcoll["McAM_github"].icon_id
    colMain.operator("wm.url_open", text="", icon_value = custom_icon).url = "https://github.com/BlueEvilGFX/MC-Assets-Manager"

    custom_icon = pcoll["McAM_youtube"].icon_id
    colMain.operator("wm.url_open", text="", icon_value = custom_icon).url = "https://www.youtube.com/channel/UCKPgR4jjSDRTqWGAd2IOL5w"

    custom_icon = pcoll["McAM_discord"].icon_id
    colMain.operator("wm.url_open", text="", icon_value = custom_icon).url = "https://discord.com/invite/3mybvgB6wE"