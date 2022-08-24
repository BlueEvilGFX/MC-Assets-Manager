import bpy
from threading import Thread
from . import connect
from .operators import set_github_data
from ...miscs import utils

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def auto_check() -> None:
    gReader = connect.GithubReader()
    connection = not gReader.network_error
    if connection:
        reference = gReader
        for dlc in reference.dlc_list:
            #   display of DLCs
            if dlc.status == connect.StatusEnum.INSTALLABLE or dlc.status ==  connect.StatusEnum.UPDATEABLE:
                news = True
                break
            else:
                news = False

    set_github_data(reference, connection, news)    

def create_auto_check_thread() -> None:
    preferences = utils.AddonPreferencesProperties.getAddonPropAccess()
    if preferences.main_props.auto_check_dlc:
        t = Thread(target=auto_check)
        t.start()