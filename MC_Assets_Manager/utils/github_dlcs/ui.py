from ..icons import basicMCAM_icon_collection
from .icons import github_dlc_icon_collections

def display_github_dlc(self, context, element=None):
    from .operators import github_gReaderReference, github_internetConnection

    if element == None:
        element = self.layout
    layout = element

    box = layout.box()
    box.label(text="Github DLC connector : shows only original DLCs")
    if not github_gReaderReference == None:
        row = box.row()
        row.operator("mcam.githubconnect", text="refresh", icon="FILE_REFRESH")

        pcoll = basicMCAM_icon_collection["McAM"]
        ic = "McAM_github"
        custom_icon = pcoll[ic].icon_id
        row.operator("wm.url_open", text="open website", icon_value = custom_icon).url = "https://github.com/BlueEvilGFX/McAM-DLCs"
    else:
        box.operator("mcam.githubconnect", text="connect", icon="WORLD_DATA")
       

    if not github_internetConnection or github_gReaderReference == None:
        layout.label(text="please connect to github")
        if github_internetConnection == False:
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

        for dlc in github_gReaderReference.dlc_list:
            try: 
                pcoll = github_dlc_icon_collections["DLCs"]
                ic = dlc.name
                custom_icon = pcoll[ic].icon_id
            except:
                custom_icon = 51
                
            if dlc.already_installed:
                #   installed
                if not dlc.update_available:
                    display = col1.row()
                    display.label(text=dlc.name, icon_value = custom_icon)
                #   update
                else:
                    display = col2.row()
                    display.label(text=dlc.name, icon_value = custom_icon)
                    button = display.operator("mcam.githubindupdateinstall", icon="FILE_REFRESH")
                    button.data = dlc.name
            #   not installed
            else:
                display = col3.row()
                display.label(text=dlc.name, icon_value = custom_icon)
                button = display.operator("mcam.githubindupdateinstall", icon = "IMPORT")
                button.data = dlc.name