const readline = require('readline');

function getCmdInput(query) {
    const lineReader = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    return new Promise(resolve => lineReader.question(query, ans => {
        lineReader.close();
        resolve(ans);
    }))
}

async function main() {
    console.clear();
    let input = await getCmdInput('\n   > Import addon version (y) or use locally stored version (n)?   y/n: ');

    switch (input) {
        case 'y':
            console.log('   > proceeding with importing...');
            await importAddon();
            break;
        case 'n':
            console.log('   > proceeding with preparing for upload...');
            await prepareAll();
            break;
        default:
            input = main();
    }

}

const archiver = require('archiver');
const path = require('path');
const fs = require('fs');

const addonName = 'MC_Assets_Manager'
const barLength = 6;
const bars = '━'.repeat(barLength);
let addonPath = null;

async function importAddon() {

}

async function getNewestLocalVersion() {
    let _path = path.join(path.dirname(__dirname), 'versions');

    // create object of all available versions
    // joins the version integers together
    // --> Versions must match x.x.x, 3 version tags each only 1 digit!
    // [{ key: '0.1.6', value: '016' }]
    const versions = fs.readdirSync(_path).map(i => {
        return {key: i, value: i.split('.').join('')}
    });

    let highest = 0;
    versions.forEach(item => {
        if (item.value > highest) highest = item.value;
    });

    addonPath = path.join(_path, highest.key, addonName);

    console.log('\n');
    console.log(bars);
    console.log(`   Newest Version: ${highest.key}`);
    console.log(`   path: ${addonPath}`);
}

function removePycache() {
    function listDirsPycache() {
        fs.readdir(addonPath, {withFileTypes: true}, (error, files) => {
            const subDirectories = files.filter(item => item.isDirectory()).map(item => item.name);

            subDirectories.forEach(name => {
                const dir = path.join(addonPath, name);
                if (name !== '__pycache__') listDirsPycache(dir)
                else fs.rmSync(dir, {recursive: true, force: true});
            })
        })
    }

    listDirsPycache(addonPath)

    console.log(bars);
    console.log('   removed pycache');
}

function removeFiles() {
    let files_dir = path.join(addonPath, 'files');
    let DLCs_dir = path.join(files_dir, 'DLCs');
    let o_assets = path.join(files_dir, 'own_assets');
    let o_presets = path.join(files_dir, 'own_presets');
    let o_rigs = path.join(files_dir, 'own_rigs');
    let addon_updater = path.join(addonPath, 'mc_assets_manager_updater');

    fs.rm(addon_updater, {recursive: true, force: true}, null);
    fs.rm(DLCs_dir, {recursive: true, force: true}, null);
    fs.rm(o_assets, {recursive: true, force: true}, null);
    fs.rm(o_presets, {recursive: true, force: true}, null);
    fs.rm(o_rigs, {recursive: true, force: true}, null);

    console.log(bars);
    console.log('   removed files');
}

function clearDlcJson() {
    let files_dir = path.join(addonPath, 'files');
    let json_path = path.join(files_dir, 'dlcs.json')
    fs.writeFile(json_path, '{}', () => {
        console.log(bars);
        console.log('   cleared dlc json');
    });
}

function zipAddons() {
    const destination = path.join(path.dirname(addonPath), `${addonName}.zip`);
    const output = fs.createWriteStream(destination);
    const archive = archiver('zip', {});

    output.on('close', () => {
        console.log(bars);
        console.log('   zipped addon');
    });

    archive.on('error', err => throw err);
    archive.pipe(output);
    // append files from a sub-directory, putting its contents at the root of archive
    archive.directory(addonPath, false);
    // append files from a sub-directory and naming it `new-subdir` within the archive
    archive.directory('subdir/', 'new-subdir');
    archive.finalize();
}

async function prepareAll() {
    async function prepAll() {
        await getNewestLocalVersion();
        removePycache();
        removeFiles();
        clearDlcJson();
    }

    await prepAll()
    zipAddons();
}

await main();