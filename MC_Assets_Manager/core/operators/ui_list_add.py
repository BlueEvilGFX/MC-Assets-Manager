import os
import shutil
import zipfile

import bpy
from bpy.props import CollectionProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from MC_Assets_Manager.core.utils import paths, reload

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UI_LIST_OT_ADD(Operator, ImportHelper):
    """
    description:
        operator wich adds an item to a list
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """
    bl_idname = "mcam.ui_list_add"
    bl_label = "add"

    asset_type : StringProperty()

    filter_glob : StringProperty(
        default = "*.blend;*.zip;*.rar",
        options = {"HIDDEN"}
        )

    files : CollectionProperty(
        name='File paths', 
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
        )

    def execute(self, context):
        Adder = AssetAdder(self, self.files, self.asset_type)
        Adder.main()
        return{'FINISHED'}

    def draw(self, context):
        pass

class AssetAdder:
    """
    description:
        operator class which performs the adding of items to hte list ->
        copying files, reading in icons
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """
    list_dict = {
        paths.USER_ASSETS : paths.ASSETS,
        paths.USER_PRESETS : paths.PRESETS,
        paths.USER_RIGS : paths.RIGS
    }

    def __init__(self, operator_reference, files, asset_type):
        """
        args:
            asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
            | paths.USER_RIGS
        """
        self.files = files
        self.filedir = os.path.dirname(operator_reference.filepath)
        self.operator = operator_reference
        self.asset_type = asset_type
        self.dst_directory = paths.get_user_sub_asset_dir(asset_type)
    
    def main(self) -> None:
        for file in self.files:
            file = os.path.join(self.filedir, file.name)
            if file.endswith(".blend"):
                self.add_file(file)
            elif file.endswith(".zip") or file.endswith(".rar"):
                self.add_zip(file)
            else:
                error_text = "one file has the wrong file format"
                self.operator.report({'ERROR'}, error_text)

        asset_type = self.list_dict[self.asset_type]
        bpy.ops.mcam.ui_list_reload(asset_type=asset_type)

    def add_file(self, file) -> None:
        # get name
        name = os.path.basename(file)
        name = os.path.splitext(name)[0]
        name = self.get_name(name) + ".blend"

        dst = os.path.join(self.dst_directory, name)
        shutil.copyfile(src=file, dst=dst)

    def add_zip(self, file) -> None:
        temp_path = os.path.join(self.dst_directory, "temp")
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        target = file
        handle = zipfile.ZipFile(target)
        handle.extractall(path = temp_path)
        handle.close()

        for file in os.listdir(temp_path):
            if file.endswith(".blend"):
                src_path = os.path.join(temp_path, file)
                # get name
                name = os.path.basename(file)
                name = os.path.splitext(name)[0]
                name = self.get_name(name) + ".blend"

                file_destination = os.path.join(self.dst_directory, name)
                shutil.copyfile(src=src_path, dst=file_destination)
                # icon
                icon_name =  os.path.splitext(name)[0]+".png"
                icon_src_name = os.path.splitext(file)[0]+".png"
                icon_src_path = os.path.join(self.dst_directory, "temp", "icons", icon_src_name)
                icon_exists = os.path.exists(icon_src_path)
                if icon_exists:
                    icon_path = os.path.join(self.dst_directory, "icons")

                    file_destination = os.path.join(icon_path, icon_name)
                    shutil.copyfile(src=icon_src_path, dst=file_destination)
        shutil.rmtree(temp_path)

    def get_name(self, name) -> str:
        """
        args:
            name : string for the input name ->
            returns name with the next valid id -> name_id
        """
        taken_names = paths.get_user_sub_assets(self.asset_type)

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
