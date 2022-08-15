/*━━━━━━━━━━━━ file structure
    > developer
    > versions
        > x.x.x
            > MC_Assets_Manager
            > MC_Assets_Manager.zip
        > x.x.x
            > MC_Assets_Manager
            > MC_Assets_Manager.zip
    > DLCs
*/


// ━━━━━━━━━━━━ import functions from other files
const { getCmdInput } = require("./utils");
const { main: addonMain} = require("./manageAddonVersions/index");
const { main: dlcMain} = require("./packDLC/index");

// ━━━━━━━━━━━━ variables
const barLength = 6;
const bars = '━'.repeat(barLength);

// ━━━━━━━━━━━━ main function
async function main() {
    console.clear();
    console.log("type <e> to exit the program; type <r> to get back by one");
    console.log(bars);
    let input = await getCmdInput('   > Manage addon version (y) or pack DLC (n)?   y/n: ');

    switch (input) {
        case 'y':
            //  ━━━━━━━━━━━━ manage addon version --> importing | prepping 
            console.log(bars);
            if (await addonMain()=="return") {main()}
            break;
        case 'n':
            //  ━━━━━━━━━━━━ DLC packer
            console.log(bars);
            dlcMain();
            break;
        case 'r':
            return
        case 'e':
                return;
        default:
            main();
    }
}

main();