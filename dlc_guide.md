<div align="center">
  <div style="display: flex;">
    <li><a href=https://github.com/BlueEvilGFX/MC-Assets-Manager/blob/main/README.md>Addon Overview</a></li>
    <li><a href=https://github.com/BlueEvilGFX/MC-Assets-Manager/blob/main/README.md>Addon Overview</a></li> 
    <li><a href=https://github.com/BlueEvilGFX/MC-Assets-Manager/blob/main/README.md>Addon Overview</a></li> 
  </div>
</div>


## 🧭 Navigation
* [Addon Overview](https://github.com/BlueEvilGFX/MC-Assets-Manager/blob/main/README.md)
* [Addon Guide](https://github.com/BlueEvilGFX/MC-Assets-Manager/blob/main/addon_guide.md)
* [DLC Guide](https://github.com/BlueEvilGFX/MC-Assets-Manager/blob/main/dlc_guide.md)

## 🏷 Summary
* [File Structure](#file-structure)

## File Structure

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
│  ├── icons
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

Your DLC does not need to contain all of the things above. Though it must contain the `data.json` file, otherwise an error will raise and your DLC cannot be read in by McAM. The data.json structure looks like following:

```json
{
    "type" : "presets",
    "creator" : "Grandpa Evil",
    "version" : "[0, 1, 0]"
}
```

The icon of the DLC is also optional. If you want to use one though it must be named `icon.png`. If the DLC does not contain an icon, Blender will use another Blender internal icon.

For the rigs and presets you just put the blend files into the right directory. If you want to use icons for them you need to name them exactly like the rig/asset.
For example: `Pathfinder.blend` and `Pathfinder.png`. McAM will now display this righ with this icon.

Now to the more complex assets structure.
