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
#
#   help: displays the help message
#
#   add_color: This function adds color and format formatting to a string and returns it

from audioop import add
from genericpath import exists
import re
import sys
from collections import defaultdict
import pyperclip
from pathlib import Path
import os
from os.path import exists

# color
G = 32
R = 31
B = 34
#format
BLD = 1
UND = 4
REG = 0

def add_color(wString, color, form):
    temp1 = "\033[" + str(form) + ";" + str(color) + "m" + wString + "\033[0m"
    return temp1

# help function
def help():
    print(add_color("=== snip.py help:", G, REG))
    print(add_color("=== snip.py help => outputs this help menu", G, REG))
    print(add_color("=== snip.py list => lists your code snip names", G, REG))
    print(add_color("=== snip.py report => reports all of the snip", G, REG))
    print(add_color("=== snip.py init => used at the start, initilizes snip files/dir", G, REG))
    print(add_color("=== snip.py edit [editor] => allows editing of the snippits.txt file", G, REG))
    print(add_color("=== snip.py [snip name] => if the snippit exists in your file, copy to keyboard", G, REG))
    print(add_color("=== snip.py return => Puts the previous clipboard buffer back into your clipboard", G, REG))
    print(add_color("=== snip.py peek [snip name] => Prints the contents of the snip if it exists.", G, REG))

def main():
    # print snippy
    print(add_color("===             ____\n"+
          "===            / . .\\\n"+
          "===   snippy   \  ---<\n"+
          "===             \  /\n"
          "===   __________/ /\n"
          "===-=:___________/", G, REG))
    print(add_color("=== Code Snippets program\n===> by Tyler Fanuele.", G, REG))
    print(add_color("=== Command issued by user: \n=== ", G, REG), end='')
    for x in sys.argv:
        print(add_color(x, B, REG) + " ", end='')
    print(add_color("\n===", G, REG))
    # Start of program. Defines home dir and wanted snip
    home = str(Path.home())
    if len(sys.argv) - 1  < 1:
        print("=== Not enough arguments passed")
        return

    # wanted is the command or arg given
    wanted = sys.argv[1]
    # this is the place our arg is

    if wanted == "help" or wanted == "h":
        help()
        return
    
    if wanted == "return":
        print(add_color("=== Starting return sequence...\n", G, REG))
        sp = open(home + "/.config/snippets/save.txt", "r")
        ret = ""
        for line in sp:
            ret += line
        pyperclip.copy(ret)
        sp.close()
        print(add_color("=== Your old clipboard item should be in your clipboard again", G, REG))
        print(add_color("===  Closing program!", G, REG))
        return

    # Init Sequence. Always ends program
    if wanted == "init":
        # if snippits dir exists
        print(add_color("=== Starting start up script", G, REG))
        if not exists(home + "/.config/snippets"):
            print(add_color("=== => Making dir: " + home + "/.config/snippets", G, REG))
            os.system("mkdir " + home + "/.config/snippets")
        else:
            print(add_color("=== => snippets directory exists so did nothing...", G, BLD))
        # if snippits.txt exists
        if not exists(home + "/.config/snippets/snippets.txt"):
            print(add_color("=== => Making file: " + home + "/.config/snippets/snippets.txt", G, REG))
            os.system("touch " + home + "/.config/snippets/snippets.txt")
        else:
            print(add_color("=== => snippets.txt file exists so did nothing...", G, BLD))
        if not exists(home + "/.config/snippets/save.txt"):
            print(add_color("=== => Making file: " + home + "/.config/snippets/save.txt", G, REG))
            os.system("touch " + home + "/.config/snippets/save.txt")
        else:
            print(add_color("=== => save.txt file exists so did nothing...", G, BLD))
        print("\n=== Setup script finished, closing program!")
        return
    
    # Edit sequence. Always ends program
    if wanted == "edit":
        if len(sys.argv) - 1 < 2:
            print(add_color("=== Not enough args!", R, BLD))
            return
        if not exists(home + "/.config/snippets") or not exists(home + "/.config/snippets/snippets.txt"):
            print(add_color("=== Snippit dir or snippet.txst file does not exist.\nRun snippet init", R, BLD))
            return
        print(add_color("=== Attempting to open " + sys.argv[2] + "...\n", G, BLD))
        os.system(sys.argv[2] + " " + home + "/.config/snippets/snippets.txt")
        print(add_color("=== Closing Program!", G, REG))
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
        print(add_color("=== Printing your snip list:", G, REG))
        for string in dict:
            print(add_color("=== => ", G, REG) + add_color(string, B, UND))
    # Report sequence. Will end program after if statement
    elif wanted == "report":
        print(add_color("=== Reporting your snips:\n===", G, REG))
        for string in dict:
            print(add_color("=== => ", G, REG) + add_color(string, B, UND))
            for line in dict[string]:
                print(add_color("=== => => ", G, REG) + add_color(line, B, REG), end='')
            print(add_color("===", G, REG))
    # begin peek sequence. Will end program after if statement
    elif wanted == "peek":
        if len(sys.argv) - 1 < 2:
            print(add_color("=== Not enough args!", R, BLD))
            print(add_color("=== Closing program!", G, REG))
            return
        wanted = sys.argv[2]
        for i in range(3, len(sys.argv)):
            # print(sys.argv[i])
            wanted += " " + sys.argv[i]
        print(add_color("=== Peeking contents of ", G, REG) + add_color(wanted, B, UND) + add_color("...", G, REG))
        if not wanted in dict:
            print(add_color("=== That snip does not seem to exist... ", R, BLD))
            print(add_color("=== Closing program!", G, REG))
            return
        for string in dict[wanted]:
            print(add_color("=== => ", G, REG) + add_color(string, B, REG))
    else:
        # Snippit to clipboard sequence
        for i in range(2, len(sys.argv)):
                # print(sys.argv[i])
                wanted += " " + sys.argv[i]
        if not wanted in dict:
            print(add_color("=== That snip does not seem to exist... ", R, BLD))
            print(add_color("=== Closing program!", G, REG))
            return
        print(add_color("=== Looking for snippet: ", G, REG)+ add_color(wanted, B, UND))
        for string in dict[wanted]:
            return_string += string
            sp = open(home + "/.config/snippets/save.txt", "w") # save clipboard
            save_string = pyperclip.paste()
            sp.write(save_string)
            sp.close()
            pyperclip.copy(return_string)
        print(add_color("=== Snip should be in your clipboard", G, REG))
    print(add_color("=== Closing program!", G, REG))
    #fp.close()
main()
