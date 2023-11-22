import os
import zipfile

import bpy
from bpy.props import CollectionProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from MC_Assets_Manager.core.addonpreferences import reload_addon_preferences
from MC_Assets_Manager.core.utils import paths, reload

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_OT_Add(Operator, ImportHelper):
    bl_idname = "mcam.dlc_list_add"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.dlc", options = {"HIDDEN"})
    files : CollectionProperty(
        name='File paths',
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
        )

    def add(self, path):
        pre_dir_path = paths.DLC.get_directory()
        # add / import
        target = path
        handle = zipfile.ZipFile(target)
        handle.extractall(path = pre_dir_path)
        handle.close()

    def execute(self, context):
        for file in self.files:
            file_name = file.name
            filepath = os.path.join(os.path.dirname(self.filepath), file_name)

            self.add(filepath)

        reload.reload_dlc_json()
        reload.reload_dlc_list()

        dlc = os.path.splitext(os.path.basename(self.filepath))[0]
        init_path = paths.DLC.get_sub_init(dlc)

        if init_path:
            reload_addon_preferences()

        bpy.ops.mcam.main_reload()
        self.report({'INFO'}, "dlc successully added")
        return{'FINISHED'}
