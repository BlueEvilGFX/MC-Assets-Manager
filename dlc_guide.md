# 🧭 Navigation
<div align="center">
    <pre><a href="README.md">Addon Overview</a>    ●    <a href="addon_guide.md">DLC Guide</a>    ●    <a href="dlc_guide.md">DLC Guide</a></pre>
</div> 

# 🏷 Summary
* [File Structure](#file-structure)
  * [Main File Structure](#main-file-structure)
  * [Data Json File](#data-json-file)
  * [Rigs & Presets](#rigs--presets)
  * [Assets](#assets)
* [Scripts](#scripts)
  * [Scripts Introduction](#scripts-info) 

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
    "version" : "[0, 1, 0]"
}
```

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

Every asset must be listed in the `asset.json` file. The name of the `object` or `collection` will also be the name which will be displayed in McAM. It is the name of the collection if `type` is set to `Collection`. Vice versa if the `type` is set to `Object` it is the name of the object. This is followed by the property `category`. You can set the category to following values which are listed in the `assetCategories.json` of the addon:
```json
[
    "tools",
    "food",
    "weapons"
]
```

You can use icons for this as well. Just make sure to name the items exactly like the corresponding asset name.

# Scripts

## Scripts Info

A DLC can contain script elements. When you want to use this you must follow certain guidelines. Especially when you want to implement the UI to the McAM UI and if you want to use addon preferences properties. Therefore, here are important things you need to comply to. All of these classes must be in the `__init__.py` file. They can either be imported to it or be written directly in the `__init__.py` file:

```py
class PreferencesProperty(PropertyGroup):
    # here will be your code for creating addon preferences
    pass
```

```py
class CustomAddonPreferences():
    '''Creates a Panel in the User Preferences -> Addon Preferences'''

    def display(self, element=None):
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
