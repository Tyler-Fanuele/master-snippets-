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
from calendar import c
import enum
from genericpath import exists
import re
import sys
from collections import defaultdict
import pyperclip
from pathlib import Path
import os
from os.path import exists
import curses
from curses import wrapper

# color
G = 32
R = 31
B = 34
# format
BLD = 1
UND = 4
REG = 0
# home directory
home = str(Path.home())

import curses.textpad


class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, items, title):
        """ Initialize the screen window
        This Class was taken and modified from 
        https://github.com/mingrammer/python-curses-scroll-example/blob/master/tui.py
        """
        self.window = None

        self.width = 0
        self.height = 0

        self.title_offset = len(title) + 1
        self.title = title

        self.option = "get"

        self.init_curses()

        self.items = items

        self.max_lines = curses.LINES - self.title_offset
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.page = self.bottom // self.max_lines

    def init_curses(self):
        """Setup the curses"""
        self.window = curses.initscr()
        self.window.keypad(True)

        curses.noecho()
        curses.cbreak()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

        self.current = curses.color_pair(2)

        self.height, self.width = self.window.getmaxyx()

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == ord('q'):
                break
            elif ch == curses.KEY_ENTER or ch == 10 or ch == 13:
                if self.option == "get":
                    string = ""
                    for i in self.items[self.current][1]:
                        string += i
                    pyperclip.copy(string)
            elif ch == ord('g'):
                self.option = "get"


    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # top position can not be negative, so if top position is going to be negative, we should set it as 0
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        """Display the items on window"""
        self.window.erase()
        for title_index, string in enumerate(self.title):
            self.window.addstr(title_index, 0, string, curses.color_pair(1))
        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            # Highlight the current cursor line
            if idx == self.current:
                self.window.addstr(idx + self.title_offset, 0, item[0].ljust(20) + "==>", curses.color_pair(2))
                for index, line in enumerate(item[1]):
                    self.window.addstr(index + 5, 50, line, curses.color_pair(1))

            else:
                self.window.addstr(idx + self.title_offset, 0, item[0], curses.color_pair(1))
        self.window.refresh()

def snip_visual(wanted, dict):
    wrapper(visual, wanted, dict)

def visual(stdscr, wanted, dict):

    l = list(dict.items())
    screen = Screen(l, ["Master Snippets Visual"
                       ,"Name                                              Contents",""])
    screen.run()
        

def snip_init(wanted, dict):
    # if snippits dir exists
    print(add_color("=== Starting start up script", G, REG))
    if not exists(home + "/.config/snippets"):
        print(add_color("=== => Making dir: " +
              home + "/.config/snippets", G, REG))
        os.system("mkdir " + home + "/.config/snippets")
    else:
        print(add_color("=== => snippets directory exists so did nothing...", G, BLD))
    # if snippits.txt exists
    if not exists(home + "/.config/snippets/snippets.txt"):
        print(add_color("=== => Making file: " + home +
              "/.config/snippets/snippets.txt", G, REG))
        os.system("touch " + home + "/.config/snippets/snippets.txt")
    else:
        print(add_color("=== => snippets.txt file exists so did nothing...", G, BLD))
    if not exists(home + "/.config/snippets/save.txt"):
        print(add_color("=== => Making file: " + home +
              "/.config/snippets/save.txt", G, REG))
        os.system("touch " + home + "/.config/snippets/save.txt")
    else:
        print(add_color("=== => save.txt file exists so did nothing...", G, BLD))
    if not exists(home + "/.config/snippets/temp.txt"):
        print(add_color("=== => Making file: " + home +
              "/.config/snippets/temp.txt", G, REG))
        os.system("touch " + home + "/.config/snippets/temp.txt")
    else:
        print(add_color("=== => config.txt file exists so did nothing...", G, BLD))
    print(add_color("===\n=== Setup script finished.", G, REG))
    return


def add_color(wString, color, form):
    temp1 = "\033[" + str(form) + ";" + str(color) + "m" + wString + "\033[0m"
    return temp1


