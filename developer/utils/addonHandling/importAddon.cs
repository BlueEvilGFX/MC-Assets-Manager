using System;
using System.Data.SqlTypes;
using System.IO;
using System.Linq;
using System.Diagnostics;
using System.IO.Compression;

namespace developerCS.utils.addonHandling
{
    internal class ImportAddon
    {
        readonly Utils utils;
        private string? version;
        private string? versionDirectory;
        
        public ImportAddon(Utils utils)
        {
            this.utils = utils;
            importAddon();
        }

        private void importAddon()
        {
            Stopwatch sw = new Stopwatch();
            sw.Start();
            Console.Clear();
            Console.WriteLine(Utils.bars);

            string? addonPath = utils.addonPath;
            string initPath = Path.Join(addonPath, "__init__.py");
            string[] lines = File.ReadAllLines(initPath);

            int blInfoStart = 0;
            var blInfo = new Dictionary<string, string>();

            foreach (var line in lines.Select((value, index) => new { value, index }))
            {
                if (line.value.Contains("bl_info") && line.value.Contains("="))
                {
                    blInfoStart = line.index;
                    break;
                }
            }

            for (int i = blInfoStart; i <= lines.Length - blInfoStart; i++)
            {
                string line = lines[i];
                if (line.Contains(":"))
                {
                    line = line.TrimEnd(',').Replace("\"", "").Replace(" ", String.Empty);
                    string[] pair = line.Split(":");
                    blInfo.Add(pair[0], pair[1]);
                }

                if (line.Contains("}"))
                {
                    break;
                }
            }

            string strVersion = blInfo["version"];
            strVersion = strVersion.Replace("(", String.Empty).Replace(")", String.Empty);
            version = strVersion.Replace(',', '.');
            Console.WriteLine($"    > found version: {version}");

            versionDirectory = Path.Join(utils.storagePath, "versions", version);
            Directory.Delete(versionDirectory, true);
            Directory.CreateDirectory(versionDirectory);

            string targetPath = Path.Join(versionDirectory, Utils.addonName);
            string[] blackList = { "__pycache__", "DLCs", "own_presets", "own_assets", "own_rigs" };
            //Now Create all of the directories
            Console.WriteLine("    > copying directories...");
            foreach (string dirPath in Directory.GetDirectories(addonPath, "*", SearchOption.AllDirectories))
            {
                if (blackList.Any(dirPath.Contains) == false)
                {
                    Directory.CreateDirectory(dirPath.Replace(addonPath, targetPath));
                }
            }

            Console.WriteLine("    > copying files...");
            //Copy all the files & Replaces any files with the same name
            foreach (string newPath in Directory.GetFiles(addonPath, "*.*", SearchOption.AllDirectories))
            {
                if (blackList.Any(newPath.Contains) == false)
                {
                    File.Copy(newPath, newPath.Replace(addonPath, targetPath), true);
                }
            }

            Console.WriteLine("    > cleaning files...");
            string dlcJsonPath = Path.Join(targetPath, "files", "dlcs.json");
            File.WriteAllText(dlcJsonPath, "{}");

            Console.WriteLine("    > creating archive...");
            string zipSrcPath = versionDirectory;
            string zipDstPath = Path.Join(utils.storagePath, "MC_Assets_Manager.zip");
            ZipFile.CreateFromDirectory(zipSrcPath, zipDstPath);
            File.Move(zipDstPath, Path.Join(zipSrcPath, "MC_Assets_Manager.zip"));

            sw.Stop();
            Console.WriteLine(Utils.bars);
            Console.WriteLine($"    > copied addon in: {sw.ElapsedMilliseconds}ms");
        }
    }
}