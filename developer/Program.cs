using System;
using developerCS.utils;

namespace developerCS
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("    > initializing...");

            // initializes utils
            Utils utils = new();
            utils.invokeApplicationSHandler();
        }
    }
}