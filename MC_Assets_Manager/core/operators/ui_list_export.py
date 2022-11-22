import os
import zipfile

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty

from MC_Assets_Manager.core.utils import paths

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UI_LIST_OT_EXPORT(Operator, ExportHelper):
    """
    description:
        operator wich exports the users content of a ui list
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """
    bl_idname = "mcam.ui_list_export"
    bl_label = "export"

    filename_ext = ".zip"

    asset_type : StringProperty()

    def execute(self, context):
        if not self.asset_type in {
            paths.USER_ASSETS,
            paths.USER_PRESETS,
            paths.USER_RIGS
            }: 
            return {'CANCELED'}

        path = paths.get_user_sub_asset_dir(self.asset_type)
        destination = self.filepath

        export_single(destination, path, self.asset_type, 'w')

        self.report({'INFO'}, f'{self.asset_type} successully exported')
        return{'FINISHED'}

class UI_LIST_OT_EXPORT_ALL(Operator, ExportHelper):
    """
    description:
        exports every user asset, preset and rig
    """
    bl_idname = "mcam.ui_list_export_all"
    bl_label = "export all"

    filename_ext = ".zip"

    def execute(self, context):
        destination = self.filepath

        path = paths.get_user_sub_asset_dir(paths.USER_ASSETS)
        export_single(destination, path, paths.USER_ASSETS, 'w')

        path = paths.get_user_sub_asset_dir(paths.USER_PRESETS)
        export_single(destination, path, paths.USER_PRESETS, 'a')

        path = paths.get_user_sub_asset_dir(paths.USER_RIGS)
        export_single(destination, path, paths.USER_RIGS, 'a')

        return {'FINISHED'}

def export_single(destination, path, asset_type, write_type):
    """
    args:
        destination: file path where the zip file is locatedd
        path: path to zip files from
        asset_type: enum from:
            paths.USER_ASSETS | paths.USER_PRESETS | paths.USER_RIGS
        write_type:
            'w' : overwrite completely
            'a' : add files to zip file
    """
    with zipfile.ZipFile(destination, write_type, zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk( os.path.join(
                paths.get_user_sub_icon_dir(asset_type)), zipf):
            for file in files:
                zipf.write( os.path.join(root, file), 
                    os.path.relpath(os.path.join(root, file), 
                    os.path.join(path, '..')))

        asset_dir = paths.get_user_sub_asset_dir(asset_type)
        for file_name in paths.get_user_sub_assets(asset_type):
            file = file_name + ".blend"
            file_path = os.path.join(asset_dir, file)
            zipf.write(file_path, os.path.join(asset_type, file))