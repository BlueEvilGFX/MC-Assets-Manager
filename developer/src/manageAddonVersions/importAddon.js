const fs = require('fs');
const fse = require('fs-extra');
const path = require('path');

function importAddon(srcDir, versionName) {
    console.log(`   > detected version: ${versionName}`);

    const versionDir = path.join(path.dirname(path.dirname(path.dirname(__dirname))), "versions", versionName);
    const destDir = path.join(versionDir, "MC_Assets_Manager");

    console.log("   > copying...");
    fs.rmSync(versionDir, {recursive: true, force: true});
    fse.copySync(srcDir, destDir);
}

module.exports = { importAddon };