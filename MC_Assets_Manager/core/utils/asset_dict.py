from enum import Enum

from .paths import (ASSETS, PRESETS, RIGS, UI_LIST_ASSETS, UI_LIST_PRESETS,
                    UI_LIST_RIGS, USER_ASSETS, USER_PRESETS, USER_RIGS)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Selection(Enum):
    raw_type = [ASSETS, PRESETS, RIGS]
    user_type = [USER_ASSETS, USER_PRESETS, USER_RIGS]
    ui_list = [UI_LIST_ASSETS, UI_LIST_PRESETS, UI_LIST_RIGS]

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

    if (
        asset_type in Selection.raw_type.value
        or asset_type in Selection.user_type.value
        or asset_type in Selection.ui_list.value
        ):
        # index determines the type of asset: asset | preset | rig 
        index = asset_determine[asset_type]
        # ui_list | user_type
        return output_type.value[index]
    return

def get_ul_class(asset_type:str) -> tuple[str]:
    """
    args:
        enum of: paths.ASSETS | paths.PRESETS | paths.RIGS
    description:
        returns the class name of the ui list [0] and the index [1]
    """
    # from 'ASSETS' to 'ASSET' --> removing the s (last letter)
    ul_class = asset_type.upper()[:-1] + "_UL_List"
    index = asset_type[:-1] + "_index"
    return ul_class, index