from . import addon_updater_ops
import bpy
import os, importlib, json
from .utils import utils
from .utils import github_dlcs

from bpy.props import EnumProperty, StringProperty, IntProperty, BoolProperty, PointerProperty
from bpy.types import AddonPreferences

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@addon_updater_ops.make_annotations
class AddonPref(AddonPreferences):
    bl_idname = __package__

    #   creates the menu enum (navbar)
    menu : EnumProperty(default = "0", items = [("0", "Presets", ""), ("1", "DLCs", ""), ("2", "Assets", ""), ("3", "Online", "")])

    #   creates the menu enum (assetsbar)
    assets_menu : EnumProperty(default = "0", items = [
        ('0', 'Items', 'Items', 'DOCUMENTS',0),
        ('1', 'Rigs', 'Rigs', 'OUTLINER_OB_ARMATURE',1),
        ('2', 'Others', 'Others', 'PARTICLE_DATA',2)
        ])

    online_menu : EnumProperty(default = "0", items = [
        ('0', 'Addon Updater', 'Addon Updater', 'RNA',0),
        ('1', 'Github', 'Github', 'OUTLINER_DATA_VOLUME',1),
        ])

    auto_check_update : bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False)

    updater_intrval_months : bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_intrval_days : bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=1,
        max=31)

    updater_intrval_hours : bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_intrval_minutes : bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)

    # load addon preferences from addon
    # load json dlc file
    addon_path = utils.AddonPathManagement.getAddonPath()
    file = os.path.join(addon_path, "files", "dlcs.json")
    with open(file, "r") as json_file:
        data = json.load(json_file) 

    for dlc in data:                                                                                    #   iterate over every dlc 
        init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]                                     #   check init path and existence
        
        if init_exists:                                                                                 #   --> if dlc is script based --> init file
            if dlc in locals():                                                                         #   if already loaded
                importlib.reload(eval(dlc))                                                             #   reload module
            else:
                module_name = ".files.DLCs."+dlc
                locals()[dlc] = importlib.import_module(name = module_name, package = __package__)      #   load module

            try:
                bpy.utils.register_class(locals()[dlc].PreferencesProperty)                             #   register PropertyGroup of dlc
            except:
                pass
            # bpy.ops.wm.save_userpref
            pointerProperty = "bpy.props.PointerProperty(type=locals()[dlc].PreferencesProperty)"       #   --> dlc_propGroup: acces to property group
            exec(f'{dlc+"_propGroup"} : {pointerProperty}')                                             #   create PointerProperty to PropertyGroup    

    def draw(self, context):
        layout = self.layout
        header = layout.row()
        header.prop(self, "menu", expand = True)
        header.operator("assetsaddon.reload", text = "", icon = "FILE_REFRESH")

        #━━━━━━━━━━━━━
        scene = context.scene

        if self.menu == "0":
            def presets_tab():
                smallHeader = layout.row()
                smallHeader.scale_y = 0.5
                row = smallHeader.box().row()
                row.label(text="Name")
                row.label(text="Source")
                smallHeader.label(text="", icon = "BLANK1")

                row = layout.row()
                row.template_list("PRESET_UL_List", "The_List", scene.mcAssetsManagerProps, "preset_list", scene.mcAssetsManagerProps, "preset_index")

                colMain = row.column()
                colFir = colMain.column()
                colFir.operator("preset_list.reload", text = "", icon = "FILE_REFRESH")
                colSec = colMain.column(align = True)
                colSec.operator("preset_list.add", text = "", icon = "ADD")
                colSec.operator("preset_list.remove", text = "", icon = "REMOVE")
                colThi = colMain.column(align = True)
                colThi.operator("preset_list.export", text = "", icon = "EXPORT")

                colFou = colMain.column(align = True)
                if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
                else: lock = "UNLOCKED"
                colFou.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)
            presets_tab()

        elif self.menu == "1":
            def dlc_tab():
                smallHeader = layout.row()
                smallHeader.scale_y = 0.5
                row = smallHeader.box().row()
                row.label(text="Name")
                row.label(text="Type")
                row.label(text="Creator")
                row.label(text="", icon ="BLANK1")
                smallHeader.label(text="", icon="BLANK1")

                row = layout.row()
                row.template_list("DLC_UL_List", "The_List", scene.mcAssetsManagerProps, "dlc_list", scene.mcAssetsManagerProps, "dlc_index")

                colMain = row.column()
                colFir = colMain.column()
                colFir.operator("dlc_list.reload", text = "", icon = "FILE_REFRESH")
                colSec = colMain.column(align = True)
                colSec.operator("dlc_list.add", text = "", icon = "ADD")
                colSec.operator("dlc_list.remove", text = "", icon = "REMOVE")

                colThi = colMain.column(align = True)
                if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
                else: lock = "UNLOCKED"
                colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)
            dlc_tab()

            def showDlcPreferences():
                dlc_list = context.scene.mcAssetsManagerProps.dlc_list
                if dlc_list:
                    #   get paths and more
                    addon_path = utils.AddonPathManagement.getAddonPath()
                    dlc_paths = os.path.join(addon_path, "files", "DLCs")
                    dlc_list = os.listdir(dlc_paths)

                    for dlc in dlc_list:
                        index = context.scene.mcAssetsManagerProps.dlc_index
                        active = context.scene.mcAssetsManagerProps.dlc_list[index].active              #   read active status of dlc
                        init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]                     #   check init path and existence

                        if self.data and active and init_exists:                                        #   if dlc exists & active & init file (script based)
                            if dlc in locals():                                                         #   if already loaded
                                importlib.reload(eval(dlc))                                             #   reload module
                            else:
                                module_name = ".files.DLCs."+dlc                                        #   get module name for importing
                                locals()[dlc] = importlib.import_module(name = module_name, package = __package__) 
                            
                            selected_dlc = str(dlc_list[index])                                         #   get selected dlc from ui list
                            dlc_name = os.path.splitext(locals()[dlc].__name__)[-1][1:]                 #   get dlc name from selection

                            if selected_dlc == dlc_name and active:                                     #   if selection is dlc from iteration
                                locals()[dlc].CustomAddonPreferences.display(self)                      #   draw addon preferences from dlc
            showDlcPreferences()
                                
        elif self.menu == "2":
            def assets_tab():
                lowerEnum = layout.row()
                lowerEnum.prop(self, "assets_menu", expand = True)
                lowerEnum.label(text="", icon = "BLANK1")
                smallHeader = layout.row()

                sm = smallHeader.column()
                smBox = sm.box()
                smr = smBox.row()
                smr.scale_y = 0.5
                smr.label(text="Name")
                smr.label(text="Source")

                right = smallHeader.row().column()

                #   assets
                if self.get("assets_menu") == 0:
                    row = sm
                    smr.label(text="Category")
                    row.template_list("ASSET_UL_List", "The_List", scene.mcAssetsManagerProps, "asset_list", scene.mcAssetsManagerProps, "asset_index")
                    colMain = right.column()
                    colFir = colMain.column()
                    colFir.operator("asset_list.reload", text = "", icon = "FILE_REFRESH")
                    colSec = colMain.column(align = True)
                    colSec.operator("asset_list.add", text = "", icon = "ADD")
                    colSec.operator("asset_list.remove", text = "", icon = "REMOVE")
                    colSec.operator("asset_list.export", text ="", icon = "EXPORT")

                    colThi = colMain.column(align = True)
                    if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
                    else: lock = "UNLOCKED"
                    colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)
                #   rigs
                elif self.get("assets_menu") == 1:
                    row = sm
                    row.template_list("RIG_UL_List", "The_List", scene.mcAssetsManagerProps, "rig_list", scene.mcAssetsManagerProps, "rig_index")
                    colMain = right.column()
                    colFir = colMain.column()
                    colFir.operator("rig_list.reload", text = "", icon = "FILE_REFRESH")
                    colSec = colMain.column(align = True)
                    colSec.operator("rig_list.add", text = "", icon = "ADD")
                    colSec.operator("rig_list.remove", text = "", icon = "REMOVE")
                    colSec.operator("rig_list.export", text ="", icon = "EXPORT")

                    colThi = colMain.column(align = True)
                    if context.scene.mcAssetsManagerProps.item_unlock == False: lock = "LOCKED"
                    else: lock = "UNLOCKED"
                    colThi.prop(context.scene.mcAssetsManagerProps, "item_unlock", text="", icon=lock)
                #   others
                else:
                    row = sm
                    row.label(text="thats 2 now")
                    row.label(text="thats 2 now")
                    row.label(text="thats 2 now")
                    row.label(text="thats 2 now")
            assets_tab()

        elif self.menu == "3":
            lowerEnum = layout.row()
            lowerEnum.prop(self, "online_menu", expand = True)
            lowerEnum.label(text="", icon = "BLANK1")

            if self.online_menu == "0":
                addon_updater_ops.update_settings_ui_medium(self, context, layout)
            elif self.online_menu == "1":
                github_dlcs.ui.display_github_dlc(self, context)

            
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

classes = (
            AddonPref,
          )
          
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)