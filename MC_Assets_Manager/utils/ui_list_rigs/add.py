import bpy
import os
import shutil
import zipfile

from .. import utils

from bpy.props import StringProperty, CollectionProperty
from bpy.types import  Operator
from bpy_extras.io_utils import ImportHelper

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RIG_OT_Add(Operator, ImportHelper):
    bl_idname = "rig_list.add"
    bl_label = "add"

    filter_glob : StringProperty(default = "*.blend;*.zip;*.rar", options = {"HIDDEN"})
    files : CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    def checkNewName(self, preset, presetX, preDirPath, x):
        #   check name if it already exists --> if yes, increment additional number by one
        path_to_create = os.path.join(preDirPath, presetX)
        path_exists = os.path.exists(path_to_create)
        if path_exists:
            x += 1
            presetX = os.path.splitext(preset)[0] + "_%s.blend" % str(x)
            return self.checkNewName(preset, presetX, preDirPath, x)
        else:
            return presetX


    def add_file(self, file_path, assets_path, preset_names, context):
        name = os.path.splitext(os.path.basename(file_path))[0]
        destination = os.path.join(assets_path, name+".blend")
        preset = name + ".blend"

        # iterate over all own asset if preset name already exists
        if name+".blend" in preset_names:
            x = 0                                                               #   start by number 0
            presetX = preset                                                    #   reference presetX as preset
            presetX = self.checkNewName(preset, presetX, assets_path, x)        #   check if name already exists
            oldName = os.path.join(assets_path, preset)                    
            newName = os.path.join(assets_path, presetX)
            os.rename(oldName,newName)                                          #   rename blend file which already exists with the new name with number
        shutil.copyfile(src=file_path, dst=destination)                         #   copy asset file with its "normal" name
        utils.AddonReloadManagement.reloadRigList()
        self.report({'INFO'}, "rig successully added")


    def add_pack(self, file_path, assets_path, preset_names, context):
        target = file_path
        handle = zipfile.ZipFile(target)
        zipNames = handle.namelist()

        # iterate over all own presets if preset name already exists
        for preset in preset_names:
            if preset in zipNames:                                              #   if file is in the zip file
                x = 0                                                           #   start by number one
                presetX = preset                                                #   reference presetX as preset
                presetX = self.checkNewName(preset, presetX, assets_path, x)
                oldName = os.path.join(assets_path, preset)
                newName = os.path.join(assets_path, presetX)
                os.rename(oldName,newName)                                      #   rename blend file which already exists with the new name with number
        handle.extractall(path = assets_path)                                   #   unpack zip file
        handle.close()
        utils.AddonReloadManagement.reloadRigList()
        self.report({'INFO'}, "rig pack successully added")


    def add(self, context):
        for file in self.files:
            # get path & data
            file_name = file.name
            file_path = os.path.join(os.path.dirname(self.filepath), file_name) #   get path of file to install
            rig_path = utils.AddonPathManagement.getOwnRigsDirPath()
            preset_names = os.listdir(rig_path)

            # add / import
            if os.path.splitext(file_name)[1] == ".blend":
                self.add_file(file_path, rig_path, preset_names, context)       #   add single preset file
            else:
                self.add_pack(file_path, rig_path, preset_names, context)       #   add preset pack

    def execute(self, context):
        self.add(context)
        return{'FINISHED'}


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          
def register():
    bpy.utils.register_class(RIG_OT_Add)
  
def unregister():
    bpy.utils.unregister_class(RIG_OT_Add)
