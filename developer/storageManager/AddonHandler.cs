using System;
using System.Data.SqlTypes;
using System.IO;
using System.Linq;
using System.Diagnostics;
using System.IO.Compression;

namespace storageManager
{
    internal class AddonHandler
    {
        public Manager Manager;
        public Printer Printer;
        public string? addonVersion;

        public AddonHandler(Manager Manager, Printer Printer)
        {
            this.Manager = Manager;
            this.Printer = Printer;

            addonVersion = GetAddonVersion();
            CopyAddon();

        }

        private string GetAddonVersion()
        {
            string initPath = Path.Combine(Manager.addonPath!, "__init__.py");
            string[] lines = File.ReadAllLines(initPath);

            int blInfoStart = 0;
            var blInfo = new Dictionary<string, string>();

            // get beginning of bl_info
            foreach (var line in lines.Select((value, index) => new {value, index }))
            {
                if (line.value.Contains("bl_info") && line.value.Contains("="))
                {
                    blInfoStart = line.index;
                    break;
                }
            }

            // trim bl lines to essential data : removing unnecessary chars
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

            // get addon version
            string strVersion = blInfo["version"];
            strVersion = strVersion.Replace("(", String.Empty).Replace(")", String.Empty);
            string version = strVersion.Replace(',', '.');
            string info = $"Addon version: {version}";
            Printer.PrintOneLiner(info, indent:1);
            return version;
        }

        private void CopyAddon()
        {
            string versionDirectory = Path.Join(Manager.storagePath, "versions", addonVersion);
            if (Directory.Exists(versionDirectory))
                Directory.Delete(versionDirectory, true);
            Directory.CreateDirectory(versionDirectory);

            string targetPath = Path.Join(versionDirectory, Manager.addonName);
            string[] blackList = { "__pycache__", "DLCs", "own_presets", "own_assets", "own_rigs", "mc_assets_manager_updater" };

            //Now Create all of the directories
            Printer.PrintOneLiner("copying directories...", indent: 2, useDot: false);
            foreach (string dirPath in Directory.GetDirectories(Manager.addonPath!, "*", SearchOption.AllDirectories))
            {
                if (blackList.Any(dirPath.Contains) == false)
                {
                    Directory.CreateDirectory(dirPath.Replace(Manager.addonPath!, targetPath));
                }
            }

            //Copy all the files & Replaces any files with the same name
            Printer.PrintOneLiner("copying files...", indent: 2, useDot: false);
            foreach (string newPath in Directory.GetFiles(Manager.addonPath!, "*.*", SearchOption.AllDirectories))
            {
                if (blackList.Any(newPath.Contains) == false)
                {
                    File.Copy(newPath, newPath.Replace(Manager.addonPath!, targetPath), true);
                }
            }

            Printer.PrintOneLiner("cleaning files...", indent: 2, useDot: false);
            string dlcJsonPath = Path.Join(targetPath, "files", "dlcs.json");
            File.WriteAllText(dlcJsonPath, "{}");

            Printer.PrintOneLiner("create archive...", indent: 2, sub: true);
            string zipSrcPath = versionDirectory;
            string zipDstPath = Path.Join(Manager.storagePath, "MC_Assets_Manager.zip");
            ZipFile.CreateFromDirectory(zipSrcPath, zipDstPath);
            File.Move(zipDstPath, Path.Join(zipSrcPath, "MC_Assets_Manager.zip"));
            Printer.Spacing();
        }
    }
}
