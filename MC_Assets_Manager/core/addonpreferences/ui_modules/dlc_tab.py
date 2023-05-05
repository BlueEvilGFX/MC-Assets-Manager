import importlib
import traceback

from MC_Assets_Manager.core.utils import paths

def draw_dlc_tab(self, context, layout, scene):
    smallHeader = layout.row()
    smallHeader.scale_y = 0.5
    row = smallHeader.box().row()
    row.label(text="Name")
    row.label(text="Type")
    row.label(text="Creator")
    row.label(text="", icon ="BLANK1")
    smallHeader.label(text="", icon="BLANK1")

    row = layout.row()
    row.template_list("DLC_UL_List", "The_List", scene.mc_assets_manager_props, "dlc_list", scene.mc_assets_manager_props, "dlc_index")

    colMain = row.column()
    colFir = colMain.column()

    reloader = colFir.operator(
        "mcam.ui_list_reload",
        text = "",
        icon = "FILE_REFRESH"
        )
    reloader.asset_type = paths.DLCS

    colSec = colMain.column(align = True)
    colSec.operator("mcam.dlc_list_add", text = "", icon = "ADD")
    colSec.operator("mcam.dlc_list_remove", text = "", icon = "REMOVE")

    colThi = colMain.column(align = True)
    lock = "UNLOCKED" if context.scene.mc_assets_manager_props.item_unlock\
        else "LOCKED"
    colThi.prop(context.scene.mc_assets_manager_props, "item_unlock", text="", icon=lock)

def showDlcPreferences(self, context, layout):
    props = context.scene.mc_assets_manager_props
    dlc_list = context.scene.mc_assets_manager_props.dlc_list
    if dlc_list:
        #   get paths and more
        dlcs = paths.get_dlcs()

        for dlc in dlcs:
            index = props.dlc_index
            active = props.dlc_list[index].active                                           #   read active status of dlc

            if self.data and active and paths.get_dlc_init(dlc):                            #   if dlc exists & active & init file (script based)                
                if dlc == str(dlc_list[index].name):
                    try:
                        if dlc in locals():                                                         #   if already loaded
                            importlib.reload(eval(dlc))                                             #   reload module
                        else:
                            module_name = ".storage.dlcs."+dlc                                        #   get module name for importing
                            locals()[dlc] = importlib.import_module(
                                name = module_name,
                                package = paths.PACKAGE
                            ) 

                        locals()[dlc].CustomAddonPreferences.display(self, layout)                      #   draw addon preferences from dlc
                    except Exception:
                        print(traceback.format_exc())
                        print(f'McAM: could not display addon preferences panel: {dlc}')