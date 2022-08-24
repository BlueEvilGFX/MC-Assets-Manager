import bpy
import importlib
import json

from bpy.props import *
from bpy.types import AddonPreferences

from .. import addon_updater_ops
from . import ui_modules
from . import update_functions
from .main_properties import AddonPreferencesProps
from ..load_modules import PACKAGE_NAME
from ..miscs import utils


@addon_updater_ops.make_annotations
class AddonPref(AddonPreferences):
    bl_idname = PACKAGE_NAME

    main_props : PointerProperty(type=AddonPreferencesProps)

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
        init_exists = utils.AddonPathManagement.getDLCInitPath(dlc)[1]                                     #   check init path and existence
        
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
            # bpy.ops.wm.save_userpref()
            try:
                pointerProperty = "bpy.props.PointerProperty(type=locals()[dlc].PreferencesProperty)"   #   --> dlc_propGroup: acces to property group
                exec(f'{dlc+"_propGroup"} : {pointerProperty}')                                         #   create PointerProperty to PropertyGroup
            except:
                print(f'McAM: could not read preference properties: {dlc}')

    def draw(self, context):
        layout = self.layout
        header = layout.row()
        header.prop(self.main_props, "menu", expand = True)
        header.operator("mcam.main_reload", text = "", icon = "FILE_REFRESH")

        #━━━━━━━━━━━━━
        scene = context.scene

        # ━━━━━━━━━━━━ assets
        if self.main_props.menu == "0":
            ui_modules.assets_tab(self, context, layout, scene)

        # ━━━━━━━━━━━━ DLCs
        elif self.main_props.menu == "1":
            ui_modules.dlc_tab(self, context, layout, scene)            
            ui_modules.showDlcPreferences(self, context)

        # ━━━━━━━━━━━━ online
        elif self.main_props.menu == "2":
            ui_modules.online_tab(self, context, layout)

        # ━━━━━━━━━━━━ settings
        elif self.main_props.menu == "3":
            ui_modules.show_settings(self, context, layout)