#!/usr/bin/env python3

# Copyright 2022 Tyler Fanuele
# Program summary:
# two functions
#   main: serves as the main function, the starting point of the program.
#       Program captures the first argument. This arg is what decides the 
#       programs final function. These include:
#       help: this path will print help to the screen
#       return: this path will look into the save.txt file located in the
#           snippets folder created by init and copy its contents into the
#           clipboard. Effectively setting the clipboard buffer to its state
#           before the program ran.
#       init: This path looks to see if the required files and directories
#           exist and if they dont it creates them. This happens in the home
#           dir.
#       edit: This path allows the user to edit the snippets.txt file with ease.
#           It takes in the edit command and the users choice of text editor.
#       The file then opens the snippets.txt file and puts all the snips into a
#           dictionary. The program then goes through the listing sequence.
#       list: This path lists the names of the snips taken from the snippets.txt
#           file.
#       report: This path lists the names as well as the contents of the snips
#           taken from the snippets.txt file.
#       peek: This path takes the peek command as well as the name of a snip
#           and returns the contents of that snip.
#       The program will now, if none of the previous paths are taken, add the
#           contents of the requested snip to the clipboard for pasting and 
#           save the previous contents to the save.txt file.
#   help: displays the help message

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
    print("snip.py return => Puts the previous clipboard buffer back into your clipboard")
    print("snip.py peek [snip name] => Prints the contents of the snip if it exists.")

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
    
    if wanted == "return":
        print("Starting return sequence...\n")
        sp = open(home + "/.config/snippets/save.txt", "r")
        ret = ""
        for line in sp:
            ret += line
        pyperclip.copy(ret)
        sp.close()
        print("Your old clipboard item should be in your clipboard again")
        print("Closing program!")
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
    fp.close()

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
    # begin peek sequence. Will end program after if statement
    elif wanted == "peek":
        wanted = sys.argv[2]
        for i in range(3, len(sys.argv)):
            print(sys.argv[i])
            wanted += " " + sys.argv[i]
        print("Reporting contents of " + wanted + "...")
        if not wanted in dict:
            print("That snip does not seem to exist... ")
            print("Closing program!")
            return
        for string in dict[wanted]:
            print("=> " + string)
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
    #fp.close()
main()
