const fse = require('fs-extra');
const path = require('path');

const { getNewestLocalVersion } = require("./localVersionGetter");

function importAddon() {
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
    console.log(`   > ${versionName}`);

    const srcDir = String.raw`C:\Users\Kinder\AppData\Roaming\Blender Foundation\Blender\3.0\scripts\addons\MC_Assets_Manager`;
    const destDir = path.join(String.raw`F:\[ BlueEvil ]\Blender x Photo\MC_Assets_Manager\versions`, versionName, "MC_Assets_Manager");

    console.log("   > copying...");
    fse.copySync(srcDir, destDir);
}

module.exports = { importAddon };