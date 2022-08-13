const archiver = require('archiver');
const path = require('path');
const fs = require('fs');

const addon_name = 'MC_Assets_Manager'
const print_information = true;
const bar_length = 6;
const bars = '━'.repeat(bar_length);
var addon_path = null;

async function get_newest_local_version(){
    let _path = path.join(__dirname, 'versions');
    
    // create dict of all available versions
    // joines the version integers together 
    // --> only one int per version sub int is possible!
    // [{ key: '0.1.6', value: '016' }]
    var versions = fs.readdirSync(_path).map(function(i){
        return {key:i, value: i.split('.').join("")}
    });

    var highest = 0;
    versions.forEach(function(item){
        if(highest == 0){
            if(item.value > highest){
                highest = item;}
        }else{
            if(item.value > highest.value){
                highest = item}};
    });

    addon_path = path.join(_path, highest.key, addon_name);

    if(print_information == false){return};
    console.log('\n');
    console.log(bars);
    console.log(`   Newest Version: ${highest.key}`);
    console.log(`   path: ${addon_path}`);
}

function remove_pycache(){
    function list_dirs_pycache(_path){
        fs.readdir(_path, { withFileTypes: true }, (error, files) => {
            const directoriesInDirectory = files.filter((item) => 
                item.isDirectory()).map((item) => item.name);
    
            directoriesInDirectory.forEach(function(name){
                var dir = path.join(_path, name);
                if(name != '__pycache__'){
                    list_dirs_pycache(dir)
                }
                else{
                    fs.rmSync(dir, { recursive: true, force: true });
                }
            })
        })
    }
    list_dirs_pycache(addon_path);

    if(print_information == false){return};
    console.log(bars);
    console.log('   removed pycache');
}

function remove_files(){
    let files_dir = path.join(addon_path, "files");
    let DLCs_dir = path.join(files_dir, "DLCs");
    let o_assets = path.join(files_dir, "own_assets");
    let o_presets = path.join(files_dir, "own_presets");
    let o_rigs = path.join(files_dir, "own_rigs");
	let addon_updater = path.join(addon_path, "mc_assets_manager_updater");

    if(fs.existsSync(addon_updater)){
        fs.rm(addon_updater, { recursive: true, force: true }, (error) => {});
    };

    fs.rm(DLCs_dir, { recursive: true, force: true }, (error) => {});
    fs.rm(o_assets, { recursive: true, force: true }, (error) => {});
    fs.rm(o_presets, { recursive: true, force: true }, (error) => {});
    fs.rm(o_rigs, { recursive: true, force: true }, (error) => {});

    if(print_information == false){return};
    console.log(bars);
    console.log('   removed files');
}

function clear_dlc_json(){
    let files_dir = path.join(addon_path, "files");
    let json_path = path.join(files_dir, 'dlcs.json')
    fs.writeFile(json_path, '{}', function (err) {
        if(print_information == false){return};
        console.log(bars);
        console.log('   cleared dlc json');
    });
}

function zip_addon(){
    var destintation = path.join(path.dirname(addon_path), `${addon_name}.zip`);
    var output = fs.createWriteStream(destintation);
    var archive = archiver('zip');

    output.on('close', function () {
        if(print_information == false){return};
        console.log(bars);
        console.log('   zipped addon');
    });

    archive.on('error', function(err){
        throw err;
    });

    archive.pipe(output);

    // append files from a sub-directory, putting its contents at the root of archive
    archive.directory(addon_path, false);

    // append files from a sub-directory and naming it `new-subdir` within the archive
    archive.directory('subdir/', 'new-subdir');

    archive.finalize();
}

async function prepare_all(){
    async function prep_all(){
        await get_newest_local_version();
        remove_pycache();
        remove_files();
        clear_dlc_json();
    }
    
    await prep_all()
    zip_addon();
  }

prepare_all()