
import re
import time #just for the luls
import numpy as np #because matrices are nice
import html.parser as hp
from html.parser import HTMLParser

#Todos
# Kindle: nothing
# Gen text: nothing
# Dyna: make mvp for splitting list into cards. make all combos. make recursive cards, ie "what are the steps of method y"
# Fun idea : ...-Guesser. train neural net to guess where ...'s should be based on my anki cards as labeled data. Then write alg that uses that for generating new cards
#write into parser to translate my shorthands (like funk = funktion etc) to the normal words?
# tool: take som inputet action whenever it matches a string. ex delete all instances of X




#This program formats different formats of text (kindle highlights, book notes, and notes from my note taking program) and creates a file that can be imported to anki
# Input: My Clippings.txt file from kindle,
# Output: output txt files  which can be imported into anki (using the anku import function).
# The resulting anki cards will have the quote on the front, the book and author on the back and the tag "book"
# Note: anki can only have a single ASCII character as separator between fields. This will cause cards to be formatted incorrecrly if the quote/author/title contains the separatedBy character in them
# This can be seen if the numcards isn't the same as the number of cards added by the import
# If this happens you can run the program again with other ascii characters and import the file again
# Since Anki doesn't allow identical cards you can do this until you have no missing cards left, you won't get any duplicates
# Remember to import to the correct anki deck

def main():
    runMode = greeter()

    modePicker(runMode)















main()