def snip_return(wanted, dict):
    print(add_color("=== Starting return sequence...", G, REG))
    sp = open(home + "/.config/snippets/save.txt", "r")
    ret = ""
    for line in sp:
        ret += line
    pyperclip.copy(ret)
    sp.close()
    print(add_color(
        "=== Your old clipboard item should be in your clipboard again\n===", G, REG))
    return


def snip_edit(wanted, dict):
    if len(sys.argv) - 1 < 2:
        print(add_color("=== Not enough args!", R, BLD))
        return
    if not exists(home + "/.config/snippets") or not exists(home + "/.config/snippets/snippets.txt"):
        print(add_color(
            "=== Snippit dir or snippet.txt file does not exist.\nRun snippet init", R, BLD))
        return
    print(add_color("=== Attempting to open " +
          sys.argv[2] + "...\n", G, BLD))
    os.system(sys.argv[2] + " " + home + "/.config/snippets/snippets.txt")
    return

def populate_snips():
    dict = defaultdict(list)
    fp = open(home + "/.config/snippets/snippets.txt", "r")
    # init working string for lines parsing
    current = ""
    top_pattern = r'[\[\]\n]'
    # fill dictionary with lines. [] assigns snip name
    for line in fp:
        if re.match("[\[][A-Z0-9a-z ]*[\]]", line):
            current = re.sub(top_pattern, '', line)
        else:
            dict[current].append(line)
    fp.close()
    return dict

def snip_search(wanted, dict):
    wanted = sys.argv[2]
    for x in range(3, len(sys.argv)):
        wanted += " " + sys.argv[x]
    print(add_color("=== Searching snippets.txt for " + wanted + "...", G, REG))
    search_dict = return_like_items(dict, wanted)
    for item in search_dict:
        print(add_color("=== Found snip called " + item, G, REG))

    get_string = input(add_color(
        "=== Would you like to get one of these? If so type its name, if not type \"N\": ", G, REG))
    if get_string == "N":
        print(add_color("=== Ok, Closing program...", G, REG))
        return
    if not get_string in dict:
        print(add_color("=== That snip does not seem to exist...", R, BLD))
        print(add_color("=== Closing program...", G, REG))
        return
    print(add_color("===\n=== Copying " +
          get_string + " to clipboard...", G, REG))
    ret_string = ""
    for line in dict[get_string]:
        ret_string += line
        sp = open(home + "/.config/snippets/save.txt",
                  "w")  # save clipboard
        save_string = pyperclip.paste()  # save old clipboard to string
        sp.write(save_string)  # save old clipboard string to save.txt
        sp.close()
        pyperclip.copy(ret_string)  # put snip into clipboard
    return


def snip_delete(wanted, dict):
    if len(sys.argv) - 1 < 2:
        print(add_color("=== Not enough args!", R, BLD))
        print(add_color("===\n=== Closing program!", G, REG))
        return
    wanted = sys.argv[2]
    for x in range(3, len(sys.argv)):
        wanted += " " + sys.argv[x]
    if wanted not in dict:
        print(add_color("=== Snip: " + wanted + " doesen't exists!", R, BLD))
        print(add_color("===\n=== Closing program!", G, REG))
        return
    print(add_color("===\n=== Attempting to delete " +
          wanted + " from snippets file...", G, REG))
    del dict[wanted]
    fp = open(home + "/.config/snippets/snippets.txt", "w")
    for string in dict:
        fp.write("[" + string + "]" + "\n")
        for x in dict[string]:
            fp.write(x)
    fp.close()
    print(add_color("=== Removed " + wanted +
          " from snippets.txt file\n=== Closing program...", G, REG))
    return


