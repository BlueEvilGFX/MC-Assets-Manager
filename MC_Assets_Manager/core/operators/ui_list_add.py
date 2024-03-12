import os
import json
import shutil
import zipfile

import bpy
from bpy.props import CollectionProperty, StringProperty, BoolProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from MC_Assets_Manager.core.utils import paths, asset_dict

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UI_LIST_OT_ADD(Operator, ImportHelper):
    """
    description:
        operator which adds an item to a list
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """
    bl_idname = "mcam.ui_list_add"
    bl_label = "add"

    asset_type : StringProperty() # type: ignore

    filter_glob : StringProperty(
        default = "*.blend;*.zip;*.rar",
        options = {"HIDDEN"}
        ) # type: ignore

    files : CollectionProperty(
        name='File paths', 
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
        ) # type: ignore

    link : BoolProperty(default=False, description=
                        "If False, the item will be saved into the addon \
storage folder.\n If True, the item will be linked and the item will be \
appended from the source. If the source file is deleted, the link is \
gone and the item vanishes from the ui list.") # type: ignore

    def execute(self, context):
        Adder = AssetAdder(self, self.files, self.asset_type)
        Adder.main()
        return{'FINISHED'}

    def draw(self, context):
        self.layout.prop(self, "link", icon="LINKED")

class AssetAdder:
    """
    description:
        operator class which performs the adding of items to the list ->
        copying files, reading in icons
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """

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
        self.dst_directory = paths.User.get_sub_asset_directory(asset_type)
        self.link = operator_reference.link
    
    def main(self) -> None:
        if self.link == False:
            for file in self.files:
                file = os.path.join(self.filedir, file.name)
                if file.endswith(".blend"):
                    self.add_file(file)
                elif file.endswith(".zip") or file.endswith(".rar"):
                    self.add_zip(file)
                else:
                    error_text = "one file has the wrong file format"
                    self.operator.report({'ERROR'}, error_text)
        else: # link True
            link_json = paths.User.get_links_json()

            with open(link_json, 'r') as json_file:
                data = json.load(json_file)

            for file in self.files:
                file_path = os.path.join(self.filedir, file.name)
                data[self.asset_type].append(file_path)

            with open(link_json, 'w') as file:
                json.dump(data, file, indent=4)

        asset_type = asset_dict.get_asset_types(
            self.asset_type,
            asset_dict.Selection.raw_type
            )
        bpy.ops.mcam.ui_list_reload(asset_type=asset_type)

    def add_file(self, file) -> None:
        # get name
        name = os.path.basename(file)
        name = os.path.splitext(name)[0]
        name = self.get_name(name) + ".blend"

        dst = os.path.join(self.dst_directory, name)
        shutil.copyfile(src=file, dst=dst)

    def copy_zip_file(self, file, temp_path) -> None:
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        with zipfile.ZipFile(file) as zip:
            zip.extractall(path = temp_path)

    def add_zip(self, file) -> None:
        temp_path = os.path.join(self.dst_directory, "temp")

        self.copy_zip_file(file, temp_path)

        files = os.listdir(temp_path)

        for file in files:
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
        taken_names = paths.User.get_sub_asset_list(self.asset_type)

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