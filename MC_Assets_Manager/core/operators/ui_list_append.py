import bpy
import os

from MC_Assets_Manager.core.utils import asset_dict, paths

from bpy.types import Operator

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UI_LIST_OT_APPEND(Operator):
    """
    description:
        operator which appends an item from a list
    args:
        asset_type : enum of paths.ASSETS | paths.PRESETS
        | paths.RIGS
    """
    bl_description = "append an item"
    bl_idname = "mcam.ui_list_append"
    bl_label = "append item"
    bl_options = {'REGISTER', 'UNDO'}

    asset_type : bpy.props.StringProperty()

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
        Appender =  AssetAppender(self, context)
        Appender.main()
        return{'FINISHED'}


class AssetAppender:
    """
    description:
        operator class which performs the appending of items from the list
    """

    def __init__(self, operator_reference, context):
        self.op_ref = operator_reference
        self.context = context
    
    def main(self) -> None:
        props = "self.context.scene.mc_assets_manager_props"
        str_ui_list = "%s.%s" % (
                props,
                asset_dict.get_asset_types(
                self.op_ref.asset_type,
                asset_dict.Selection.ui_list)
        )

        raw_type = asset_dict.get_asset_types(
            self.op_ref.asset_type,
            asset_dict.Selection.raw_type
        )

        index = eval(f'{props}.{asset_dict.get_ul_class(raw_type)[1]}')
        item = eval(f'{str_ui_list}[{index}]')

        blend_file = self.get_item(item)

        if item.dlc and self.op_ref.asset_type == paths.ASSETS:
            self.append_dlc_asset(blend_file, item)
        # append normally | no appending restriction of collection
        elif not item.collection:
            self.append_normally(blend_file)
        else:
            self.append_restrictioned(blend_file, item)

        self.op_ref.report({'INFO'}, "%s successully appended" %\
            self.op_ref.asset_type)

    def get_item(self, item) -> os.path:
        """
        description:
            returns the path to the blend file
        arg:
            item: ui list object
        """

        if not item.dlc:
            asset = asset_dict.get_asset_types(
                self.op_ref.asset_type,
                asset_dict.Selection.user_type
                )
            blend_dir = paths.get_user_sub_asset_dir(asset)
            blend_file = os.path.join(blend_dir, item.name + ".blend")
        else:
            blend_dir = paths.get_dlc_sub_assets_dir(
                item.dlc,
                self.op_ref.asset_type
                )

            if self.op_ref.asset_type == paths.ASSETS:
                return os.path.join(blend_dir, "assets.blend")

            item_name = f"{item.name}&&{item.collection}"\
                if item.collection else item.name

            blend_file = os.path.join(
                blend_dir,
                item_name + ".blend")

        return blend_file

    def append_dlc_asset(self, blend_file, item) -> None:
        """
        appends the item from the dlc assets blend file based on its name
        """
        path_half = os.path.join(blend_file, item.type)
        path_full = os.path.join(path_half, item.name)

        bpy.ops.wm.append(
            filepath = path_full,
            filename = item.name,
            directory = path_half,
            link = False
        )

    def append_restrictioned(self, blend_file, item) -> None:
        """
        appends the restricted collection only
        """
        bpy.ops.wm.append(
            filepath = blend_file,
            directory = f'{blend_file}\\Collection\\',
            filename = item.collection,
            active_collection=True
        )

    def append_normally(self, blend_file) -> None:
        """
        appends the collection if a collection exists
        otherwise append the objects
        """
        with bpy.data.libraries.load(blend_file, link = False)\
            as (data_from, data_to):
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