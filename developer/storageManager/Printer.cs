using System;
using System.Linq;

namespace storageManager
{
    internal class Printer
    {
        internal Dictionary<ConnectorType, string> ConnectorDict;
        internal string dot = "●";

        public Printer()
        {
            ConnectorDict = new Dictionary<ConnectorType, string>()
            {
                { ConnectorType.Connect, "│      "},
                { ConnectorType.Branch, "├──────"},
                { ConnectorType.Last, "└──────"},
                { ConnectorType.Space, "       "}
            };
        }

        internal enum ConnectorType{
            Connect,
            Branch,
            Last,
            Space
        }

        /// <summary>
        /// This method prints a "one-liner" to the console.
        /// It adds the right indentation with or without lines as indentation.
        /// </summary>
        public void PrintOneLiner(string line, int indent = 0, bool clean = false, bool sub = false, bool spacing = false, bool useDot=true)
        {
            int _indent = indent > 0 ? indent - 1 : 0;
            ConnectorType connectorType = clean ? ConnectorType.Space : ConnectorType.Connect;
            if (sub == false)
            {
                string spaces = String.Concat(Enumerable.Repeat(ConnectorDict[connectorType], _indent));
                if (useDot==false)
                    dot = "";
                if (indent < 1)
                    Console.WriteLine(String.Concat(spaces, dot, line));
                else
                    Console.WriteLine(String.Concat(spaces, ConnectorDict[ConnectorType.Branch], dot, line));
            }
            else
            {
                string spaces = String.Concat(Enumerable.Repeat(ConnectorDict[connectorType], _indent));
                if (indent < 1)
                    Console.WriteLine(String.Concat(spaces, ConnectorDict[ConnectorType.Last], line));
                else
                    Console.WriteLine(String.Concat(spaces, ConnectorDict[ConnectorType.Last], line));
            }
            if(spacing)
                Spacing();
        }

        /// <summary>
        /// This method displays the instruction what the user should
        /// write into the console and the options which operations can be run (Listing method).
        /// It is like choosing settings. OptionDefinitions can be written instead of the items,
        /// which are the items the input will be checked against (Input.GetUserInput method).
        /// </summary>
        public string InputInit(string instruction, string[] items, string[]? optionDefinitions = null, int indent = 0, bool clean = false)
        {
            ConnectorType connectorType = clean ? ConnectorType.Space : ConnectorType.Connect;
            string spaces = String.Concat(Enumerable.Repeat(ConnectorDict[connectorType], indent));

            Console.Write(String.Concat(spaces, ConnectorDict[ConnectorType.Branch], dot, instruction));
            (int l, int t) cursorPosition = Console.GetCursorPosition();
            Console.WriteLine();

            if (optionDefinitions is null)
                Listing(items, indent + 1);
            else
                Listing(optionDefinitions, indent+1);

            return Input.GetInput(items, cursorPosition);
        }
        /// <summary>
        /// This method outputs the array of strings to the console.
        /// </summary>
        public void Listing(string[] items, int indent = 0, bool clean = false)
        {
            ConnectorType connectorType = clean ? ConnectorType.Space : ConnectorType.Connect;
            string spaces = String.Concat(Enumerable.Repeat(ConnectorDict[connectorType], indent));
            int length = items.Length;
            for (int i = 0; i < length-1; i++)
            {
                Console.WriteLine(String.Concat(spaces, ConnectorDict[ConnectorType.Branch], items[i]));
            }
            Console.WriteLine(String.Concat(spaces, ConnectorDict[ConnectorType.Last], items[length-1]));
            Spacing();
        }

        /// <summary>
        /// This method prints the end of the console / program
        /// </summary>
        public void EndLine()
        {
            Console.WriteLine(String.Concat(ConnectorDict[ConnectorType.Last], "Done!"));
        }

        public void Spacing(int indent=0)
        {
            indent += 1;
            // one line spacing
            string sp = String.Concat(Enumerable.Repeat(ConnectorDict[ConnectorType.Connect], indent));
            Console.WriteLine(sp);
        }
    }
}
