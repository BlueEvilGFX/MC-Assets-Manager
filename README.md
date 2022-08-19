# MC Assets Manager [![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) ![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/BlueEvilGFX/MC-Assets-Manager) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![GitHub all releases](https://img.shields.io/github/downloads/BlueEvilGFX/Mc-Assets-Manager/total)

![artwork](./visuals/wallpaper.png)

## 🏷 Summary
* [Purpose](#purpose)
* [Installing](#installing)
* [Support and Help](#support-and-help)
* [Quick Manual](#quick-manual)  

## Purpose
The MC-Assets-Manager (McAM) manages Minecraft Assets, Rigs, Presets and more. The easy to use DLCs are an optimal file structure for Minecraft Assets publisher. These packs full of items can be directly installed into the addon in the addons preferences. Additionally, script based DLCs can be installed as well. The addon also handles the way of appending these items and rigs. The user can access the append operator in the shift a menu. Searching for the right rig should be no problem since the UI lists contain a search and a filter function.

## Installing
For the download click this [link](https://github.com/BlueEvilGFX/MC-Assets-Manager/releases/latest/download/Mc_Assets_Manager.zip).
The addon should remain a zip folder. Otherwise it cannot be installed correctly in blender. In Blender, go to preferences, then the addons tab, and at the top right *install*. Blender might not enable it automatically on its own. Therefore, activate it yourself if needed.
 
## Support and Help
If there are any questions about the addon and managing minecraft rigs with it, feel free to contact us on our Discord server. You can join [here](https://discord.com/invite/3mybvgB6wE).

## Quick Manual
### Adding/Removing Assets
![adding assets](./visuals/preferences_assets.png)

For adding assets you will go to the Assets tab as shown in the picture. There you will find three differnt sub-tabs, each dedicated to their own group of assets --> presets, assets and rigs.

For adding an asset to such a group, you go to the dedicated tab and click on the + next to the UI list above the - button. Then you will choose a filepath and then you confirm your addition to the "storage" of McAM. This can also be a .zip file, which contains blend files. Very important for this is that you have to make all external files internal. That means you need to pack your images etc. first. Quick tip: for this you can also select multiple blend files at once.

For removing you will have to first unlock the remove operator with the little lock beneath it. Then you select the asset you want to remove in the list and click on the - to remvove it completely. This is an operation that can not be redo! So please only remove a file if you are sure you want to remove it. Therefore I suggest to let the lock be locked all the time when you do not want to remove any file. Then you will find the "export" button. You can export your personal assets here into a zip file. Assets from DLCs wont be exported since they are not created by you or maybe are privat.

Last but not least for adding assets is the "main-add" operator. It is the button that looks like a DNA helix and a small +. With this, you can add either a preset, asset or a rig. But you have to choose to which group you want to add it. Furthermore, you are able to add an icon to it too. Just follow the instructions that are written in the add operator when you choose your file. This setting is optional!

### Adding DLCs


### Addon Updater


### Original DLC Manager


### appending


### UI
