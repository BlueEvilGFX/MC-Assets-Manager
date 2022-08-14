const fse = require('fs-extra');
const path = require('path');

const { getNewestLocalVersion } = require("./localVersionGetter");

function importAddon(srcDir) {
    let version = getNewestLocalVersion(null, null, null)[1];
    let versionArray = version.split('.');

    const lastDigit = versionArray[2];

    if (lastDigit != 9) {
        versionArray[2]  = parseInt(lastDigit)+1;
    } else {
        const middleDigit = versionArray[1];
        versionArray[2]  = 0;
        if (middleDigit != 9) {
            versionArray[1]  = parseInt(middleDigit)+1;
        } else {
            const firstDigit = versionArray[0];
            versionArray[1] = 0;
            versionArray[0] = parseInt(firstDigit)+1
        }
    }

    const versionName = versionArray.join('.');
    console.log(`   > new version: ${versionName}`);

    const destDir = path.join(path.dirname(path.dirname(__dirname)), "versions", versionName, "MC_Assets_Manager");

    console.log("   > copying...");
    fse.copySync(srcDir, destDir);
}

module.exports = { importAddon };