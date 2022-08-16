using System;
using System.Data.SqlTypes;
using System.IO;
using System.Linq;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.IO.Compression;
using Newtonsoft.Json;

namespace developerCS.utils.dlcHandling
{
    internal class ImportAddon
    {
        readonly Utils utils;
        private string? dlcDir;
        private string? dlcStorage;

        public ImportAddon(Utils utils)
        {
            this.utils = utils;
            importDLCs();
        }

        private void importDLCs()
        {
            Stopwatch sw = new Stopwatch();
            sw.Start();

            Console.Clear();
            Console.WriteLine(Utils.bars);
            Console.WriteLine("    > checking for DLCs...");

            dlcStorage = Path.Join(utils.storagePath, "DLCs");
            string? addonPath = utils.addonPath;
            dlcDir = Path.Join(addonPath, "files", "DLCs");
            string[] DLCs = Directory.GetDirectories(dlcDir).Select(i => Path.GetFileName(i)).ToArray();

            if (DLCs.Length == 0)
            {
                Console.WriteLine("    > no DLCs found");
                return;
            }

            Task[] tasks = new Task[DLCs.Length];

            foreach (var dlc in DLCs.Select((value, index) => new { value, index }))
            {
                tasks[dlc.index] = Task.Run(() => {
                    importDLC(dlc.value);
                    return dlc.index;
                });
            }

            Task.WaitAll(tasks);
            sw.Stop();
            Console.WriteLine(Utils.bars);
            Console.WriteLine($"    > copied DLCs in: {sw.ElapsedMilliseconds}ms");
        }

        private void importDLC(string dlc)
        {
            Console.WriteLine($"        > proceeding with: {dlc}");
            string dlcPath = Path.Join(dlcDir, dlc);
            string dlcDataFile = Path.Join(dlcPath, "data.json");

            if (File.Exists(dlcDataFile) == false)
            {
                Console.WriteLine($"        > {dlc}: data.json file missing");
                return;
            }

            dynamic? jsonFile = JsonConvert.DeserializeObject(File.ReadAllText(dlcDataFile));
            string targetPath = Path.Join(dlcStorage, dlc);
            if (Directory.Exists(targetPath))
            {
                Directory.Delete(targetPath, true);
            }
            Directory.CreateDirectory(targetPath);

            string[] blackList = { "__pycache__" };
            //Now Create all of the directories
            foreach (string dirPath in Directory.GetDirectories(dlcPath, "*", SearchOption.AllDirectories))
            {
                if (blackList.Any(dirPath.Contains) == false)
                {
                    Directory.CreateDirectory(dirPath.Replace(dlcPath, targetPath));
                }
            }

            //Copy all the files & Replaces any files with the same name
            foreach (string newPath in Directory.GetFiles(dlcPath, "*.*", SearchOption.AllDirectories))
            {
                if (blackList.Any(newPath.Contains) == false)
                {
                    File.Copy(newPath, newPath.Replace(dlcPath, targetPath), true);
                }
            }
        }
    }
}