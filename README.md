# master-snippets

> By Tyler Fanuele

## What is master snippits?

This is a python program that at a basic level copys code or text to your clipboard for pasting later on. It does this\
by storing your snippits in a user accesable text file.

## How to get started

Add the directory to the path and make snip.py exicutable with chmod +x snip.py.
Then run snip.py init to create your config folder and file and run snip.py edit vim to add snips.
A snip is a refrence to a code snippit. It will be used in the options.

## Options

| cmd | result |
|-----|--------|
| snip.py [snip name] | Copys your snip to the clipboard if it exists. |
| snip.py list | Lists out the names of your snips. |
| snip.py report | Lists out the names and contents of your snips. |
| snip.py edit [ editor ] | Allows your to edit your snips file easier. Use your favorite editor. |
| snip.py help | Prints the help screne to the console. |
| snip.py init | Creates the config folder and file if they are not created. |