def snip_append(wanted, dict):
    if len(sys.argv) - 1 < 3:  # check for right number of args. Must have "append" "editor" "snip name"
        print(add_color("=== Not enough args!", R, BLD))
        print(add_color("===\n=== Closing program!", G, REG))
        return
    editor = sys.argv[2]    # get editor from args
    # check if temp.txt buffer file exists
    if not exists(home + "/.config/snippets/temp.txt"):
        print(
            add_color("=== temp.txt does not exist!\n=== Run snip.py init!", R, BLD))
        print(add_color("=== Closing program...", G, REG))
        return
    wanted = sys.argv[3]    # gets full snip name from rest of arg list
    for x in range(4, len(sys.argv)):
        wanted += " " + sys.argv[x]
    if wanted in dict:  # if snip already exists copy it into temp buffer file for append
        tempF = open(home + "/.config/snippets/temp.txt", "w")
        for string in dict[wanted]:
            tempF.write(string)
        tempF.close()
        dict[wanted] = ""
    else:   # if snip does not exist allocate space for it so it can be created
        dict[wanted].append("")
    print(add_color("=== Attempting to open " + editor + "\n===", G, REG))
    # open temp buffer in user defined editor
    os.system(editor + " " + home + "/.config/snippets/temp.txt")
    tempF = open(home + "/.config/snippets/temp.txt",
                 "r")  # read in changed snip contents
    insert = ""
    for x in tempF:
        insert += x
    tempF.close()
    dict[wanted] = insert  # add the new snip contents to the dict
    # reprint the file by copying dict in the original format
    fp = open(home + "/.config/snippets/snippets.txt", "w")
    for string in dict:
        fp.write("[" + string + "]" + "\n")
        for x in dict[string]:
            fp.write(x)
    fp.close()
    tempF = open(home + "/.config/snippets/temp.txt", "w")
    tempF.close()
    print(add_color("=== Append sequence finished", G, REG))
    return


def snip_list(wanted, dict):
    print(add_color("=== Printing your snip list:\n===", G, REG))
    print(add_color("=== |-- ", G, REG) +
          add_color("snippets.txt", B, UND))
    for string in dict:
        print(add_color("=== |    |", G, REG))
        print(add_color("=== |    |-- ", G, REG) + add_color(string, B, UND))
    print(add_color("===", G, REG))


def snip_report(wanted, dict):
    print(add_color("=== Reporting your snips:\n===", G, REG))
    print(add_color("=== |-- ", G, REG) + add_color("snippets.txt", B, UND))
    for string in dict:
        print(add_color("=== |    |", G, REG))
        print(add_color("=== |    |-- ", G, REG) + add_color(string, B, UND))
        print(add_color("=== |    |    | ", G, REG))
        for line in dict[string]:
            print(add_color("=== |    |    |-- ", G, REG) +
                  add_color(line, B, REG), end='')
    print(add_color("===", G, REG))


def snip_peek(wanted, dict):
    if len(sys.argv) - 1 < 2:
        print(add_color("=== Not enough args!", R, BLD))
        print(add_color("===\n=== Closing program!", G, REG))
        return
    wanted = sys.argv[2]
    for i in range(3, len(sys.argv)):
        # print(sys.argv[i])
        wanted += " " + sys.argv[i]
    print(add_color("=== Peeking contents of ", G, REG) +
          add_color(wanted, B, UND) + add_color("...", G, REG))
    if not wanted in dict:
        print(add_color("=== That snip does not seem to exist... ", R, BLD))
        print(add_color("===\n=== Closing program!", G, REG))
        return
    for string in dict[wanted]:
        print(add_color("=== => ", G, REG) + add_color(string, B, REG), end='')


