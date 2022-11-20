from MC_Assets_Manager.core.utils import icons
from MC_Assets_Manager.core.utils.github_connect import StatusEnum
from MC_Assets_Manager import addon_updater_ops

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def draw_online_tab(self, context, element=None):
    layout = self.layout
    pcoll = icons.mcam_icons["McAM"]
    smallHeader = layout.row()
    smallHeader.prop(self.main_props, "online_menu", expand = True)
    smallHeader.label(text="", icon="BLANK1")

    row = layout.row()
    if self.main_props.online_menu == "Addon Updater":
        addon_updater_ops.update_settings_ui(self, context, row)
    else:
        draw_github_tab(self, layout, row)

    colMain = row.column(align=True)
    custom_icon = pcoll["github"].icon_id
    colMain.operator("wm.url_open", text="", icon_value = custom_icon).url = "https://github.com/BlueEvilGFX/MC-Assets-Manager"

    custom_icon = pcoll["youtube"].icon_id
    colMain.operator("wm.url_open", text="", icon_value = custom_icon).url = "https://www.youtube.com/channel/UCKPgR4jjSDRTqWGAd2IOL5w"

    custom_icon = pcoll["discord"].icon_id
    colMain.operator("wm.url_open", text="", icon_value = custom_icon).url = "https://discord.com/invite/3mybvgB6wE"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
def draw_github_tab(self, layout, element):
    from MC_Assets_Manager.core.utils.github_connect import github_reader
        
    layout = layout if element is None else element.column()

    box = layout.box()
    box.label(text="Github DLC connector : shows only original DLCs")
    row = box.row()
    if not github_reader == None:
        pcoll = icons.mcam_icons[icons.PCOLL_MCAM_ID]
        custom_icon = pcoll["github"].icon_id

        row.operator("mcam.githubconnect", text="refresh", icon="FILE_REFRESH")
        row.alert = False
        row.operator(
            "wm.url_open",
            text="open website",
            icon_value = custom_icon)\
                .url = "https://github.com/BlueEvilGFX/McAM-DLCs"
    else:
        row.operator("mcam.githubconnect", text="connect", icon="WORLD_DATA")

    row.prop(self.main_props, "auto_check_dlc", text="", icon="TEMP")

    if not github_reader.network_connection or not github_reader:
        layout.label(text="please connect to github")
        if not github_reader.network_connection:
            layout.label(text="please connect to the internet")
    else:
        header = layout.box()
        header.scale_y = 0.5
        header = header.row()   
        header.label(text="installed")
        header.label(text="update available")
        header.label(text="not installed")

        body = layout.row()
        split = body.split(factor=1/3)
        col1 = split.box().column()             #   up-to-date
        col2 = split.split().box().column()     #   update
        col3 = split.split().box().column()     #   not installed

        for dlc in github_reader.dlc_list:
            try: 
                pcoll = icons.mcam_icons[icons.PCOLL_DLC_ID]
                custom_icon = pcoll[dlc.name].icon_id
            except:
                custom_icon = 51
                
            #   display of DLCs
            if dlc.status == StatusEnum.INSTALLED:
                display = col1.row()
                display.label(text=dlc.name, icon_value = custom_icon)

            elif dlc.status == StatusEnum.UPDATEABLE:
                display = col2.row()
                display.label(text=dlc.name, icon_value = custom_icon)
                button = display.operator(
                    "mcam.githubupdateinstall",
                    icon="FILE_REFRESH"
                    )
                button.data = dlc.name
                
            elif dlc.status == StatusEnum.INSTALLABLE:
                display = col3.row()
                display.label(text=dlc.name, icon_value = custom_icon)
                button = display.operator("mcam.githubupdateinstall", icon = "IMPORT")
                button.data = dlc.name

        #   display of update/install all DLCs
        sub_row = layout.row()
        if all(dlc.status == StatusEnum.INSTALLED\
                for dlc in github_reader.dlc_list):
            sub_row.enabled = False
        else:
            sub_row.enabled = True
        sub_row.operator("mcam.githubupdateinstallall")