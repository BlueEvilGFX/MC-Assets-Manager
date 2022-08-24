using System;
using System.Collections.Generic;
using System.IO.Compression;
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
        private Manager Manager;
        private Printer Printer;
        private string dlcDir;
        private Dictionary<string, string> dlcData = new Dictionary<string, string> { };
        private string storageDlcDir;
        private string srcDir;
        private string githubDir;

        public DlcHandler(Manager Manager, Printer Printer)
        {
            this.Manager = Manager;
            this.Printer = Printer;

            dlcDir = GetDlcDir();
            GetDlcData();
            storageDlcDir = GetStorageDlcDir();
            srcDir = GetSrcDir();
            githubDir = GetGitHubDir();
            CopyDLCs();
        }

        /// <summary>
        /// This method returns the path to the DLCs of the addon
        /// </summary>
        private string GetDlcDir()
        {
            return Path.Combine(Manager.addonPath!, "files", "DLCs");
        }

        /// <summary>
        /// This method gets the Dlc Data -> all dlc names and versions
        /// </summary>
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

        /// <summary>
        /// This method returns the path to the dlc storage dir
        /// </summary>
        private string GetStorageDlcDir()
        {
            string path = Path.Combine(Manager.storagePath!, "DLCs");
            if (Directory.Exists(path) == false)
                Directory.CreateDirectory(path);
            return path;
        }

        /// <summary>
        /// This method returns the path to the src dir of the storage
        /// </summary>
        private string GetSrcDir()
        {
            string path = Path.Combine(storageDlcDir, "src");
            if (Directory.Exists(path) == false)
                Directory.CreateDirectory(path);
            return path;
        }

        /// <summary>
        /// This method returns the path to the github dir of the storage
        /// </summary>
        private string GetGitHubDir()
        {
            string path = Path.Combine(storageDlcDir, "github");
            if (Directory.Exists(path) == false)
                Directory.CreateDirectory(path);
            return path;
        }

        /// <summary>
        /// This method initializes the copying of all the DLCs
        /// It will start one task for each of the DLCs --> CopyDLC()
        /// </summary>
        private void CopyDLCs()
        {
            Printer.PrintOneLiner("copying DLCs...", indent:1);
            Task[] tasks = new Task[dlcData.Count];

            int i = 0;
            foreach (var dlc in dlcData)
            {
                tasks[i] = Task.Run(() => {
                    CopyDLC(dlc.Key);
                    PrepareForGithub(dlc.Key);
                    return i;
                });
                i++;               
            }

            Task.WaitAll(tasks);
            Printer.Spacing();
        }

        /// <summary>
        /// This is the main method for copying a DLC
        /// </summary>
        private void CopyDLC(string name)
        {
            // empties and creates the dir
            string targetPath = Path.Combine(srcDir, name);
            if (Directory.Exists(targetPath))
            {
                Directory.Delete(targetPath, true);
            }
            Directory.CreateDirectory(targetPath);

            // set time needed variables
            string[] blackList = { "__pycache__"};
            string sourcePath = Path.Combine(dlcDir, name);

            // copy files
            // first create the directories
            foreach (string dirPath in Directory.GetDirectories(sourcePath, "*", SearchOption.AllDirectories))
            {
                if (blackList.Any(dirPath.Contains) == false)
                {
                    Directory.CreateDirectory(dirPath.Replace(sourcePath, targetPath));
                }
            }

            // then copy the files
            foreach (string newPath in Directory.GetFiles(sourcePath, "*.*", SearchOption.AllDirectories))
            {
                if (blackList.Any(newPath.Contains) == false)
                {
                    File.Copy(newPath, newPath.Replace(sourcePath, targetPath), true);
                }
            }
        }

        /// <summary>
        /// This is the main method for preparing one DLC for the upload to github
        /// </summary>
        private void PrepareForGithub(string name)
        {
            string dstFolder = Path.Combine(githubDir, name);
            string iconPath = Path.Combine(srcDir, name, "icon.png");
            string dataJsonPath = Path.Combine(srcDir, name, "data.json");

            // empties and creates the dir
            if (Directory.Exists(dstFolder))
            {
                Directory.Delete(dstFolder, true);
            }
            Directory.CreateDirectory(dstFolder);

            // copying
            File.Copy(dataJsonPath, Path.Join(dstFolder, "data.json"));
            if (File.Exists(iconPath))
            {
                File.Copy(dataJsonPath, Path.Combine(dstFolder, "icon.png"));
            }

            // zipping
            string zipSrcPath = Path.Combine(srcDir, name);
            string zipDstPath = Path.Join(dstFolder, $"{name}.dlc");
            ZipFile.CreateFromDirectory(zipSrcPath, zipDstPath);
        }
    }
}