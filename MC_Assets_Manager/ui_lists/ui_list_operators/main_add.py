import bpy

import os, shutil

from ...miscs import utils
from ..ui_list_utils import add

class Main_ADD_EXEC:

    def __init__(self):
        self._extension = None

        self._asset_files = None
        self._asset_type = None
        self._asset_source_dir = None

        self._operator_reference = None

        self._set_icon = None
        self._icon_files = None
        self._icon_source_dir = None

    #━━━━━━━━━━━━━

    def set_asset_files(self, asset_files, asset_type, asset_source_dir, operator_reference):
        self._asset_files = asset_files
        self._asset_type = asset_type
        self._asset_source_dir = asset_source_dir
        self._operator_reference = operator_reference
    
    def set_icon_init(self, icon) -> None:
        self._set_icon = icon

    def set_icon_files(self, icon_files, icon_source_dir, operator_reference):
        self._icon_files = icon_files
        self._icon_source_dir = icon_source_dir
        self._operator_reference = operator_reference

    #━━━━━━━━━━━━━

    def execute(self):
        def copy_asset():
            for file in self._asset_files:
                source_asset = os.path.join(self._asset_source_dir, file)
                if os.path.splitext(file)[1] == ".zip":
                    add.add_pack(source_asset, self.get_asset_dir())
                else:
                    name = self.check_name(file, self.get_asset_dir)
                    destination = os.path.join(self.get_asset_dir(), name)
                    shutil.copyfile(src=source_asset, dst=destination)

        def copy_both():
            for file in self._asset_files:
                source_asset = os.path.join(self._asset_source_dir, file)
                if os.path.splitext(file)[1] == ".zip":
                    add.add_pack(source_asset, self.get_asset_dir())
                else:
                    name = self.check_name(file, self.get_asset_dir)
                    source_asset = os.path.join(self._asset_source_dir, file)
                    destination_asset = os.path.join(self.get_asset_dir(), name)
                    shutil.copyfile(src=source_asset, dst=destination_asset)

                    original_name = os.path.splitext(file)[0]
                    icon_src_name = original_name+".png"
                    if icon_src_name in self._icon_files:
                        source_icon = os.path.join(self._icon_source_dir, icon_src_name)
                        name = name.split(".")[0]
                        destination_icon = os.path.join(self.get_icon_dir(), name+".png")
                        shutil.copyfile(src=source_icon, dst=destination_icon)
                    
        if not self._set_icon:        
            copy_asset()
        else:
            copy_both()


        #   copy icons
        if self._set_icon:
            pass

        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
        self._operator_reference.report({'INFO'}, "asset successully added")

    #━━━━━━━━━━━━━

    def get_icon_dir(self) -> os.path:
        path = os.path.join(self.get_asset_dir(), "icons")
        return path

    def get_asset_dir(self) -> os.path:
        addon_path = utils.AddonPathManagement.getAddonPath()
        path = os.path.join(addon_path, "files", self._asset_type)
        return path

    def check_name(self, name, dir, x=0) -> str:
        '''
        returns new filename with extension
        dir is the function which gets the correct directory: icons or normal assets
        '''
        file = os.path.join(dir(), name)
        if os.path.exists(file):
            return self.get_new_name(name, dir, x)
        else: return name

    def get_new_name(self, name, dir, x ) -> str:
        x += 1
        name, extension =  os.path.splitext(name)
        split = name.split("_")[-1]
        if split.isnumeric():
            name = name[:-(len(split)+1)]
        name = "%s_%s%s" % (name, x, extension)
        return self.check_name(name, dir, x)