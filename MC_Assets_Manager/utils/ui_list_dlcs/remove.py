import json
import bpy
import importlib
import os
import shutil
from .. import utils
from ..icons import reloadDLCIcons, reloadPresetIcons

from ...load_modules import PACKAGE_NAME

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DLC_OT_Remove(Operator):
    bl_idname = "mcam.dlc_list_remove"
    bl_label = "remove"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        try: item = scene.mcAssetsManagerProps.dlc_list[scene.mcAssetsManagerProps.dlc_index]
        except: pass
        try: return (context.scene.mcAssetsManagerProps.item_unlock)
        except: pass

    @reloadDLCIcons(1)
    @reloadPresetIcons(1)
    def execute(self, context):
        # get path & data
        path = os.path.join(utils.AddonPathManagement.getAddonPath(), "files", "DLCs")
        files = os.listdir(path)
        dlc_list = context.scene.mcAssetsManagerProps.dlc_list
        index = context.scene.mcAssetsManagerProps.dlc_index

        #   unregister the module if the dlc is a module
        file = os.path.join(path, files[index])
        dlc = os.path.basename(file)
        init_path = os.path.join(path, dlc, "__init__.py")
        path_exists = os.path.exists(init_path)
        
        if path_exists:
            module_name = ".files.DLCs."+dlc
            locals()[dlc] = importlib.import_module(name = module_name, package = PACKAGE_NAME)
            jFile = utils.AddonPathManagement.getDlcMainJson()
            with open(jFile) as dataFile:
                data = json.load(dataFile)
                if data[dlc]["active"]:
                    locals()[dlc].unregister()
            
        # remove
        shutil.rmtree(file)
        dlc_list.remove(index)
        context.scene.mcAssetsManagerProps.dlc_index = min(max(0, index - 1), len(dlc_list) - 1)
        utils.AddonReloadManagement.reloadDlcJson()
        utils.AddonReloadManagement.reloadPresetList()
        utils.AddonReloadManagement.reloadAssetList()
        utils.AddonReloadManagement.reloadRigList()
        self.report({'INFO'}, "dlc successully removed")
        return{'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(DLC_OT_Remove)

def unregister():
    bpy.utils.unregister_class(DLC_OT_Remove)