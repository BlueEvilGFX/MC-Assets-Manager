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
        public string? blenderVersion;
        public string? application;

        public Manager(Printer printer)
        {
            this.printer = printer;
            blenderVersion = GetBlenderVersion();
            application = GetApplication();
        }

        /// <summary>This method returns the installed Blender version.
        /// If more than one are installed, it will ask the user which one to use.
        /// </summary>
        private string GetBlenderVersion()
        {
            string roamingPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            string blenderVersionsPath = Path.Join(roamingPath, "Blender Foundation", "Blender");
            string[] blenderVersions = Directory.GetDirectories(blenderVersionsPath).Select(i => Path.GetFileName(i)).ToArray();

            if (blenderVersions.Length == 1)
            {
                printer.PrintOneLiner($"Blender version: {blenderVersions[0]}");
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