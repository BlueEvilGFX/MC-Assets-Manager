import importlib
import json
import traceback

import bpy
from bpy.props import *
from bpy.types import AddonPreferences

from MC_Assets_Manager import addon_updater_ops
from MC_Assets_Manager.core import utils
from MC_Assets_Manager.core.addonpreferences import ui_modules
from MC_Assets_Manager.core.addonpreferences.properties import \
    AddonPreferencesProps


@addon_updater_ops.make_annotations
class AddonPref(AddonPreferences):
    bl_idname = utils.paths.PACKAGE

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
    dlc_json = utils.paths.get_dlc_json()
    with open(dlc_json, "r") as file:
        data = json.load(file) 

    active_set_false = []
    for dlc in data:
        if utils.paths.get_dlc_init(dlc):
            try:
                if dlc in locals():
                    importlib.reload(eval(dlc))
                else:
                    locals()[dlc] = importlib.import_module(
                        name = f'.storage.dlcs.{dlc}',
                        package = utils.paths.PACKAGE
                    )

                try:
                    bpy.utils.register_class(locals()[dlc].PreferencesProperty)
                except: pass

                # dlc_propGroup: acces to property group
                pointer = "bpy.props.PointerProperty(type=locals()[dlc].PreferencesProperty)"
                #   creates PointerProperty to PropertyGroup
                exec(f'{dlc+"_propGroup"} : {pointer}')
            except Exception:
                print(traceback.format_exc())
                active_set_false.append(dlc)
    
    with open(dlc_json, "w") as file:
        for dlc in active_set_false:
            data[dlc]["active"] = False
        json.dump(data, file, indent=4)

    def draw(self, context):
        layout = self.layout
        header = layout.row()
        header.prop(self.main_props, "menu", expand = True)
        header.operator("mcam.main_reload", text = "", icon = "FILE_REFRESH")

        #━━━━━━━━━━━━━
        scene = context.scene

        # ━━━━━━━━━━━━ assets
        if self.main_props.menu == "Assets":
            ui_modules.assets_tab.draw_assets_tab(self, context)
        # ━━━━━━━━━━━━ DLCs
        elif self.main_props.menu == "DLCs":
            ui_modules.draw_dlc_tab(self, context, layout, scene)            
        #     ui_modules.showDlcPreferences(self, context)

        # ━━━━━━━━━━━━ online
        elif self.main_props.menu == "Online":
            ui_modules.draw_online_tab(self, context, layout)

        # ━━━━━━━━━━━━ settings
        elif self.main_props.menu == "Settings":
            ui_modules.settings_tab.draw_settings_tab(self, context)
