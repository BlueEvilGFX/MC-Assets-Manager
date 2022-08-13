import os, shutil, json, zipfile, time

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UPLOAD_PREPARE:
    
    def __init__(self) -> None:
        self.file_path = os.path.realpath(__file__)
        self.addon_path = os.path.dirname(self.file_path) 

    def remove_pychache(self, rootdir=None):
        if rootdir is None: rootdir = self.addon_path

        for it in os.scandir(rootdir):
            if it.is_dir():
                self.remove_pychache(it)
                if os.path.basename(it) == "__pycache__":
                    shutil.rmtree(it)
        updater_dir = os.path.join(self.addon_path ,"addon_updater", "mc_assets_manager_updater")
        if os.path.exists(updater_dir):
            shutil.rmtree(updater_dir)

        github_icon_dir = os.path.join(self.addon_path, "utils", "github_dlcs", "icons")
        if os.path.exists(github_icon_dir):
            shutil.rmtree(github_icon_dir)

    def remove_files(cls):
        path = os.path.join(cls.addon_path, "files")
        for it in os.scandir(path):
            if it.is_dir():
                shutil.rmtree(it)

    def clear_dlc_json(cls):
        jFile = os.path.join(cls.addon_path, "files", "dlcs.json")
        with open(jFile, "w") as jData:
            json.dump({}, jData)

    def ziping(cls):
        path = os.path.dirname(cls.addon_path)
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
            zipdir(cls.addon_path, zipf)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

remove_files_bool = True if input("removing all files and make it ready for publishing? y/n: ") == "y" else False

if remove_files_bool:
    print("initializing...")
    prepare = UPLOAD_PREPARE()

    print("removing pychache...")
    prepare.remove_pychache()

    print("removing files...")
    prepare.remove_files()

    print("clearing dlc json...")
    prepare.clear_dlc_json()

    print("ziping...")
    prepare.ziping()

    print("\ndone!")
    time.sleep(1)