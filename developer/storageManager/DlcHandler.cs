using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using Newtonsoft.Json;
using static storageManager.Printer;

namespace storageManager
{
    internal class DLC
    {
        string version;
        string creator;
        public DLC(string version, string creator)
        {
            this.version = version;
            this.creator = creator;
        }
    }

    internal class DlcHandler
    {
        public Manager Manager;
        public Printer Printer;
        public string dlcDir;
        private Dictionary<string, string> dlcData = new Dictionary<string, string> { };

        public DlcHandler(Manager Manager, Printer Printer)
        {
            this.Manager = Manager;
            this.Printer = Printer;

            dlcDir = GetDlcDir(); 
            var dlcData = new Dictionary<string, string>();
            GetDlcData();
        }

        private string GetDlcDir()
        {
            return Path.Combine(Manager.addonPath!, "files", "DLCs");
        }

        private void GetDlcData()
        {
            string[] DLCs = Directory.GetDirectories(dlcDir);
            string[] printInformation = new string[DLCs.Length];

            foreach (var dlc in DLCs.Select((name, index) => new { name, index }))
            {
                string jsonFile = Path.Combine(dlc.name, "data.json");
                var values = JsonConvert.DeserializeObject<Dictionary<string, string>>(File.ReadAllText(jsonFile));

                string dlcName = Path.GetFileName(dlc.name);
                string version = values!["version"];

                dlcData.Add(dlcName, version);
                string spaces = String.Concat(Enumerable.Repeat(' ', 20- dlcName.Length));
                printInformation[dlc.index] = ($"name: {dlcName}{spaces} version: {version}");
            }

            Printer.PrintOneLiner("found DLCs", indent: 1);
            Printer.Listing(items: printInformation, indent:1);
        }
    }
}
