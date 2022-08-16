using System;
using System.IO;

using developerCS.utils.addonHandling;
using developerCS.utils.dlcHandling;

namespace developerCS.utils
{
    public class Utils
    {
        public const string bars = "----";
        public const string addonName = "MC_Assets_Manager";
        public string? blenderVersion;
        public string? blenderPath;
        public string? addonPath;
        public string? storagePath;

        public Utils()
        {
            string roamingPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            blenderPath = Path.Join(roamingPath, "Blender Foundation", "Blender");

            string[] blenderVersions = Directory.GetDirectories(blenderPath).Select(i => Path.GetFileName(i)).ToArray();

            if (blenderVersions.Length == 1)
            {
                blenderVersion = blenderVersions[0];
            }
            else if (blenderVersions.Length > 1)
            {
                string? input;
                do
                {
                    Console.Clear();
                    Console.WriteLine(bars);
                    Console.WriteLine("    > please select Blender version");

                    foreach (string item in blenderVersions)
                    {
                        Console.WriteLine($"        > {item}");
                    }

                    Console.Write("    > select: ");
                    input = Console.ReadLine();
                }
                while (blenderVersions.Contains(input) == false);
                blenderVersion = input;
            }

            blenderPath = Path.Join(blenderPath, blenderVersion);
            addonPath = Path.Join(blenderPath, "scripts", "addons", addonName);

            string path = Directory.GetCurrentDirectory();
            path = Path.GetFullPath(Path.Combine(path, @"..\..\..\..\"));
            storagePath = Path.Join(path, "storage");
            if (Directory.Exists(storagePath) == false)
            {
                Console.WriteLine("    > invalid storage path");
                Console.Write("    > please choose the correct storage path: ");
                do
                {
                    string? input = Console.ReadLine();
                    storagePath = input;
                }
                while (Directory.Exists(storagePath) == false);
            }
        }

        public void invokeApplicationSHandler()
        {
            Console.Clear();
            Console.WriteLine(bars);
            Console.WriteLine("    <a> for addon handling, <d> for DLC handling");
            Console.WriteLine(bars);
            Console.Write("    > please select application: ");

            string? input = Console.ReadLine();
            switch (input)
            {
                case "a":
                    AddonHandling addonHandler = new(this);
                    break;
                case "d":
                    DLCHandling dlcHandler = new(this);
                    break;
                default:
                    invokeApplicationSHandler();
                    break;
            }

            Console.WriteLine(bars);
            Console.WriteLine("    > done");
        }
    }
}