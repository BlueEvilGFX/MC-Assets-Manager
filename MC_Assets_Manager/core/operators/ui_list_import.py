import os
import shutil
import zipfile

import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from MC_Assets_Manager.core.utils import paths

class UI_LIST_OT_IMPORT_ASSET_COMPOUND(Operator, ImportHelper):
    """
    Operator which imports a asset compound .zip file
    """
    
    bl_idname = "mcam.add_asset_compound"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.zip;*.rar", options = {"HIDDEN"})

    def execute(self, context):
        temp_path = os.path.join(paths.PathConstants.STORAGE_DIRECTORY, "temp")
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)

        with zipfile.ZipFile(self.filepath) as zip:
            zip.extractall(path = temp_path)

        categories = os.listdir(temp_path)
        for category in categories:
            validation = {
                paths.AssetTypes.USER_ASSETS,
                paths.AssetTypes.USER_PRESETS,
                paths.AssetTypes.USER_RIGS
                }

            if not category in validation:
                continue

            category_path = os.path.join(temp_path, category)
            files = os.listdir(category_path)

            for file in files:
                if not file.endswith(".blend"):
                    continue
                # file
                src_path = os.path.join(category_path, file)
                name = os.path.splitext(file)[0]
                name = self.get_name(name, category) + ".blend"
                dst_path = os.path.join(
                    paths.User.get_sub_icon_directory(category),
                    name
                    )

                shutil.copyfile(src = src_path, dst = dst_path)
                
                # icon
                src_name = os.path.splitext(file)[0] + ".png"
                src_path = os.path.join(category_path, "icons", src_name)
                name = os.path.splitext(name)[0] + ".png"
                if os.path.exists(src_path):
                    dst_path = os.path.join(
                        paths.User.get_sub_icon_directory(category),
                        name
                    )
                    shutil.copyfile(src = src_path, dst = dst_path)


        shutil.rmtree(temp_path)

        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.ASSETS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.PRESETS)
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.RIGS)

        self.report({'INFO'}, "successully exported asset compound")
        return{'FINISHED'}

    def get_name(self, name, category) -> str:
        """
        args:
            name : string for the input name
            category : 
                enum : paths.USER_ASSETS | paths.USER_PRESETS | paths.USER_RIGS
        returns name with the next valid id -> name_id
        """
        taken_names = paths.User.get_sub_asset_list(category)

        # return name if name is not taken
        if not name in taken_names:
            return name

        taken_names = [file_name for file_name in taken_names\
                         if name in file_name]
        highest_name = max(taken_names)

        # create new name with starter id: 1
        if not "_" in highest_name:
            return name + "_1"
        if not highest_name.split("_")[-1].isdigit():
            return name + "_1"
        # increment id by 1
        id = int(highest_name.split("_")[-1]) + 1
        return name + '_' + str(id)