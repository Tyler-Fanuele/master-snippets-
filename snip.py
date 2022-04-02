#!/usr/bin/env python3

# Copyright 2022 Tyler Fanuele

from genericpath import exists
import re
import sys
from collections import defaultdict
import pyperclip
from pathlib import Path
import os
from os.path import exists

# help function
def help():
    print("snip.py help:")
    print("snip.py help => outputs this help menu")
    print("snip.py list => lists your code snip names")
    print("snip.py report => reports all of the snip")
    print("snip.py init => used at the start, initilizes snip files/dir")
    print("snip.py edit [editor] => allows editing of the snippits.txt file")
    print("snip.py [snip name] => if the snippit exists in your file, copy to keyboard")
    print("snip.py ret => Puts the previus clipboard buffer back into your clipboard")

def main():
    # print snippy
    print("             ____\n"+
          "            / . .\\\n"+
          "   snippy   \  ---<\n"+
          "             \  /\n"
          "   __________/ /\n"
          "-=:___________/")

    print("Code Snippets program\n> by Tyler Fanuele.\n")
    # Start of program. Defines home dir and wanted snip
    home = str(Path.home())
    if len(sys.argv) - 1  < 1:
        print("Not enough arguments passed")
        return
    # wanted is the command or arg given
    wanted = sys.argv[1]
    # this is the place our arg is

    if wanted == "help" or wanted == "h":
        help()
        return
    
    if wanted == "ret":
        sp = open(home + "/.config/snippets/save.txt", "r")
        ret = ""
        for line in sp:
            ret += line
        pyperclip.copy(ret)
        sp.close()
        return

    # Init Sequence. Always ends program
    if wanted == "init":
        # if snippits dir exists
        print("Starting start up script")
        if not exists(home + "/.config/snippets"):
            print("=> Making dir: " + home + "/.config/snippets")
            os.system("mkdir " + home + "/.config/snippets")
        else:
            print("=> snippets directory exists so did nothing...")
        # if snippits.txt exists
        if not exists(home + "/.config/snippets/snippets.txt"):
            print("=> Making file: " + home + "/.config/snippets/snippets.txt")
            os.system("touch " + home + "/.config/snippets/snippets.txt")
        else:
            print("=> snippets.txt file exists so did nothing...")
        if not exists(home + "/.config/snippets/save.txt"):
            print("=> Making file: " + home + "/.config/snippets/save.txt")
            os.system("touch " + home + "/.config/snippets/save.txt")
        else:
            print("=> save.txt file exists so did nothing...")
        print("\nSetup script finished, closing program!")
        return
    
    # Edit sequence. Always ends program
    if wanted == "edit":
        if len(sys.argv) - 1 < 2:
            print("Not enough args!")
            return
        if not exists(home + "/.config/snippets") or not exists(home + "/.config/snippets/snippets.txt"):
            print("Snippit dir or snippet.txst file does not exist.\nRun snippet init")
            return
        print("Attempting to open " + sys.argv[2] + "...\n")
        os.system(sys.argv[2] + " " + home + "/.config/snippets/snippets.txt")
        print("Closing Program!")
        return

    
    
    fp = open(home + "/.config/snippets/snippets.txt", "r")
    # init snip dict
    dict = defaultdict(list)
    # init working string for lines parsing
    current = ""
    top_pattern = r'[\[\]\n]'
    # fill dictionary with lines. [] assigns snip name
    for line in fp:
        if re.match("[\[][A-Z0-9a-z ]*[\]]", line):
            current = re.sub(top_pattern, '', line)
        else:
            dict[current].append(line)
    return_string = ""

    # looks for 'args'. 
    # list will list snip names. else do regular op
    # List sequence. Will end program after if statement
    if wanted == "list":
        print("Printing your snip list:")
        for string in dict:
            print("=> " + string)
    # Report sequence. Will end program after if statement
    elif wanted == "report":
        print("Reporting your snips:\n")
        for string in dict:
            print("=> " + string)
            for line in dict[string]:
                print("=> => " + line, end='')
            print()
    else:
        # Snippit to clipboard sequence
        for i in range(2, len(sys.argv)):
                print(sys.argv[i])
                wanted += " " + sys.argv[i]
        if not wanted in dict:
            print("That snip does not seem to exist... ")
            print("Closing program!")
            return
        print("Looking for snippet: " + wanted)
        for string in dict[wanted]:
            return_string += string
            sp = open(home + "/.config/snippets/save.txt", "w") # save clipboard
            save_string = pyperclip.paste()
            sp.write(save_string)
            sp.close()
            pyperclip.copy(return_string)
        print("Snip should be in your clipboard")
    print("Closing program!")
    fp.close()
main()
