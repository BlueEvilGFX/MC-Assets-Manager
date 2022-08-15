const archiver = require('archiver');
const path = require('path');
const fs = require('fs');

async function zipAddon(callback, addonPath, addonName) {
    dirPath = path.dirname(addonPath);
    fs.rmSync(path.join(dirPath, 'MC_Assets_Manager.zip'), {recursive: true, force: true});
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    await sleep(1);
    
    const dirUpPath = path.dirname(dirPath);
    const destination = path.join(dirUpPath, `${addonName}.zip`);
    const output = fs.createWriteStream(destination);
    const archive = archiver('zip', {});

    output.on('close', () => {console.log('   > zipped addon')});

    archive.on('error', (err) => {console.log(error);throw err;});

    archive.on('warning', function(err) {
        if (err.code === 'ENOENT') {
          console.log(err);
          // log warning
        } else {
          // throw error
          throw err;
        }
      });

    archive.pipe(output);
    // append files from a sub-directory, putting its contents at the root of archive
    archive.directory(dirPath, false);
    // append files from a sub-directory and naming it `new-subdir` within the archive
    archive.directory('subdir/', 'new-subdir');
    archive.finalize();
    // moving zip 
    await sleep(1);
    fs.renameSync(destination, path.join(dirPath, `${addonName}.zip`));
    callback();
}

module.exports = { zipAddon };