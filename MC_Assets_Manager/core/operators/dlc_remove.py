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
            if paths.DLC.get_sub_init(dlc):
                module_name = ".storage.DLCs."+dlc
                globals()[dlc] = importlib.import_module(
                    name = module_name,
                    package = paths.PathConstants.PACKAGE
                )
                
                json_file = paths.McAM.get_dlc_main_json()
                with open(json_file) as dataFile:
                    data = json.load(dataFile)
                    if data[dlc]["active"]:
                        globals()[dlc].unregister()
        except:
            print(f"McAM: [DLC Unregistering] error: {dlc}")

        shutil.rmtree(paths.DLC.get_sub_directory(dlc))

        bpy.ops.mcam.main_reload()
        
        github_connect.GitHubReader().connect_threaded()
        self.report({'INFO'}, "dlc successully removed")
        return{'FINISHED'}