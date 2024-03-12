import os
import subprocess
import sys

import bpy
from bpy.props import StringProperty

from MC_Assets_Manager.core.utils import paths

class UI_LIST_OT_OPEN_DIR(bpy.types.Operator):
    """
    description:
        operator wich opens the directory of the asset type or the linked item
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of 
        | paths.USER_ASSETS
        | paths.USER_PRESETS 
        | paths.USER_RIGS
        or :: directory
    """
    bl_idname = "mcam.ui_list_open_dir"
    bl_label = "open"

    asset_type : StringProperty() # type: ignore

    def execute(self, context):
        if self.asset_type in {
            paths.AssetTypes.USER_ASSETS,
            paths.AssetTypes.USER_PRESETS,
            paths.AssetTypes.USER_RIGS
        }: 
            path = paths.User.get_sub_asset_directory(self.asset_type)
            path = os.path.normpath(path)
        else:
            path = self.asset_type

        try:
            if sys.platform == 'darwin':
                subprocess.check_call(['open', '--', path])
            elif sys.platform == 'linux2':
                subprocess.check_call(['gnome-open', '--', path])
            elif sys.platform == 'win32':
                subprocess.check_call(['explorer', path])
            return {'FINISHED'}
        except:
            return {"CANCELLED"}