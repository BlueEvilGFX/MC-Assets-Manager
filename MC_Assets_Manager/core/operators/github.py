import bpy, urllib, os, zipfile, json, datetime

from MC_Assets_Manager.core import addonpreferences, utils
from MC_Assets_Manager.core.utils.github_connect import GitHubReader
from MC_Assets_Manager.core.utils import paths

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GITHUB_OT_connect(bpy.types.Operator):
    bl_idname = "mcam.githubconnect"
    bl_label = ""

    def execute(self, context):
        from MC_Assets_Manager.core.utils import paths
        bpy.ops.mcam.ui_list_reload(asset_type=paths.AssetTypes.DLCS)
        GitHubReader().connect_threaded()
        return{'FINISHED'}

def install_dlc(dlc, github_reader):
    sta, owner = github_reader._sta_url, github_reader._rep_owner 
    repo, name = github_reader._repo, dlc.name     
    url = dlc.download_link if dlc.download_link else\
        f'{sta}/{owner}/{repo}/raw/main/{name}/{name}.dlc'

    dlc_dir = utils.paths.DLC.get_directory()
    save_location = os.path.join(dlc_dir, f'{name}.dlc')
    urllib.request.urlretrieve(url, save_location)

    with zipfile.ZipFile(save_location, 'r') as zip:
        zip.extractall(path = dlc_dir)

    os.remove(save_location)
    dlc.status = utils.github_connect.StatusEnum.INSTALLED
    dlc.installed_version = dlc.online_version
    
class UpdateInstall(bpy.types.Operator):
    bl_idname = "mcam.githubupdateinstall"
    bl_label = ""
 
    data : bpy.props.StringProperty(
        name = "data",
        description = "contains data",
        default = ''
    ) # type: ignore
 
    def execute(self, context):
        github_reader = GitHubReader()
        for dlc in github_reader.dlc_list:
            if dlc.name == self.data:
                break
        
        install_dlc(dlc, github_reader)
        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
        
        self.report({'INFO'}, f'{self.data} successfully updated/installed')
        return {'FINISHED'}

class UpdateInstallAll(bpy.types.Operator):
    bl_idname = "mcam.githubupdateinstallall"
    bl_label = "update / install all DLCs"
 
    def execute(self, context):
        from MC_Assets_Manager.core.utils.github_connect import GitHubReader
        github_reader = GitHubReader()

        #   dlc list full of dlcs which need to be installed or updated
        dlcs_to_manage = [dlc for dlc in github_reader.dlc_list\
            if dlc.status != utils.github_connect.StatusEnum.INSTALLED
            ]

        #   iterating over the dlcs to install / update them
        reload_preferences = False
        for dlc in dlcs_to_manage:
            install_dlc(dlc, github_reader)
            reload_preferences = utils.paths.DLC.get_sub_init(dlc.name)

        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')

        if reload_preferences:
            addonpreferences.reload_addon_preferences()
        
        github_reader._news = False
        self.report({'INFO'}, "DLCs successfully updated/installed")
        return {'FINISHED'}

class GITHUB_OT_IGNORE(bpy.types.Operator):
    bl_idname = "mcam.githubignore"
    bl_label = "ignore"

    def execute(self, context):
        from MC_Assets_Manager.core.utils.github_connect import GitHubReader
        GitHubReader()._news = False

        # read date file
        dlc_date_file = paths.McAM.get_dlc_last_ignored_json_file()
        with open(dlc_date_file, 'r') as fb:
            data = json.load(fb)

        # set new date
        with open(dlc_date_file, 'w') as fb:
            data["last_ignored"] = str(datetime.datetime.now().date())
            json.dump(data, fb, indent=4,)
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