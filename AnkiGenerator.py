#!/usr/bin/python
import re
#This is the same as kindle to anki, but it's attempting to hack a solution to the anki cards having become corrupt somehow
#Hack: since the cards seem to be corrupt causing them to work normal apart from the fact that anki doesn't recognize them as identical to themselves
#Solution:ignore the first 970 lines of the output.txt file

#TODO make an experimental version that picks out a part of the quote and puts it on the back of the card so that you actually have to think and not just read the card.

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
    #kindle_corrupt_bypass(970) #creates anki cards from kindle clippings, the 970 is the number of cards that are corrupted in my anki-kindle deck, can be omitted for others.

    #dynalist_text_gen("DynalistPaste.txt", "dyna-anki.txt", ";", "dynalist") #creates file with correctly formatted cards with tag dynalist
    speedRead_parser("SpreedTest.txt", "SpreedOut.tx", "^", "Spreed")

def kindle_corrupt_bypass(corruptedCards):
    #Normal parser but it bypassess some cards in my kindle/anki dexk that are currupted
    #The corrupted cards are part of the anki deck, but will not prevent duplicates to be added, so to bypass this we ignore the first n cards that are corrupted

    kindle_text_gen(corruptedCards, 'My Clippings.txt', 'outputcorrupt.txt' , '^', 'TestCorrupt')

def kindle_text_gen(firstCard, inputName, outputName, separatorSign, cardTag):
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    f = open(outputName, 'w')
    separatedBy = separatorSign
    tag = cardTag
    numCards = 0
    n = 0
    while n < (len(lines)-1): #skip the last line

        if lines[n].strip() == "==========": # this is the start of a kindle highlight
            back = lines[n+1].strip() #this line is the book and author
            front = lines[n+4].strip() #this line is the actual quote
            card = "%s %c %s %c %s \n" %(front, separatedBy, back, separatedBy, tag)  #format to anki #Add another %c and separatedBy if you want to tag the card. Warning: this will make anki import it even if there is an identical card without the tag
            if numCards > firstCard:
                f.write(card)
            numCards+=1
            n+= 4 #skip the lines just used

        else:
            n+=1 # move to next line if current isn't start of highlight

    f.close()
    print("%s cards where created" %(numCards - firstCard))

def dynalist_text_gen(inputName, outputName, separatedBy, tag):
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    f = open(outputName, 'w')

    numCards = 0
    n = 0
    while n < (len(lines)-1): #skip the last line
        nextCard = sign_padder(lines[n], separatedBy,2 , tag)
        f.write(nextCard)
        numCards+=1
        n+=1
    f.close()
    print("%s cards where created" %(numCards))

def speedRead_parser(inputName, outputName, separatedBy, tag):
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    f = open(outputName, 'w')
    currentBook = ""

    numCards = 0
    n = 0
    newBook = r"Book:" #finds tabs

    while n < (len(lines)-1): #skip the last line
        if(re.match(newBook, lines[n])):
            currentBook = lines[n].strip()
            print("cBook = "+ currentBook + "line: " + lines[n])
        else:
            f.write(book_source_padder(lines[n], separatedBy, currentBook, tag))
        n+=1
        numCards+=1
        #print("1    " + lines[n])
    #    currentBook = "KaosCows"


    #    n+=1
    f.close()
    print("%s cards where created" %(numCards))
    #print()


def book_source_padder(line, separatedBy, book, tag):
    return(line.strip() + separatedBy + book + separatedBy + tag + "\n")

def sign_padder(line, separatedBy, fieldNum, tag):
    #returns the line split into or padded with the separatedBy fieldNum times
    #testPat = r";"
    #testline = "det;ar ; fredag"

    pattern = r""+re.escape(separatedBy)
    separations = re.findall(pattern, line)
    #cows = re.findall(testPat, testline)
    numSeparations = len(separations)
    #if (fieldNum-numSeparations == 3):
    #    line = line + separatedBy + separatedBy + separatedBy
    #print(line.strip()+"hi")
    if (fieldNum-numSeparations == 2):
        line = line.strip() + separatedBy + separatedBy + tag + "\n"
    if (fieldNum-numSeparations == 1):
        line = line.strip() + separatedBy + tag + "\n"

    return line


main()
