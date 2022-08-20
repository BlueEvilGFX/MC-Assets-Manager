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
└── __init__py           // if DLC has its own script you need to initialize it here
```



