import bpy, urllib, os, zipfile

from . import connect
from .. import utils
from ... import addonPreferences

github_gReaderReference = None
github_internetConnection = None
github_NEWS = False

def clear_github_data():
    global github_gReaderReference
    global github_internetConnection
    global github_NEWS
    
    github_gReaderReference = None
    github_internetConnection = None
    github_NEWS = False

def set_github_data(reference, connection, news) -> None:
    global github_gReaderReference
    global github_internetConnection
    global github_NEWS

    github_gReaderReference = reference
    github_internetConnection = connection
    github_NEWS = news

def set_news(news):
    global github_NEWS
    github_NEWS = news

class GITHUB_OT_connect(bpy.types.Operator):
    bl_idname = "mcam.githubconnect"
    bl_label = ""

    def get_data(self):
        global github_gReaderReference
        global github_internetConnection

        gReader = connect.GithubReader()

        github_internetConnection = not gReader.network_error
        if github_internetConnection:
            github_gReaderReference = gReader

    def execute(self, context):
        self.get_data()
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
        global github_gReaderReference

        for x in github_gReaderReference.dlc_list:
            if x.name == self.data:
                dl_link = x.download_link
                break

        if dl_link == None:
            sta = github_gReaderReference.sta_url
            owner = github_gReaderReference.rep_owner
            repo = github_gReaderReference.repo
            url = "%s/%s/%s/raw/main/%s/%s.dlc" % (sta, owner, repo, self.data, self.data)
        else:
            url = dl_link
        
        dlc_dir_location = utils.AddonPathManagement.getDlcDirPath()
        save_location = os.path.join(dlc_dir_location, "%s.dlc" % self.data)
        urllib.request.urlretrieve(url, save_location)

        target = save_location
        handle = zipfile.ZipFile(target)
        handle.extractall(path = dlc_dir_location)
        handle.close()

        os.remove(save_location)
        utils.AddonReloadManagement.reloadDlcJson()
        utils.AddonReloadManagement.reloadDlcList()

        for x in github_gReaderReference.dlc_list:
            if x.name == self.data:
                x.status = connect.StatusEnum.INSTALLED
                name = x.name
        github_gReaderReference.check_dlcs()

        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
        
        init_path = utils.AddonPathManagement.getDLCInitPath(name)[1]
        if init_path:
            addonPreferences.reload()
            
        self.report({'INFO'}, "%s successfully updated/installed" % self.data)
        return {'FINISHED'}

class UpdateInstallAll(bpy.types.Operator):
    bl_idname = "mcam.githubupdateinstallall"
    bl_label = "update / install all DLCs"
 
    def execute(self, context):
        global github_gReaderReference

        #   dlc list full of dlcs which need to be installed or updated
        dlcs_to_manage = [dlc for dlc in github_gReaderReference.dlc_list if dlc.status != connect.StatusEnum.INSTALLED]

        #   iterating over the dlcs to install / update them
        for dlc in dlcs_to_manage:
            dl_link = dlc.download_link

            #   get DLC from github
            if dl_link is None:
                sta = github_gReaderReference.sta_url
                owner = github_gReaderReference.rep_owner
                repo = github_gReaderReference.repo
                url = "%s/%s/%s/raw/main/%s/%s.dlc" % (sta, owner, repo, dlc.name, dlc.name)
            #   get dlc from link
            else:
                url = dl_link

            dlc_dir_location = utils.AddonPathManagement.getDlcDirPath()
            save_location = os.path.join(dlc_dir_location, f'{dlc.name}.dlc')
            urllib.request.urlretrieve(url, save_location)

            target = save_location
            handle = zipfile.ZipFile(target)
            handle.extractall(path = dlc_dir_location)
            handle.close()

            os.remove(save_location)
            utils.AddonReloadManagement.reloadDlcJson()
            utils.AddonReloadManagement.reloadDlcList()

            for x in github_gReaderReference.dlc_list:
                if x.name == dlc.name:
                    x.status = connect.StatusEnum.INSTALLED
                    name = x.name
                    break
            github_gReaderReference.check_dlcs()

        bpy.ops.mcam.main_reload('INVOKE_DEFAULT')
        init_path = utils.AddonPathManagement.getDLCInitPath(name)[1]
        if init_path:
            addonPreferences.reload()
            
        self.report({'INFO'}, "DLCs successfully updated/installed")
        return {'FINISHED'}

class GITHUB_OT_IGNORE(bpy.types.Operator):
    bl_idname = "mcam.githubignore"
    bl_label = "ignore"

    def execute(self, context):
        global github_NEWS
        github_NEWS = False
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