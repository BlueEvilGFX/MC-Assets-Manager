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
                { ConnectorType.Connect, "│  "},
                { ConnectorType.Branch, "├──"},
                { ConnectorType.Last, "└──"},
                { ConnectorType.Space, "   "}
            };
        }

        internal enum ConnectorType{
            Connect,
            Branch,
            Last,
            Space
        }

        public void PrintOneLiner(string line, int indent = 0, bool clean = false)
        {
            ConnectorType connectorType = clean ? ConnectorType.Space : ConnectorType.Connect;
            string spaces = String.Concat(Enumerable.Repeat(ConnectorDict[connectorType], indent));
            Console.Write(String.Concat(spaces, ConnectorDict[ConnectorType.Branch], dot, line));
        }

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
        }
    }
}
