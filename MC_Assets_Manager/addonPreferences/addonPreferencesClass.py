import bpy, importlib, json

from bpy.props import *
from bpy.types import AddonPreferences

from .. import addon_updater_ops
from ..load_modules import PACKAGE_NAME
from ..utils import utils
from . import ui_modules

@addon_updater_ops.make_annotations
class AddonPref(AddonPreferences):
    bl_idname = PACKAGE_NAME

    #   creates the menu enum (navbar)
    menu : EnumProperty(default = "0", items = [("0", "Assets", ""), ("1", "DLCs", ""), ("2", "Online", ""),
                                                ('3', '', '', 'SETTINGS', 3)])

    #   creates the menu enum (assetsbar)
    assets_menu : EnumProperty(default = "0", items = [
        ('0', 'Presets', 'Presets', 'OUTLINER_OB_ARMATURE',0),
        ('1', 'Assets', 'Assets', 'DOCUMENTS',1),
        ('2', 'Rigs', 'Rigs', 'ARMATURE_DATA',2)
        ])

    online_menu : EnumProperty(default = "0", items = [
        ('0', 'Addon Updater', 'Addon Updater', 'RNA',0),
        ('1', 'Github', 'Github', 'OUTLINER_DATA_VOLUME',1),
        ])

    #   auto check dlc updater
    auto_check_dlc : BoolProperty(default=True, description="checking automatically for dlc updates every time blender starts")

    #   two UIs : DLCs in the n panel
    two_dlc_ui_panels : BoolProperty(default=False)

    #   reload all while starting blender
    reload_all_during_startup : BoolProperty(default=False)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    #   theDuckCow addon updater
    auto_check_update : bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False)

    updater_interval_months : bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_interval_days : bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=1,
        max=31)

    updater_interval_hours : bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes : bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)

    # ━━━━━━━━━━━━ loading dlc preferences
    dlc_json_path = utils.AddonPathManagement.getDlcMainJson()
    with open(dlc_json_path, "r") as json_file:
        data = json.load(json_file) 
    for dlc in data:                                                                                    #   iterate over every dlc 
        init_exists = utils.AddonPathManagement.getInitPath(dlc)[1]                                     #   check init path and existence
        
        if init_exists:                                                                                 #   --> if dlc is script based --> init file
            if dlc in locals():                                                                         #   if already loaded
                importlib.reload(eval(dlc))                                                             #   reload module
            else:
                module_name = ".files.DLCs."+dlc
                locals()[dlc] = importlib.import_module(name = module_name, package = PACKAGE_NAME)          #   load module

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
        header.operator("mcam.main_reload", text = "", icon = "FILE_REFRESH")

        #━━━━━━━━━━━━━
        scene = context.scene

        # ━━━━━━━━━━━━ assets
        if self.menu == "0":
            ui_modules.assets_tab(self, context, layout, scene)

        # ━━━━━━━━━━━━ DLCs
        elif self.menu == "1":
            ui_modules.dlc_tab(self, context, layout, scene)            
            ui_modules.showDlcPreferences(self, context)

        # ━━━━━━━━━━━━ online
        elif self.menu == "2":
            ui_modules.online_tab(self, context, layout)

        # ━━━━━━━━━━━━ settings
        elif self.menu == "3":
            ui_modules.show_settings(self, context, layout)