def snip_get(wanted, dict):
    # Snippit to clipboard sequence
    return_string = ""
    wanted = sys.argv[2]
    for i in range(3, len(sys.argv)):
        print(sys.argv[i])
        wanted += " " + sys.argv[i]
    if not exists(home + "/.config/snippets/snippets.txt"):
        print(add_color("=== snippets.txt does not seem to exist... ", R, BLD))
        print(add_color("=== Run snip init !\n=== Closing program!", G, REG))
        return
    if not wanted in dict:  # check if the snip exists
        print(add_color("=== " + wanted + " snip does not seem to exist... ", R, BLD))
        print(add_color("=== Try edit or append!\n=== Closing program!", G, REG))
        return
    print(add_color("=== Looking for snippet: ",
          G, REG) + add_color(wanted, B, UND))
    for string in dict[wanted]:  # copy contents of snip to the a string
        return_string += string
        sp = open(home + "/.config/snippets/save.txt", "w")  # save clipboard
        save_string = pyperclip.paste()  # save old clipboard to string
        sp.write(save_string)  # save old clipboard string to save.txt
        sp.close()
        pyperclip.copy(return_string)  # put snip into clipboard
    print(add_color("=== Old snip should be in your save.txt file...", G, REG))
    print(add_color("=== Snip should be in your clipboard", G, REG))


def return_like_items(dict, string):
    return_dict = defaultdict(list)
    for key in dict:
        if re.match(r"[" + key + "]", string):
            return_dict[key] = dict[key]
    return return_dict

# help function
def snip_help(wanted, dict):
    print(add_color("=== snip.py help:", G, REG))
    print(add_color("=== snip.py help => outputs this help menu", G, REG))
    print(add_color("=== snip.py list => lists your code snip names", G, REG))
    print(add_color("=== snip.py report => reports all of the snip", G, REG))
    print(add_color(
        "=== snip.py init => used at the start, initializes snip files/dir", G, REG))
    print(add_color(
        "=== snip.py edit [editor] => allows editing of the snippits.txt file", G, REG))
    print(add_color(
        "=== snip.py get [snip name] => if the snippit exists in your file, copy to keyboard", G, REG))
    print(add_color(
        "=== snip.py return => Puts the previous clipboard buffer back into your clipboard", G, REG))
    print(add_color(
        "=== snip.py peek [snip name] => Prints the contents of the snip if it exists.", G, REG))
    print(add_color(
        "=== snip.py append [editor] [snip name] => Allows user to edit or create a snip in a text editor", G, REG))
    print(add_color(
        "=== snip.py delete [snip name] => Allows user to delete a snip from snippets.txt file.", G, REG))
    print(add_color("=== snip.py search [snip name] => Allows user to search alike snips", G, REG))

def is_in_file(string, file_name):
    fp = open(file_name, 'r')
    for line in fp:
        if line == string:
            fp.close()
            return True
    fp.close()
    return False


def main():
    # print snippy
    print(add_color(
          "===               ____\n" +
          "===              / . .\\\n" +
          "===    snippy    \  ---<\n" +
          "===               \  /\n"
          "===     __________/ /\n"
          "===  -=:___________/\n===", G, REG))
    print(add_color("=== Code Snippets program\n=== ", G, REG) +
          add_color("Copyright 2022, Tyler Fanuele.", G, UND))
    print(add_color("===\n=== Command issued by user: \n=== ", G, REG), end='')
    for x in sys.argv:
        print(add_color(x, B, REG) + " ", end='')
    print(add_color("\n===", G, REG))
    # Start of program. Defines home dir and wanted snip
    if len(sys.argv) - 1 < 1:
        wanted = sys.argv[0]
    else:
        # wanted is the command or arg given
        # this is the place our arg is
        wanted = sys.argv[1]
    # init snip dict
    dict = populate_snips()
    # dictonary of options
    options = {
        "init" : snip_init,
        "help" : snip_help,
        "return" : snip_return,
        "edit" : snip_edit,
        "search" : snip_search,
        "delete" : snip_delete,
        "append" : snip_append,
        "list" : snip_list,
        "peek" : snip_peek,
        "report" : snip_report,
        "get" : snip_get,
        str(sys.argv[0]) : snip_visual
    }
    # check if the option is valid
    if not wanted in options:
        print(add_color("=== Item \"" + wanted +"\" is not an option!", R, BLD))
    else:
        # run associated option command
        options[wanted](wanted, dict)

    print(add_color("=== Closing program!", G, REG))
main()
