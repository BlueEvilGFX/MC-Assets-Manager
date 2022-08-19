﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace storageManager
{
    internal class Input
    {
        public static string GetInput(string[] restrictions, (int l, int t) cursorPosition)
        {
            Console.SetCursorPosition(cursorPosition.l, cursorPosition.t);
            string? input = Console.ReadLine();
            Console.SetCursorPosition(cursorPosition.l + input!.Length, cursorPosition.t);
            bool isNull = input is null;
            bool invalidInput = !(restrictions.Contains(input));
            if (isNull || invalidInput)
            {
                for (int i = 0; i < input!.Length; i++)
                    Console.Write("\b \b");
                return GetInput(restrictions, cursorPosition);
            }
            Console.SetCursorPosition(0, cursorPosition.t+restrictions.Length+1);
            return input!;
        }
    }
}
