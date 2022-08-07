import os
from .. import utils

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def execute(context, asset_type, list, index):
    # get path & data
    path = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", asset_type)
    files = [file for file in os.listdir(path) if not file == "icons"]
    file_path = os.path.join(path, files[index])
    icon_name = os.path.splitext(files[index])[0]+".png"
    icon_path = os.path.join(path, "icons", icon_name)
    # remove
    os.remove(file_path)
    if os.path.exists(icon_path):
        os.remove(icon_path)
    list.remove(index)
    index = min(max(0, index - 1), len(list) - 1)