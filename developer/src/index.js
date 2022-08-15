/*━━━━━━━━━━━━ file structure
    > developer
    > versions
        > x.x.x
            > MC_Assets_Manager
            > MC_Assets_Manager.zip
        > x.x.x
            > MC_Assets_Manager
            > MC_Assets_Manager.zip
*/

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
            let blenderDir = path.join(process.env.APPDATA, "Blender Foundation", "Blender");
            let versions = fs.readdirSync(blenderDir);

            var blenderVersion;
            //  if only one blender version: use this
            if (versions.length == 1) {
                blenderVersion = versions[0]
            //  multilple blender versions: ask user
            } else {
                console.log(versions);
                let _input = null;
                do {_input = await getCmdInput('   > Please select the correct blender version: ')}
                  while (versions.includes(_input) == false);
                blenderVersion = _input;
            }

            //  reads in the __init__ file of the addon to get the correct version
            let __init__File = path.join(blenderDir, blenderVersion, "scripts", "addons", "MC_Assets_Manager", "__init__.py");
            const allFileContents = fs.readFileSync(__init__File, 'utf-8');
            //  gets the line 12, containing the information
            //  removes spaces
            //  replaces () with {}
            //  remove ,
            //  result: { version: [i, i, i] }
            try {
                var versionLine = `{${allFileContents
                    .split(/\r?\n/)[11]
                    .replace(/\s/g, '')
                    .replace('(', '[')
                    .replace(')', ']')
                    .slice(0, -1)}}`;
                
                let obj = JSON.parse(versionLine);
                var version = Object.values(obj)[0].join('.');
            } catch (error) {
                console.log('   > could not read addon version');
                return;
            }
            
            //  importing
            console.log('   > proceeding with importing...');
            let srcDir = path.join(blenderDir, blenderVersion, "scripts", "addons", "MC_Assets_Manager");
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
        default:
            input = main();
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

main();