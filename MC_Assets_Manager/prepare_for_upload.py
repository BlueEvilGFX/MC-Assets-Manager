import os, shutil, json, zipfile

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

    github_icon_dir = os.path.join(addon_path, "utils", "github_dlcs", "icons")
    if os.path.exists(github_icon_dir):
        shutil.rmtree(github_icon_dir)


def remove_files():
    path = os.path.join(addon_path, "files")
    for it in os.scandir(path):
        if it.is_dir():
            shutil.rmtree(it)


def clear_dlc_json():
    jFile = os.path.join(addon_path, "files", "dlcs.json")
    with open(jFile, "w") as jData:
        json.dump({}, jData)

def ziping():
    path = os.path.dirname(addon_path)
    destination = os.path.join(path, "MC_Assets_Manager.zip")

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                if not file.endswith(".zip"):
                    ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))

    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(addon_path, zipf)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

remove_files_bool = True if input("removing all files and make it ready for publishing? y/n: ") == "y" else False

if remove_files_bool:
    remove_pycache(addon_path)
    remove_files()
    clear_dlc_json()
    ziping()