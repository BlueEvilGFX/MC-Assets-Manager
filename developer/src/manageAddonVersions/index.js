// ━━━━━━━━━━━━ import normal libraries
const async = require('async');
const path = require('path');
const fs = require('fs');

// ━━━━━━━━━━━━ import functions from other files
const { getCmdInput, getBlenderVersion } = require("../utils");
const { importAddon } = require("./importAddon");
const { getNewestLocalVersion } = require("./localVersionGetter");
const { removePycache, removeFiles } = require("./removers");
const { clearDlcJson } = require("./clearDLC");
const { zipAddon } = require("./zipper");

// ━━━━━━━━━━━━ variables
const addonName = 'MC_Assets_Manager';
const barLength = 6;
const bars = '━'.repeat(barLength);
let addonPath = null;

// ━━━━━━━━━━━━ main function
async function main() {
    console.clear();
    console.log(bars);
    let input = await getCmdInput('   > Import addon version (y) or use locally stored version (n)?   y/n: ');

    switch (input) {
        case 'y':
            //  ━━━━━━━━━━━━ import 
            //  first import addon from the Blender Addons directory
            //  then prepare this version for uploading to githgub;
            //  the addon versions is read from the __init__.py file
            //  line by line. The Version number is in a specific line
            //  hardcoded!
            console.log(bars);

            //  get blender dir
            const blenderDir = path.join(process.env.APPDATA, "Blender Foundation", "Blender");
            const blenderVersion = await getBlenderVersion();

            //  access init file of "original" addon
            const __init__File = path.join(blenderDir, blenderVersion, "scripts", "addons", addonName, "__init__.py");
            const allFileContents = fs.readFileSync(__init__File, 'utf-8');
            //  gets the line 12, containing the information
            //  removes spaces
            //  replaces () with {}
            //  remove ,
            //  result: { version: [i, i, i] }
            let version;
            try {
                var versionLine = `{${allFileContents
                    .split(/\r?\n/)[11]
                    .replace(/\s/g, '')
                    .replace('(', '[')
                    .replace(')', ']')
                    .slice(0, -1)}}`;
                
                const obj = JSON.parse(versionLine);
                version = Object.values(obj)[0].join('.');
            } catch (error) {
                console.log('   > could not read addon version');
                return;
            }
            //  importing
            console.log('   > proceeding with importing...');
            let srcDir = path.join(blenderDir, blenderVersion, "scripts", "addons", addonName);
            importAddon(srcDir, version);
            //  prepping
            prepareAll();
            break;
        case 'n':
            //  ━━━━━━━━━━━━ prep
            //  this only preps the latest addon version found 
            //  in the versions directory
            console.log(bars);
            console.log('   > proceeding with preparing for upload...');
            prepareAll();
            break;
        case 'r':
            return "return";
        case 'e':
            return;
        default:
            main();
    }
}

// ━━━━━━━━━━━━  function which executes all preperation
function prepareAll() {
    console.log(bars);
    async.series([
        function (callback) {addonPath = getNewestLocalVersion(callback, addonName)[0]},
        function (callback) {removePycache(callback, addonPath)},
        function (callback) {removeFiles(callback, addonPath)},
        function (callback) {clearDlcJson(callback, addonPath)},
        function (callback) {zipAddon(callback, addonPath, addonName)}
    ],
    function(error, result){});
}

module.exports = { main };