import bpy, urllib, os, zipfile

from . import connect
from .. import utils

github_gReaderReference = None
github_internetConnection = None
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

class MessageBox(bpy.types.Operator):
    bl_idname = "mcam.githubmessagebox"
    bl_label = ""
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 450)
 
    def draw(self, context):
        layout = self.layout
        layout.alert = True
        layout.operator(
            "wm.quit_blender",
            text="Restart blender and then activate the dlc in the addon preferences",
            icon="BLANK1")

class UpdateInstall(bpy.types.Operator):
    bl_idname = "mcam.githubindupdateinstall"
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
        
        init_path = utils.AddonPathManagement.getInitPath(name)[1]
        if init_path:
            bpy.ops.mcam.githubmessagebox('INVOKE_DEFAULT')
            
        self.report({'INFO'}, "%s successfully updated/installed" % self.data)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MessageBox)
    bpy.utils.register_class(GITHUB_OT_connect)
    bpy.utils.register_class(UpdateInstall)

def unregister():
    bpy.utils.unregister_class(UpdateInstall)
    bpy.utils.unregister_class(GITHUB_OT_connect)
    bpy.utils.unregister_class(MessageBox)