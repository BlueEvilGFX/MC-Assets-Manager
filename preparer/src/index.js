// ━━━━━━━━━━━━ import normal libraries
const readline = require('readline');
const async = require('async');
const path = require('path');
const fs = require('fs');

// ━━━━━━━━━━━━ import functions from other files
const { importAddon } = require("./importAddon");
const { getNewestLocalVersion } = require("./localVersionGetter");
const { removePycache, removeFiles } = require("./removers");
const { clearDlcJson } = require("./clearDLC");
const { zipAddon } = require("./zipper");

// ━━━━━━━━━━━━ variables
const addonName = 'MC_Assets_Manager'
const barLength = 6;
const bars = '━'.repeat(barLength);
let addonPath = null;

// ━━━━━━━━━━━━
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

// ━━━━━━━━━━━━ main function
async function main() {
    console.clear();
    let input = await getCmdInput('\n   > Import addon version (y) or use locally stored version (n)?   y/n: ');

    switch (input) {
        case 'y':
            // ━━━━━━━━━━━━ get source directory
            let blenderDir = path.join(process.env.APPDATA, "Blender Foundation", "Blender");
            let versions = fs.readdirSync(blenderDir);

            var blenderVersion;
            // if only one blender version: use this
            if (versions.length == 1) {
                blenderVersion = versions[0]
            // multilple blender versions: ask user
            } else {
                console.log(versions);
                let _input = null;
                do {_input = await getCmdInput('   > Please select the correct blender version: ')}
                  while (versions.includes(_input) == false);
                blenderVersion = _input;
            }

            // importing
            console.log('   > proceeding with importing...');
            let srcDir = path.join(blenderDir, blenderVersion, "scripts", "addons", "MC_Assets_Manager");
            importAddon(srcDir);
            // prepping
            console.log('   > proceeding with preparing for upload...');
            prepareAll();
            break;
            // ━━━━━━━━━━━━ only prepping
        case 'n':
            console.log('   > proceeding with preparing for upload...');
            prepareAll();
            break;
        default:
            input = main();
    }

}

// ━━━━━━━━━━━━ function which executes all preperation
function prepareAll() {
    async.series([
        function (callback) {addonPath = getNewestLocalVersion(callback, addonName, bars)[0]},
        function (callback) {removePycache(callback, addonPath, bars)},
        function (callback) {removeFiles(callback, addonPath, bars)},
        function (callback) {clearDlcJson(callback, addonPath, bars)},
        function (callback) {zipAddon(callback, addonPath, addonName, bars)}
    ],
    function(error, result){});
}

main();