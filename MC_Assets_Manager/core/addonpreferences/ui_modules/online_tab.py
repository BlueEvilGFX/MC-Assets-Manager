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

def get_icon(pcoll_id, dlc):
    """
    pcoll_id: enum of
        PCOLL_ASSET_ID | PCOLL_PRESET_ID | PCOLL_RIG_ID | PCOLL_MCAM_ID
        | PCOLL_DLC_ID | PCOLL_GITHUB_DLC_ID
    """
    try: 
        pcoll = icons.mcam_icons[pcoll_id]
        return pcoll[dlc.name].icon_id
    except:
        return 51

       
def draw_github_tab(self, layout, element):
    from MC_Assets_Manager.core.utils.github_connect import github_reader
        
    layout = layout if element is None else element.column()

    box = layout.box()
    box.label(text="Github DLC connector : shows only original DLCs")
    row = box.row()

    # no githubreader initialized
    if github_reader == None:
        row.operator("mcam.githubconnect", text="connect", icon="WORLD_DATA")
        return
    else:
        pcoll = icons.mcam_icons[icons.PCOLL_MCAM_ID]
        custom_icon = pcoll["github"].icon_id

        row.operator("mcam.githubconnect", text="refresh", icon="FILE_REFRESH")
        row.alert = False
        row.operator(
            "wm.url_open",
            text="open website",
            icon_value = custom_icon)\
                .url = "https://github.com/BlueEvilGFX/McAM-DLCs"

    row.prop(self.main_props, "auto_check_dlc", text="", icon="TEMP")

    # no internet connection
    if not github_reader.network_connection:
        layout.label(text="please connect to the internet")
        return
    
    # displaying DLCs- github
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
        #   display of DLCs
        if dlc.status == StatusEnum.INSTALLED:
            custom_icon = get_icon(icons.PCOLL_DLC_ID, dlc)
            display = col1.row()
            display.label(text=dlc.name, icon_value = custom_icon)

        elif dlc.status == StatusEnum.UPDATEABLE:
            custom_icon = get_icon(icons.PCOLL_DLC_ID, dlc)
            display = col2.row()
            display.label(text=dlc.name, icon_value = custom_icon)
            button = display.operator(
                "mcam.githubupdateinstall",
                icon="FILE_REFRESH"
                )
            button.data = dlc.name
            
        elif dlc.status == StatusEnum.INSTALLABLE:
            custom_icon = get_icon(icons.PCOLL_GITHUB_DLC_ID, dlc)
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