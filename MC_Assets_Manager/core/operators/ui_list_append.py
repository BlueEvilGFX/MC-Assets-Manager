import bpy
import os

from MC_Assets_Manager.core.utils import asset_dict, paths

from bpy.types import Operator


class UI_LIST_OT_APPEND_BASE(Operator):
    bl_description = "append an item"
    bl_label = "append item"
    bl_options = {'REGISTER', 'UNDO'}

    asset_type = None

    @classmethod
    def poll(cls, context):
        props = bpy.context.scene.mc_assets_manager_props
        ui_list = getattr(
            props, 
            asset_dict.get_asset_types(
                cls.asset_type,
                asset_dict.Selection.ui_list
            )
        )
        return any(ui_list)

    def invoke(self, context, event):
        bpy.ops.mcam.ui_list_reload(asset_type=self.asset_type)
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()

        ul_class, index = asset_dict.get_ul_class(self.asset_type)
        ui_list = asset_dict.get_asset_types(
            self.asset_type,
            asset_dict.Selection.ui_list
            )

        row.template_list(
            ul_class,
            "The_List",
            scene.mc_assets_manager_props,
            ui_list,
            scene.mc_assets_manager_props,
            index
            )
        
    def execute(self, context):
        Appender =  AssetAppender(self, context, self.asset_type)
        Appender.main()
        return{'FINISHED'}
    
class UI_LIST_OT_APPEND_ASSET(UI_LIST_OT_APPEND_BASE):
    bl_idname = "mcam.ui_list_append_asset"
    asset_type = paths.AssetTypes.ASSETS


class UI_LIST_OT_APPEND_PRESET(UI_LIST_OT_APPEND_BASE):
    bl_idname = "mcam.ui_list_append_preset"
    asset_type = paths.AssetTypes.PRESETS
    

class UI_LIST_OT_APPEND_RIG(UI_LIST_OT_APPEND_BASE):
    bl_idname = "mcam.ui_list_append_rig"
    asset_type = paths.AssetTypes.RIGS


class AssetAppender:
    """Operator class which performs the appending of items from the list."""

    def __init__(self, operator_reference, context, asset_type):
        self.op_ref = operator_reference
        self.context = context
        self.asset_type = asset_type

    def main(self):
        """Main function to append the asset."""
        raw_type = asset_dict.get_asset_types(self.asset_type, asset_dict.Selection.raw_type)
        props = self.context.scene.mc_assets_manager_props
        index = getattr(props, asset_dict.get_ul_class(raw_type)[1])
        ui_list = getattr(props, asset_dict.get_asset_types(self.asset_type, asset_dict.Selection.ui_list))
        item = ui_list[index]
        blend_file = self.get_item(item)

        if item.dlc and self.asset_type == paths.AssetTypes.ASSETS:
            self.append_dlc_asset(blend_file, item)
        elif not item.collection:
            self.append_normally(blend_file)
        else:
            self.append_restrictioned(blend_file, item)

        self.op_ref.report({'INFO'}, f"{self.asset_type} successfully appended")

    def get_item(self, item):
        """Returns the path to the blend file."""
        # Get the asset type
        asset = asset_dict.get_asset_types(self.asset_type, asset_dict.Selection.user_type)

        # Determine the directory based on whether the item is a DLC
        if item.dlc:
            blend_dir = paths.DLC.get_sub_asset_directory(item.dlc, self.asset_type)
        else:
            blend_dir = paths.User.get_sub_asset_directory(asset)

        # Determine the file name based on the asset type and whether the item has a collection
        if self.asset_type == paths.AssetTypes.ASSETS:
            file_name = "assets.blend"
        elif item.collection:
            file_name = f"{item.name}&&{item.collection}.blend"
        else:
            file_name = f"{item.name}.blend"

        # Return the full path to the blend file
        return os.path.join(blend_dir, file_name)

    def append_dlc_asset(self, blend_file, item):
        """Appends the item from the dlc assets blend file based on its name."""
        path_half = os.path.join(blend_file, item.type)
        bpy.ops.wm.append(
            filepath=os.path.join(path_half, item.name),
            filename=item.name,
            directory=path_half,
            link=False
            )

    def append_restrictioned(self, blend_file, item):
        """Appends the restricted collection only."""
        bpy.ops.wm.append(
            filepath=blend_file,
            directory=f'{blend_file}\\Collection\\',
            filename=item.collection,
            active_collection=True
        )

    def append_normally(self, blend_file):
        """Appends the collection if a collection exists, otherwise append the objects."""
        with bpy.data.libraries.load(blend_file, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
            data_to.collections = data_from.collections

        if data_to.collections:
            main_collection = None
            sub_collections = []

            for coll in data_to.collections:
                if main_collection is None:
                    main_collection = coll
                else:
                    sub_collections.append(coll)
                bpy.context.scene.collection.children.link(coll)

            collection = bpy.context.view_layer.layer_collection.collection
            if collection:
                for coll in sub_collections:
                    collection.children.unlink(coll)
        else:
            for obj in data_to.objects:
                if obj is not None:
                    bpy.context.scene.collection.objects.link(obj)
