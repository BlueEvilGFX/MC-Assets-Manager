import os

#   creating all directories needed for the addon
def pathExists(path):
    return os.path.exists(path)

def setup():
    main_path = os.path.dirname(os.path.realpath(__file__))
    files_path = os.path.join(main_path, "files")

    dlcs = os.path.join(files_path, "DLCs")

    o_assets= os.path.join(files_path, "own_assets")
    o_rigs = os.path.join(files_path, "own_rigs")
    o_presets = os.path.join(files_path, "own_presets")

    o_assets_icons = os.path.join(o_assets, "icons")
    o_rigs_icons = os.path.join(o_rigs, "icons")
    o_presets_icons = os.path.join(o_presets, "icons")

    paths = [dlcs, o_assets, o_rigs, o_presets, o_assets_icons, o_rigs_icons, o_presets_icons]

    for p in paths:
        if not pathExists(p):
            os.mkdir(p)