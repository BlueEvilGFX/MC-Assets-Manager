import bpy, urllib, os, zipfile

from MC_Assets_Manager.core import addonpreferences, utils

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GITHUB_OT_connect(bpy.types.Operator):
    bl_idname = "mcam.githubconnect"
    bl_label = ""

    def execute(self, context):
        from MC_Assets_Manager.core.utils import github_connect
        github_connect.connect()
        self.report({'INFO'}, "Successfull connection to Github")
        return{'FINISHED'}

class UpdateInstall(bpy.types.Operator):
    bl_idname = "mcam.githubupdateinstall"
    bl_label = ""
 
    data : bpy.props.StringProperty(
        name = "data",
        description = "contains data",
        default = ''
    )
 
    def execute(self, context):
        from MC_Assets_Manager.core.utils.github_connect import github_reader
        
        for dlc in github_reader.dlc_list:
            if dlc.name == self.data:
                dl_link = dlc.download_link
                break
        
        sta, owner = github_reader.sta_url, github_reader.rep_owner 
        repo, name = github_reader.repo, self.data         
        url = dl_link if dl_link else\
            f'{sta}/{owner}/{repo}/raw/main/{name}/{name}.dlc'

        dlc_dir = utils.paths.get_dlc_dir()
        save_location = os.path.join(dlc_dir, f'{self.data}.dlc')
        urllib.request.urlretrieve(url, save_location)

        with zipfile.ZipFile(save_location) as zip:
            zip.extractall(path = dlc_dir)

        os.remove(save_location)

        dlc.status = utils.github_connect.StatusEnum.INSTALLED
        github_reader.news = False

        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')            
        self.report({'INFO'}, f'{self.data} successfully updated/installed')
        return {'FINISHED'}

class UpdateInstallAll(bpy.types.Operator):
    bl_idname = "mcam.githubupdateinstallall"
    bl_label = "update / install all DLCs"
 
    def execute(self, context):
        from MC_Assets_Manager.core.utils.github_connect import github_reader

        #   dlc list full of dlcs which need to be installed or updated
        dlcs_to_manage = [dlc for dlc in github_reader.dlc_list\
            if dlc.status != utils.github_connect.StatusEnum.INSTALLED
            ]

        #   iterating over the dlcs to install / update them
        for dlc in dlcs_to_manage:
            dl_link = dlc.download_link
            sta, owner = github_reader.sta_url, github_reader.rep_owner 
            repo, name = github_reader.repo, dlc.name           
            url = dl_link if dl_link else\
                f'{sta}/{owner}/{repo}/raw/main/{name}/{name}.dlc'
            
            dlc_dir = utils.paths.get_dlc_dir()
            save_location = os.path.join(dlc_dir, f'{name}.dlc')
            urllib.request.urlretrieve(url, save_location)

            with zipfile.ZipFile(save_location) as zip:
                zip.extractall(path = dlc_dir)

            os.remove(save_location)

        for dlc in dlcs_to_manage:
            dlc.status = utils.github_connect.StatusEnum.INSTALLED

        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
        if utils.paths.get_dlc_init(name):
            addonpreferences.reload_addon_preferences()
        
        github_reader.news = False
        self.report({'INFO'}, "DLCs successfully updated/installed")
        return {'FINISHED'}

class GITHUB_OT_IGNORE(bpy.types.Operator):
    bl_idname = "mcam.githubignore"
    bl_label = "ignore"

    def execute(self, context):
        from MC_Assets_Manager.core.utils.github_connect import github_reader
        github_reader.news = False
        return{'FINISHED'}

def register():
    bpy.utils.register_class(GITHUB_OT_connect)
    bpy.utils.register_class(UpdateInstall)
    bpy.utils.register_class(UpdateInstallAll)
    bpy.utils.register_class(GITHUB_OT_IGNORE)

def unregister():
    bpy.utils.unregister_class(GITHUB_OT_IGNORE)
    bpy.utils.unregister_class(UpdateInstallAll)
    bpy.utils.unregister_class(UpdateInstall)
    bpy.utils.unregister_class(GITHUB_OT_connect)