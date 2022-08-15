const path = require("path");
const fs = require("fs");

const { getBlenderVersion } = require("../utils");


async function copyDLCs() {
    const blenderDir = path.join(process.env.APPDATA, "Blender Foundation", "Blender");
    const dlcDir = path.join(blenderDir, await getBlenderVersion(), "scripts", "addons", "MC_Assets_Manager", "files", "DLCs");
    const dlcs = fs.readdirSync(dlcDir);

    console.log(dlcs);
}

module.exports = { copyDLCs };