// ━━━━━━━━━━━━ import normal libraries
const async = require('async');
const path = require('path');
const fs = require('fs');

// ━━━━━━━━━━━━ import functions from other files
const { getCmdInput } = require("../utils");
const { copyDLCs } = require("./copy");

// ━━━━━━━━━━━━ variables
const barLength = 6;
const bars = '━'.repeat(barLength);

// ━━━━━━━━━━━━ main function
async function main() {
    console.clear();
    console.log(bars);
    console.log('   > Proceeding with getting all DLCs');

    copyDLCs();
}

// ━━━━━━━━━━━━  function which executes all preperation
// function prepareAll() {
//     console.log(bars);
//     async.series([
//         function (callback) {addonPath = getNewestLocalVersion(callback, addonName)[0]},
//         function (callback) {removePycache(callback, addonPath)},
//         function (callback) {removeFiles(callback, addonPath)},
//         function (callback) {clearDlcJson(callback, addonPath)},
//         function (callback) {zipAddon(callback, addonPath, addonName)}
//     ],
//     function(error, result){});
// }

module.exports = { main };