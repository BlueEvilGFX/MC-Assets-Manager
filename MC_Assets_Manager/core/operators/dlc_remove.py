import importlib
import json
import shutil

import bpy
from bpy.types import Operator
from MC_Assets_Manager.core.utils import paths, github_connect

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_OT_Remove(Operator):
    bl_idname = "mcam.dlc_list_remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try:
            dlc  = scene.mc_assets_manager_props.dlc_list[
                scene.mc_assets_manager_props.dlc_index
            ]
            return scene.mc_assets_manager_props.item_unlock
        except:
            return False

    def execute(self, context):
        scene = context.scene
        dlc  = scene.mc_assets_manager_props.dlc_list[
                scene.mc_assets_manager_props.dlc_index
                ].name

        try:
            if paths.get_dlc_init(dlc):
                module_name = ".storage.DLCs."+dlc
                locals()[dlc] = importlib.import_module(
                    name = module_name,
                    package = paths.PACKAGE
                )
                
                json_file = paths.get_dlc_json()
                with open(json_file) as dataFile:
                    data = json.load(dataFile)
                    if data[dlc]["active"]:
                        locals()[dlc].unregister()
        except:
            print(f"McAM: [DLC Unregistering] error: {dlc}")

        shutil.rmtree(paths.get_dlc_sub_dir(dlc))

        bpy.ops.mcam.main_reload()
        github_connect.check_in_background()
        self.report({'INFO'}, "dlc successully removed")
        return{'FINISHED'}