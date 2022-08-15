const readline = require('readline');
const path = require('path');
const fs = require('fs');

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

async function getBlenderVersion(){
    const blenderDir = path.join(process.env.APPDATA, "Blender Foundation", "Blender");
    const versions = fs.readdirSync(blenderDir);

    //  if only one blender version: use this
    if (versions.length == 1) {
        return versions[0]
    //  multilple blender versions: ask user
    } else {
        console.log(versions);
        let _input = null;
        do {_input = await getCmdInput('   > Please select the correct blender version: ')}
        while (versions.includes(_input) == false);
        return _input;
    }
}

module.exports = { getCmdInput, getBlenderVersion };