from obfuscate import *
import pyperclip as pp

# Change this with whatever you want.
# Change to False to make the script ask you everytime you run it.
YOUR_STATIC_KEYWORD = "Hello World!"


# ResultModePrint: 0 -> only print password; 1 -> only send password to clipboard;
# 2 -> both print and send to the clipboard
ResultModePrint = 1

if (YOUR_STATIC_KEYWORD == False):
    YOUR_STATIC_KEYWORD = input("Please enter the keyword to get your password\n")

site = input("Enter the site!\n(Case insensitive)\n\n")

result = getPass(YOUR_STATIC_KEYWORD, site)

if (ResultModePrint in [0,2]):
    print  ( result )

if (ResultModePrint in [1,2]):
    pp.copy( result )
