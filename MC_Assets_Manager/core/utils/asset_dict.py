from enum import Enum, auto

from .paths import (ASSETS, PRESETS, RIGS, UI_LIST_ASSETS, UI_LIST_PRESETS,
                    UI_LIST_RIGS, USER_ASSETS, USER_PRESETS, USER_RIGS)


class Selection(Enum):
    raw_type = auto()
    user_type = auto()
    ui_list = auto()


class AssetData:
    """
    contains the dictionaries for the assignment\n
    argument must be from the Selection Enum
    """

    raw_types = [ASSETS, PRESETS, RIGS]
    user_types = [USER_ASSETS, USER_PRESETS, USER_RIGS]
    ui_lists = [UI_LIST_ASSETS, UI_LIST_PRESETS, UI_LIST_RIGS]

    input = {
        Selection.raw_type : raw_types,
        Selection.user_type : user_types,
        Selection.ui_list : ui_lists
    }

    asset_determine = {
        ASSETS : 0,
        PRESETS : 1,
        RIGS : 2,
        USER_ASSETS : 0,
        USER_PRESETS : 1,
        USER_RIGS : 2,
        UI_LIST_ASSETS : 0,
        UI_LIST_PRESETS : 1,
        UI_LIST_RIGS : 2
    }


def get_asset_types(asset_type:str, output_type:Selection) -> str:
    """
    args:
        asset_type: enum of: any assset type from .paths : also ui lists
        output_type: enum of Selection 
    """
    if not output_type in Selection:
        return


    if asset_type in AssetData.raw_types:
        # index determines the type of asset: asset | preset | rig 
        index = AssetData.asset_determine[asset_type]
        # ui_list | user_type
        return AssetData.input[output_type][index]

    if (
        asset_type in AssetData.user_types
        or asset_type in AssetData.ui_lists
        ):
        # index determines the type of asset: asset | preset | rig 
        index = AssetData.asset_determine[asset_type]
        # ui_list | user_type
        return AssetData.input[output_type][index]
    return