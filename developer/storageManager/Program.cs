using System;

namespace storageManager
{
    class Programm
    {
        public static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Printer printer = new Printer();
            Manager manager = new Manager(printer);
            Console.ReadKey();
        }
    }
}