using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace storageManager
{
    internal class Manager
    {
        public Printer printer;
        public string? localDir;
        public string? storagePath;
        public string? blenderVersion;
        public string? application;

        public Manager(Printer printer)
        {
            this.printer = printer;

            localDir = GetLocalDir();
            storagePath = GetStoragePath();
            blenderVersion = GetBlenderVersion();
            application = GetApplication();

            switch (application)
            {
                case "a":
                    break;
                case "i":
                    break;
                default:
                    Console.WriteLine("ERROR, application initialiation error [0])");
                    break;
            }
        }

        /// <summary>returns current directory | check needed for vs run</summary>
        private string GetLocalDir()
        {
            string? localDir = Directory.GetCurrentDirectory();
            string? possibleBinDir = Path.GetDirectoryName(Path.GetDirectoryName(localDir));
            if (Path.GetFileName(possibleBinDir) == "bin")
                localDir = Path.GetDirectoryName(possibleBinDir);
            return localDir!;
        }

        /// <summary>return the Storage Path</summary>
        private string GetStoragePath()
        {
            string _storagePath = Path.Combine(Path.GetDirectoryName(localDir)!, "storage");
            printer.PrintOneLiner("storage path:", 1);
            printer.PrintOneLiner(_storagePath, 2, sub:true);
            return _storagePath;
        }

        /// <summary>This method returns the installed Blender version.
        /// If more than one are installed, it will ask the user which one to use.
        /// </summary>s
        private string GetBlenderVersion()
        {
            string roamingPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            string blenderVersionsPath = Path.Join(roamingPath, "Blender Foundation", "Blender");
            string[] blenderVersions = Directory.GetDirectories(blenderVersionsPath).Select(i => Path.GetFileName(i)).ToArray();

            if (blenderVersions.Length == 1)
            {
                printer.PrintOneLiner($"Blender version: {blenderVersions[0]}", 1);
                return blenderVersions[0];
            }

            string instruction = "Blender version: ";
            return printer.InputInit(instruction, blenderVersions);
        }

        /// <summary>This method returns the application after asking the user
        /// which program to run
        /// </summary>
        private string GetApplication()
        {
            string[] options = { "a", "d"};
            string[] optionDefinitions = { "<a> import addon", "<d> import dlcs"};

            string instruction = "application: ";
            return printer.InputInit(instruction, options, optionDefinitions);
        }
    }
}