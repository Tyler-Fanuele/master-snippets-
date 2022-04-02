#!/usr/bin/env python3
from genericpath import exists
import re
import sys
from collections import defaultdict
import pyperclip
from pathlib import Path
import os
from os.path import exists

def main():
    print("Snippits program\nby Tyler Fanuele.\n")
    # Start of program. Defines home dir and wanted snip
    home = str(Path.home())
    wanted = sys.argv[1]

    if wanted == "init":
        # if exists(home + "/.config/snippits/snippits.txt") or exists(home + "/.config/snippits"):
        print("Starting start up script")
        if not exists(home + "/.config/snippits"):
            print("=> Making dir: " + home + "/.config/snippits")
            os.system("mkdir " + home + "/.config/snippits")
        else:
            print("=> snippits directory exists so did nothing...")

        if not exists(home + "/.config/snippits/snippits.txt"):
            print("=> Making file: " + home + "/.config/snippits/snippits.txt")
            os.system("touch " + home + "/.config/snippits/snippits.txt")
        else:
            print("=> snippits.txt file exists so did nothing...")
        print("\nSetup script finished, closing program!")
        return
    if wanted == "edit":
        
    home += "/.config/snippits/snippits.txt"
    fp = open(home, "r")
    # init snip dict
    dict = defaultdict(list)
    # init working string for lines parsing
    current = ""
    top_pattern = r'[\[\]\n]'
    # fill dictionary with lines. [] assigns snip name
    for line in fp:
        if re.match("[\[][A-Z0-9a-z]*[\]]", line):
            current = re.sub(top_pattern, '', line)
        else:
            dict[current].append(line)
    return_string = ""
    # looks for 'args'. 
    # list will list snip names. else do regular op
    if wanted == "list":
        print("Printing your snip list:")
        for string in dict:
            print("=> " + string)
    else:
        if not dict.has_key(wanted):
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
