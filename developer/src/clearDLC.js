const path = require('path');
const fs = require('fs');

function clearDlcJson(callback, addonPath, bars) {
    let files_dir = path.join(addonPath, 'files');
    let json_path = path.join(files_dir, 'dlcs.json')
    fs.writeFileSync(json_path, '{}', {encoding: "utf8"});
    console.log(bars);
    console.log('   > cleared dlc json');
    callback();
}

module.exports = { clearDlcJson };