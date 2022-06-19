import os, shutil, json

file_path = os.path.realpath(__file__)
addon_path = os.path.dirname(file_path)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def remove_pycache(rootdir):
    for it in os.scandir(rootdir):
        if it.is_dir():
            remove_pycache(it)
            if os.path.basename(it) == "__pycache__":
                shutil.rmtree(it)
    updater_dir = os.path.join(addon_path, "mc_assets_manager_updater")
    if os.path.exists(updater_dir):
        shutil.rmtree(updater_dir)


def remove_files():
    path = os.path.join(addon_path, "files")
    for it in os.scandir(path):
        if it.is_dir():
            shutil.rmtree(it)


def clear_dlc_json():
    jFile = os.path.join(addon_path, "files", "dlcs.json")
    with open(jFile, "w") as jData:
        json.dump({}, jData)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

remove_chache_bool = True if input("removing pycache? y/n: ") == "y" else False
remove_files_bool = True if input("removing files? y/n: ") == "y" else False

if remove_chache_bool:
    remove_pycache(addon_path)
    print("removed cache")

if remove_files_bool:
    remove_files()
    clear_dlc_json()
    print("removed files")