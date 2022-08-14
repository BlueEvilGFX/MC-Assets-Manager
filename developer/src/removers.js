const path = require('path');
const fs = require('fs');

function removePycache(callback, addonPath, bars) {
    function deleteDirsPycache(_path) {
        fs.readdir(_path, {withFileTypes: true}, (error, files) => {
            if (files == undefined) {return};

            const subDirectories = files.filter(item => item.isDirectory()).map(item => item.name);

            subDirectories.forEach(name => {
                const dir = path.join(_path, name);
                if (name !== '__pycache__') {deleteDirsPycache(dir)}
                else {if (fs.existsSync(dir)) {fs.rmSync(dir, {recursive: true, force: true})}}
            })
        })
    }

    deleteDirsPycache(addonPath);

    console.log(bars);
    console.log('   > removed pycache');
    callback();
}

function removeFiles(callback, addonPath, bars) {
    let files_dir = path.join(addonPath, 'files');
    let DLCs_dir = path.join(files_dir, 'DLCs');
    let o_assets = path.join(files_dir, 'own_assets');
    let o_presets = path.join(files_dir, 'own_presets');
    let o_rigs = path.join(files_dir, 'own_rigs');
    let addon_updater = path.join(addonPath, 'mc_assets_manager_updater');

    fs.rmSync(addon_updater, {recursive: true, force: true});
    fs.rmSync(DLCs_dir, {recursive: true, force: true});
    fs.rmSync(o_assets, {recursive: true, force: true});
    fs.rmSync(o_presets, {recursive: true, force: true});
    fs.rmSync(o_rigs, {recursive: true, force: true});

    console.log(bars);
    console.log('   > removed files');
    callback();
}

module.exports = { removePycache ,removeFiles };