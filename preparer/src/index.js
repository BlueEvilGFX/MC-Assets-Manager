const readline = require('readline');
const async = require('async');

const { importAddon } = require("./importAddon");
const { getNewestLocalVersion } = require("./localVersionGetter");
const { removePycache, removeFiles } = require("./removers");
const { clearDlcJson } = require("./clearDLC");
const { zipAddon } = require("./zipper");

const addonName = 'MC_Assets_Manager'
const barLength = 6;
const bars = '━'.repeat(barLength);
let addonPath = null;

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
            importAddon();
            console.log('   > proceeding with preparing for upload...');
            prepareAll();
            break;
        case 'n':
            console.log('   > proceeding with preparing for upload...');
            prepareAll();
            break;
        default:
            input = main();
    }

}

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