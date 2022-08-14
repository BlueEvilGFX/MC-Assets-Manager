const path = require('path');
const fs = require('fs');

function getNewestLocalVersion(callback, addonName, bars) {
    const versionsPath = path.join(path.dirname(path.dirname(__dirname)), 'versions');
    const versions = fs.readdirSync(versionsPath);

    const newestVersion = versions
        .map(function(v) {
            return v.split('.').map(
                function(vs){return parseInt(vs,10)}
            )
        })
        .sort(function(a,b){
            return a[0]*100+a[1]*10+a[2] > b[0]*100+b[1]*10+b[2]
        })
        .pop()
        .join('.');

    let addonPath = null;
    if (addonName != null) {
        addonPath = path.join(versionsPath, newestVersion, addonName)
    console.log(bars);
    console.log(`   > Newest Version: ${newestVersion}`);
    console.log(`   > path: ${addonPath}`);}


    if (callback != null) {callback()};
    return [addonPath, newestVersion]
}

module.exports = { getNewestLocalVersion };