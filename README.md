# master-snippets

> By Tyler Fanuele

## What is master snippets?

This is a python program that at a basic level copies code or text to your clipboard for pasting later on. It does this\
by storing your snippets in a user accessible text file.

## How to get started

Add the directory to the path and make snip.py executable with chmod +x snip.py.
Then run snip.py init to create your config folder, snippets.txt file and save.txt file and run snip.py edit vim to add snips.
A snip is a reference to a code snippet. It will be used in the options. save.txt is used to save your last clipboard buffer.

## Options

| cmd | result |
|-----|--------|
| snip.py [snip name] | Copies your snip to the clipboard if it exists. |
| snip.py list | Lists out the names of your snips. |
| snip.py report | Lists out the names and contents of your snips. |
| snip.py edit [ editor ] | Allows your to edit your snips file easier. Use your favorite editor. |
| snip.py help | Prints the help screen to the console. |
| snip.py init | Creates the config folder and file if they are not created. |
| snip.py return | Puts the previous clipboard buffer back into your clipboard |
| snip.py peek [snip name] | Prints the contents of the snip if it exists. |
| snip.py append [ editor ] [snip name] | Allows user to edit or create a snip in a text editor |
| snip.py delete [snip name] | Allows user to delete a snip from snippets.txt file. |

## The snippets.txt file

### How To

There are two parts of a snippets.txt file; the name and contents of the snip.\

The name is defined with when a string is surrounded by brackets. The contents\
are defined by everything in between the brackets that define its name and the\
next snips brackets or the end of the file.

### Example

\
\[ssh]\
ssh  -X example ex.ex.com\
\[main]\
int main() {\
    printf();\
    \
}

### How to continued

In the above example notice how there is a blank line  in the function, this will be copied so\
be mindful of whitespaces.
