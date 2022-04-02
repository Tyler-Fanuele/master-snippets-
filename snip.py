#!/usr/bin/env python3
from genericpath import exists
import re
import sys
from collections import defaultdict
import pyperclip
from pathlib import Path
import os
from os.path import exists

def help():
    print("snip.py help:")
    print("snip.py help => outputs this help menu")
    print("snip.py list => lists your code snip names")
    print("snip.py report => reports all of the snip")
    print("snip.py init => used at the start, initilizes snip files/dir")
    print("snip.py edit [editor] => allows editing of the snippits.txt file")
    print("snip.py [snip name] => if the snippit exists in your file, copy to keyboard")

def main():
    print("Snippits program\n> by Tyler Fanuele.\n")
    #print("echo " + '"alias snip=' + "'./snippits.py'" +'"' + ">> ~/.bashrc")
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

    # Init Sequence. Always ends program
    if wanted == "init":
        # if snippits dir exists
        print("Starting start up script")
        if not exists(home + "/.config/snippits"):
            print("=> Making dir: " + home + "/.config/snippits")
            os.system("mkdir " + home + "/.config/snippits")
        else:
            print("=> snippits directory exists so did nothing...")
        # if snippits.txt exists
        if not exists(home + "/.config/snippits/snippits.txt"):
            print("=> Making file: " + home + "/.config/snippits/snippits.txt")
            os.system("touch " + home + "/.config/snippits/snippits.txt")
        else:
            print("=> snippits.txt file exists so did nothing...")
        print("\nSetup script finished, closing program!")
        return
    
    # Edit sequence. Always ends program
    if wanted == "edit":
        if len(sys.argv) - 1 < 2:
            print("Not enough args!")
            return
        if not exists(home + "/.config/snippits") or not exists(home + "/.config/snippits/snippits.txt"):
            print("Snippit dir or snippit.txst file does not exist.\nRun snippit init")
            return
        print("Attempting to open " + sys.argv[2] + "...\n")
        os.system(sys.argv[2] + " " + home + "/.config/snippits/snippits.txt")
        print("Closing Program!")
        return

    
    home += "/.config/snippits/snippits.txt"
    fp = open(home, "r")
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
    if wanted == "report":
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
        print("Looking for snippit: " + wanted)
        for string in dict[wanted]:
            return_string += string
            pyperclip.copy(return_string)
        print("Snip should be in your clipboard")
    fp.close()
main()
