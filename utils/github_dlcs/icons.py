import bpy
import os
import bpy.utils.previews
from .. import utils

#━━━━━━━━━━━━━━━    functions    ━━━━━━━━━━━━━━━━━━━━━━


def read_github_dlc_icons():
    addon_path = utils.AddonPathManagement.getAddonPath()
    icon_path = os.path.join(addon_path, "utils", "github_dlcs", "icons")

    if os.path.exists(icon_path):   
        for pcoll in github_dlc_icon_collections.values():
            bpy.utils.previews.remove(pcoll)
        github_dlc_icon_collections.clear()
        pcoll = bpy.utils.previews.new()

        for name in os.listdir(icon_path):
            path = os.path.join(icon_path, name)
            name = name.split(".")[0]
            if os.path.exists(path):
                pcoll.load(name, path, "IMAGE")

        github_dlc_icon_collections["DLCs"] = pcoll

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

github_dlc_icon_collections = {}

def register():
    # pcoll = bpy.utils.previews.new()
    # read_github_dlc_icons()
    # github_dlc_icon_collections["McAM"] = pcoll
    pass


def unregister():
    for pcoll in github_dlc_icon_collections.values():
        bpy.utils.previews.remove(pcoll)

    github_dlc_icon_collections.clear()