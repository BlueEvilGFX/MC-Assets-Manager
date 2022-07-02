import os
import zipfile

from .. import utils

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def poll(assets):
    addonPath = utils.AddonPathManagement.getAddonPath()
    path = os.path.join(addonPath, "files", assets)
    files = [file for file in os.listdir(path) if file.endswith(".blend")]
    return False if not files else True

def _zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write( os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                        os.path.join(path, '..')))

def execute(self, assets, assetsList) -> None:
    addonPath = utils.AddonPathManagement.getAddonPath()
    path = os.path.join(addonPath, "files", assets)
    destination = self.filepath

    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
        _zipdir(os.path.join(path, "icons"), zipf)

        for fileName in assetsList:
            filePath = os.path.join(path, fileName)
            zipf.write(filePath, fileName)