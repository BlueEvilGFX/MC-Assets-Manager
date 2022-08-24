import os
import shutil
import zipfile

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def check_name(name, dir, x=0) -> str:
    '''
    returns new filename with extension
    dir is the function which gets the correct directory: icons or normal assets
    '''
    file = os.path.join(dir, name)
    if os.path.exists(file):
        return get_new_name(name, dir, x)
    else: return name

def get_new_name(name, dir, x ) -> str:
    x += 1
    name, extension =  os.path.splitext(name)
    split = name.split("_")[-1]
    if split.isnumeric():
        name = name[:-(len(split)+1)]
    name = "%s_%s%s" % (name, x, extension)
    return check_name(name, dir, x)

def add_file(file_path, assets_path):
    name = os.path.basename(file_path)
    destination = os.path.join(assets_path, check_name(name, assets_path))
    shutil.copyfile(src=file_path, dst=destination)

def add_pack(file_path, assets_path):
    temp_path = os.path.join(assets_path, "temp")
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    target = file_path
    handle = zipfile.ZipFile(target)
    handle.extractall(path = temp_path)
    handle.close()

    for file in os.listdir(temp_path):
        if file.endswith(".blend"):
            #   file
            preset_src_path = os.path.join(assets_path, "temp", file)
            preset_name = check_name(file, assets_path)
            file_destination = os.path.join(assets_path, preset_name)
            shutil.copyfile(src=preset_src_path, dst=file_destination)
            #   icon
            icon_name =  os.path.splitext(preset_name)[0]+".png"
            icon_src_name = os.path.splitext(file)[0]+".png"
            icon_src_path = os.path.join(assets_path, "temp", "icons", icon_src_name)
            icon_exists = os.path.exists(icon_src_path)
            if icon_exists:
                icon_path = os.path.join(assets_path, "icons")

                file_destination = os.path.join(icon_path, icon_name)
                shutil.copyfile(src=icon_src_path, dst=file_destination)

    shutil.rmtree(temp_path)

def execute(self, assets_dir_path) -> None:
    for file in self.files:
        # get path & data
        file_name = file.name
        file_path = os.path.join(os.path.dirname(self.filepath), file_name) #   get path of file to install

        # add / import
        if os.path.splitext(file_name)[1] == ".blend":
            add_file(file_path, assets_dir_path)                          #   add single preset file
        else:
            add_pack(file_path, assets_dir_path)                          #   add preset pack    