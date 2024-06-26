# 🧭 Navigation
<div align="center">
    <pre><a href="README.md">Addon Overview</a>    ●    <a href="addon_guide.md">Addon Guide</a>    ●    <a href="dlc_guide.md">DLC Guide</a></pre>
</div> 

# 🏷 Summary
* [File Structure](#file-structure)
  * [Main File Structure](#main-file-structure)
  * [Data Json File](#data-json-file)
  * [Rigs & Presets](#rigs--presets)
  * [Assets](#assets)
* [Scripts](#scripts)
  * [Introduction to Scripts](#introduction-to-scripts)
  * [Multilfile Script](#multilfile-script)
  * [Defining the DLCs Addon Preferences Properties](#defining-the-dlcs-addon-preferences-properties)
  * [Displaying text/properties in the Addon Preferences Panel](#displaying-properties-in-the-addon-preferences-panel)
  * [Accessing the DLCs addon preferences](#accessing-the-dlcs-addon-preferences)
  * [Using custom icons for the DLC](#using-custom-icons-for-the-dlc)

# File Structure

## Main File Structure

```
DLC.dlc                   // every dlc must be converted into a .dlc file
└── DLC                   // your source code of the dlc --> file structure see below
```

```
DLC
├──● assets               // this contains all the assets of your DLC
│  ├──● icons             // this contains all the icons of your assets
│  │  └── icon_1.png      // example of an icon
│  ├── assets.blend       // asset blend file --> stores all assets in one file
│  └── assets.json        // asset data file --> stores all assets date
│  
├──● presets              // will be explained below...
│  ├──● icons
│  │  ├── icon_1.png
│  │  └── icon_2.png
│  ├── preset_1.blend
│  └── preset_2.blend
│  
├──● rigs               // will be explained below...
│  ├──● icons
│  │  ├── icon_1.png
│  │  └── icon_2.png
│  ├── rig_1.blend
│  └── rig_2.blend
│
├──● icons               // icons for the DLC itself
│  ├── icon_1.png
│  └── icon_2.png
│
├── data.json           // contains all DLC data including version number, creator and type of DLC 
├── __init__.py         // if DLC has its own script you need to initialize it here
└── icon.png            // the icon for the DLC
```

## Data Json File

Your DLC does not need to contain all of the things above. Though it must contain the `data.json` file, otherwise an error will raise and your DLC cannot be read in by McAM. The data.json structure looks like following:

```json
{
    "type" : "presets",
    "creator" : "Grandpa Evil",
    "version" : "[0, 1, 0]",
    "ui" : false
}
```
The `ui` determines if the UI should be shown in the `McAM n-Panel` or not.

The icon of the DLC is also optional. If you want to use one though it must be named `icon.png`. If the DLC does not contain an icon, Blender will use another Blender internal icon.

## Rigs & Presets

For the rigs and presets you just put the blend files into the right directory. If you want to use icons for them you need to name them exactly like the rig/asset.\
For example: `Pathfinder.blend` and `Pathfinder.png`. McAM will now display this rig with this icon.

Important side node: normally, McAM will append the while Blend file. But if you want only to append one collection of the blend file you can restrict the appending to one collection only. This does **only** work **for rigs**!\
For Example: `Pathfinder&&CollectionName.blend` and `Pathfinder&&CollectionName.png`. The rig will appear under the name `Pathfinder` in the rig UI list. The Addon will only append the collection `CollectionName`. The icon for this file still has to have the exact same name.

## Assets

Now to the more complex assets structure.
```json
{
    "PickAxe1" : {"type" : "Object", "category" : "tools"},
    "PickAxe2" : {"type" : "Object", "category" : "tools"},
    "Hammer" : {"type" : "Collection", "category" : "tools"}
}
```

Every asset must be listed in the `asset.json` file. The name of the `object` or `collection` will also be the name which will be displayed in McAM. It is the name of the collection if `type` is set to `Collection`. Vice versa if the `type` is set to `Object` it is the name of the object. This is followed by the property `category`. You can set the category to following values which are listed in the `assetCategories.json` of the addon (file location: `MC_Assets_Manager/resources/`:
```json
[
    "tools",
    "food",
    "weapons",
    "armor"
]
```

You can use icons for this as well. Just make sure to name the items exactly like the corresponding asset name.

# Scripts

## Introduction to Scripts

A DLC can contain script elements. When you want to use this you must follow certain guidelines. Especially when you want to implement the UI to the McAM UI and if you want to use addon preferences properties. Therefore, here are important things you need to comply to. All of these classes must be in the `__init__.py` file. They can either be imported to it or be written directly in the `__init__.py` file:

```py
class PreferencesProperty(PropertyGroup):
    # here will be your code for creating addon preferences
    pass
```

```py
class CustomAddonPreferences():
    """Creates a Panel in the User Preferences -> Addon Preferences"""

    def display(self, layout=None):
        # here will be your code for your preferences UI
        pass
```

```py
class Panel():
    """Creates a Panel for the DLC in McAMUI"""
    
    @classmethod
    def poll(self, context):
        # here will be your code for polling your UI
        pass

    def draw(self, context):
        # here will be your code for your UI
        # this calls the polling: if the polling returns false
        # the UI will not be drawn 
        if not __class__.poll(context): return

        layout = self.layout
        obj = context.object
```
You will find more information below.

## Multilfile Script

Especially when there is much code in a DLC i recommend using different files. Instead of putting everything in the `__init__.py` file you can import the needed components from other files in the same directory or in subdirectories of the DLC --> python importing modules and files knowledge is needed here

Example (reduced to script files only):
```py
DLC
├── __init__.py
├── preferenes_property.py
├── custom_addon_preferences.py
└── panel.py
```
This would be an example of using different files for the script. Please do not forget to import the needed classes from the other file to the `__init__.py` file. Here, it would be like this:
```py
from .preferences_property import PreferencesProperty
from .custom_addon_preferences import CustomAddomPreferences
from .panel import Panel
```
The names of the files can be changed. The class names must be the same though.

## Defining the DLCs Addon Preferences Properties

To define the addon preferenes properties you need to declare them in the `PreferencesProperty` class.
It could look like following:
```py
class PreferencesProperty(PropertyGroup):
    test1 : bpy.props.BoolProperty()
    test2 : bpy.props.StringProperty()
    test3 : bpy.props.IntProperty()
```

## Displaying properties in the Addon Preferences Panel

When you need to write text or display any kind of information in the DLCs addon preferences panel, you need to write that in the `CustomAddonPreferences` class.
This could look like this using the properties which we have defined in the `PreferencesProperty` class before.
```py
class CustomAddonPreferences():
    '''Creates a Panel in the User Preferences -> Addon Preferences'''

    def display(self, element=None):
        import os
        from MC_Assets_Manager.core.utils import paths
        # alternatively: use the dlc name for dlc_name
        dlc_name = os.path.basename(os.path.dirname(__file__))
        addon_preferences = paths.McAM.get_addon_properties()
        prop_access = getattr(addon_preferences, f"{dlc_name}_propGroup"
        layout = self.layout
        layout.prop(prop_access, "test1")
        layout.prop(prop_access, "test2")
        layout.prop(prop_access, "test3")
```

## Accessing the DLCs addon preferences

To access the DLCs addon preference properties (in any class or file) you have created in the `PreferencesProperty` class you will need to do it this way: (It is similar to the `CustomAddonPreferences`)
```py
from MC_Assets_Manager.core.utils import paths

dlc_name = os.path.basename(os.path.dirname(__file__))
addon_preferences = paths.McAM.get_addon_properties()
prop_access = getattr(addon_preferences, f"{dlc_name}_propGroup")
```
Example of using:
```py
from MC_Assets_Manager.core.utils import paths

dlc_name = os.path.basename(os.path.dirname(__file__))
addon_preferences = paths.McAM.get_addon_properties()
prop_access = getattr(addon_preferences, f"{dlc_name}_propGroup")

self.layout.prop(prop_access, "test1", expand=true)
value = prop_access.test1
```

## Using custom icons for the DLC

You can also use custom icons for the UI of a DLC. For this you need to put your icons in the icons folder directly in your `<DLC>` folder. The addressing name to the icon is composited by the DLC name and the icon name: `<DLC_name>:<icon_name>`. For the DLC `Thomas_Rig` and the icon `cape` it would be this: `Thomas_Rig:cape`

First import the `icons.py` file from McAM, then you can use it like following:
```py
from MC_Assets_Manager.core.utils import icons

pcoll = icons.mcam_icon[icons.PCOLL_DLC_ID]
icon_id = pcoll["Thomas_Rig:cape"].icon_id

row.label(text = "hey", icon_value = icon_id)
```

        
Except this, you can build your script like you want. This are the only restrictions / guidelines you need to follow.
