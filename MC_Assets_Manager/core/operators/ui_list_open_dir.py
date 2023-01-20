import os
import subprocess
import sys

import bpy
from bpy.props import StringProperty

from MC_Assets_Manager.core.utils import paths

class UI_LIST_OT_OPEN_DIR(bpy.types.Operator):
    """
    description:
        operator wich exports the users content of a ui list
        returns {'CANCELLED'} if asset_type is invalid
    args:
        asset_type : enum of paths.USER_ASSETS | paths.USER_PRESETS 
        | paths.USER_RIGS
    """
    bl_idname = "mcam.ui_list_open_dir"
    bl_label = "open"

    asset_type : StringProperty()

    def execute(self, context):
        if not self.asset_type in {
            paths.USER_ASSETS,
            paths.USER_PRESETS,
            paths.USER_RIGS
            }: 
            return {'CANCELLED'}

        path = paths.get_user_sub_asset_dir(self.asset_type)
        path = os.path.normpath(path)

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