import re
import time  # just for the luls


# import html.parser as hp
#from html.parser import HTMLParser

import numpy as np  # because matrices are nice

# Todos
# Kindle: nothing
# Gen text: nothing
# Dyna: make mvp for splitting list into cards. make all combos. make recursive cards, ie "what are the steps of method y"
# Fun idea : ...-Guesser. train neural net to guess where ...'s should be based on my anki cards as labeled data. Then write alg that uses that for generating new cards
# write into parser to translate my shorthands (like funk = funktion etc) to the normal words?
# tool: take som inputet action whenever it matches a string. ex delete all instances of X


# This program formats different formats of text (kindle highlights, book notes, and notes from my note taking program) and creates a file that can be imported to anki
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


def greeter():
    runMode = 0
    possibleModes = 5
    while runMode > possibleModes or runMode < 1:
        runMode = int(
            input(
                "Welcome to the Fantastic Anki Generator."
                "What function do you want to use? \n "
                "1: Generate Kindle Anki cards \n "
                "2: Run general generator in quick mode \n "
                "3: Run general generator in step by step mode \n "
                "4 : take over the world \n "
                "5 : run testing mode \n "
                "Your desired mode:"
            )
        )
    # 4: generate anki deck with custom target input and output (not implemented yet) "")
    return runMode  # greets used and prompts them to pick run mode


def modePicker(runMode):
    if runMode == 1:
        kindle_corrupt_bypass(
            970
        )  # creates anki cards from kindle clippings, the 970 is the number of cards that are corrupted in my anki-kindle deck, can be omitted for others.
    elif runMode == 2:
        generalTextParser("input.txt", "output.txt", "^", "AnkiGenerator")
    elif runMode == 3:
        defaultIn = "input.txt"
        defaultOut = "output.txt"
        defaultTag = "AnkiGenerator"
        defaultSeparator = "^"
        inputFile = input(
            "What file do you want to take from? \n if you want the default of 'input.txt', just press enter"
        )
        outputFile = input(
            "What file do you want the cards to be written to? \n if you want the default of "
            + defaultOut
            + ", press enter"
        )
        separator = input(
            "What separator sign do you want? \n space to keep "
            + defaultSeparator
            + " as default"
        )
        tag = input(
            "What tag do you want? \n space to keep " + defaultTag + "as default tag"
        )
        if inputFile == "":
            inputFile = defaultIn
        if outputFile == "":
            outputFile = defaultOut
        if separator == "":
            separator = defaultSeparator

        if tag == "":
            tag = defaultTag

        # print("debugg, in: " + inputFile + "out: "+ outputFile)
        generalTextParser(inputFile, outputFile, separator, tag)

    elif runMode == 4:
        print("Hacking in to all main frames")
        time.sleep(3)
        print("You've now hacked all computers, you are the hackerman")
        main()

    elif runMode == 5:
        print("running test mode")
        testMode()
    else:
        print("invalid input")
        main()  # calls differnt functions based on result from greeter


def testMode():
    # hackytest
    # if(charNeedEscape('d')):
    #    print("why?")
    #    return False
    # print("inTest")
    # refString = "distribution arises naturally in Bayesian"
    # testString = "observedfeaturevector is X =(X1. . .XL, XL +1. . . X2L)"
    # regex = hackyRegExGen(testString)
    # fileSearch(testString, 'referenceFiles.txt') #mode for testing specific fuctions faster

    # regTest
    line = "you have 2 cycles that control your sleep, so you need to keep them synchronisted to avoid being fatigued, how do you do that?; Go to sleep at a very regular rate and don't vary it at all if possible. Track your sleep with pulse trackers"
    tag = "30secSummaries"
    cardBack = "30sec: Biohacker/super-selfmedicator summary"
    separatedBy = ";"
    # card = book_source_padder(line, separatedBy, cardBack, tag)
    res = separatorPadding(line, separatedBy, 2, tag, cardBack)
    # regList , muu = regexTags()
    # print(regList)
    # print(len(regList))
    # print(re.match(regList[0], refString))

    # dynatest
    # testHead = "Gnome Plan"
    # testList = ["Steal Socs", "???", "Profit"]
    # testOut = 'dynaAutoOut.txt'
    # #res = dynaCardWriter(testHead, testList, 1, testOut)
    # #res = numStepStr(testList)
    # res = findList('test.html', False)
    # print(res)


def generalTextParser(inputName, outputName, separatedBy, tag):
    # Bugs : (minor) tries to create cards from empty lines
    tag = tag
    # File init

    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    f = open(outputName, "w")
    noteMistOut = open("NotesAndMistakesOut.txt", "w")
    backToDyna = open(
        "BackToDynalist.txt", "w"
    )  # text file of things that shouldn't be ankified
    trash = open("Trash.txt", "w")
    catchAnki = open("catchallAnki.txt", "w")
    DailyEvalFile = open("DailyEval.txt", "w")

    cardBack = ""

    dailyEval = (
        r"(daily)+\s*(eval)+(uation)*"
    )  # regex noticing when I start a daily evaluation

    numCards = 0
    n = 0
    ##regex list
    regexArray, tagCounter = regexTags()
    print("tash")
    ##textParser
    while n < (len(lines) - 1):  # skip the last line
        line = lines[n]
        # print("current tag = "+ tag )
        if (
            len(line) == 0
        ):  # This doesnt actually fix the empty line bug. todo think of other fixes
            trash.write(line)
        elif re.match(regexArray[0], line, re.IGNORECASE):
            tag = "DailyEval"
            # print("I like to moce it")
            DailyEvalFile.write(line)
            tagCounter[0] += 1
        elif re.match(regexArray[1], line):
            tag = "mistakes"
            line = " " + line  # Anki doesn't allow # as first sign it seems?
            noteMistOut.write(" " + separatorPadding(line, separatedBy, 2, tag, ""))
            tagCounter[1] += 1
        elif re.match(regexArray[2], line):
            cardBack = line.strip()
            tag = "Book:"
        elif re.match(regexArray[3], line):
            cardBack = line.strip()
            tag = "30secSummaries"
        elif re.match(regexArray[4], line):
            tag = "notes"
            line = " " + line  # Anki doesn't allow # as first sign it seems?
            noteMistOut.write(" " + separatorPadding(line, separatedBy, 2, tag, ""))
            tagCounter[4] += 1

        elif re.match(regexArray[5], line):
            tag = "LifeProTips"
            catchAnki.write(separatorPadding(line, separatedBy, 3, tag, "LPT"))
            tagCounter[5] += 1

        elif re.match(regexArray[6], line) or tag == "break":
            tag = "break"
            # print("Howdy Yall,  the line is : "+ line)
            backToDyna.write(line)
            tagCounter[6] += 1

        elif re.match(regexArray[7], line):
            cardBack = line.strip()
            tag = "Spreed"
            tagCounter[7] += 1

        elif re.match(regexArray[8], line, re.IGNORECASE):
            tag = "messenger"
            trash.write(line)
            tagCounter[8] += 1

        elif re.match(regexArray[7], tag):
            f.write(book_source_padder(line, separatedBy, cardBack, tag))
            tagCounter[7] += 1

        elif tag == "30secSummaries":
            # card = book_source_padder(line, separatedBy, cardBack, tag)

            f.write(separatorPadding(line, separatedBy, 2, tag, cardBack))
            tagCounter[3] += 1

        elif tag == "Book:":
            # card = book_source_padder(line, separatedBy, cardBack, tag)
            f.write(separatorPadding(line, separatedBy, 2, tag, cardBack))
            tagCounter[2] += 1

        elif tag == "DailyEval":
            DailyEvalFile.write(line)
            tagCounter[0] += 1
        else:
            backToDyna.write(line)
            numCards += 1

        n += 1
        # print("1    " + line)
    #    currentBook = "KaosCows"

    #    n+=1
    f.close()
    noteMistOut.close()
    backToDyna.close()
    trash.close()
    catchAnki.close()
    printNumCards(tagCounter, numCards)


def fileSearch(inputline, comparisonFile):
    print("it fucking works, my god it works")
    m = ""
    # comparison = open(comparisonFile, "r")
    ref = open("referenceFiles.txt", "r")
    lines = ref.readlines()
    print(len(lines))
    ref.close()
    trash = open("Trash.txt", "w")
    finalRes = ""
    finRes2 = ""
    reg = hackyRegExGen(inputline)
    print(reg)
    # print(lines[1])
    for line in lines:
        # print("mi")
        try:
            m = re.search(reg, line, re.IGNORECASE)
            # m = splitCompare(inputline, line) #fucking damn it this was here
            # print("in try")
            if m:
                # print("in if")
                # finalRes = m.group(1)
                finRes2 = m.group()
                print(finRes2)
                ref.close()
                # print("in m")
                # print(finalRes)
                # print(line[116085: 116122])
                return m.group()

            else:
                # print("in else")
                # print(inputline)
                # print(reg)
                # print(regline)
                ref.close()

        except:
            print("Trashman")
            trash.write(inputline)

    # print("int the end")
    # print(finalRes)
    print(finRes2)

    # print("in the end")
    ref.close()  # searches comparisonFile for inputline with added spaces


def splitCompare(
    input, reference
):  # outdated attempt, the approach was harder than using hackyRegExGen so it remains unfunctional
    splitInput = "".join(input.split())
    splitRef = "".join(reference.split())
    m = re.search(splitInput, splitRef)
    if m:
        print(m)
        return m


def hackyRegExGen(inputline):
    # creates a regex with optional space between each character of the input. used for matching texts without space to the corresponding text with spaces
    inputline = "".join(inputline.split())
    reg = ""
    # if ((len(inputline)-1) < cutoff):
    #    cutoff = (len(inputline)-1)
    for character in inputline:
        if charNeedEscape(character):  # hacky solution to escape chara
            character = "\\" + character

        reg = reg + character + "\s*"

    # print("hax")
    # print(reg)
    return (
        reg
    )  # , creates regex with possible spaces between each letter and digit (used for adding spaces to highlights from pdfs where spaces disapear)


def charNeedEscape(character):
    # true if character needs to be escaped for the regex
    normalChar = r"[a-zA-Z1-9]"
    if re.match(normalChar, character):
        print("False" + character)
        return False
    else:
        print("true" + character)
        return True  # determines if the char should be escaped for regex


def kindle_corrupt_bypass(corruptedCards):
    # Normal parser but it bypassess some cards in my kindle/anki dexk that are currupted
    # The corrupted cards are part of the anki deck, but will not prevent duplicates to be added, so to bypass this we ignore the first n cards that are corrupted

    kindle_text_gen(
        corruptedCards, "My Clippings.txt", "outputcorrupt.txt", "^", "TestCorrupt"
    )  # bypasses the first n cards in myclipplings due to them being corrupted


def kindle_text_gen(firstCard, inputName, outputName, separatorSign, cardTag):
    # todo make the referenceFiles approach work. Adding a parenthesis to hackyRegExGen might work, but makes it even hackier
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    outPut = open(outputName, "w")
    noSpaceFile = open("noSpaces.txt", "w")
    # refs = open("referenceFiles.txt", 'w')
    separatedBy = separatorSign
    tag = cardTag
    numCards = 0
    n = 0
    refFiles = "PatRecKomp"
    excluded_books = (
        r"PattRecKomp|Mark Manson"
    )  # todo remove second part of this if wrong
    space = r" +"
    teststring = "PattRecKomp (Arne Leijon & Gustav Eje Henter)"
    test2 = "ff a bab  aa "
    # print(re.search(refFiles, teststring))
    # print(re.search(refFiles, test2))
    while n < (len(lines) - 1):  # skip the last line

        if lines[n].strip() == "==========":  # this is the start of a kindle highlight
            back = lines[n + 1].strip()  # this line is the book and author
            front = lines[n + 4].strip()  # this line is the actual quote
            card = "%s %c %s %c %s \n" % (
                front,
                separatedBy,
                back,
                separatedBy,
                tag,
            )  # format to anki #Add another %c and separatedBy if you want to tag the card. Warning: this will make anki import it even if there is an identical card without the tag
            if 10000 < len(front):  # check if it's a reference file
                # refs.write(front + "\n")
                print("refs is closed for debugging")
            elif re.search(refFiles, back):
                noSpaceFile.write(card)
                # newFront = fileSearch(front, "referenceFiles.txt")
                # if not(newFront):
                #    newFront = front
                # print("nf" + newFront)
                # card = "%s %c %s %c %s \n" %(front, separatedBy, back, separatedBy, "RefFiles")
                # noSpaceFile.write(card)

            elif numCards > firstCard:
                outPut.write(card)
            numCards += 1
            n += 4  # skip the lines just used

        else:
            n += 1  # move to next line if current isn't start of highlight

    outPut.close()
    noSpaceFile.close()
    # backToDyna.close()
    print(
        "%s cards where created" % (numCards - firstCard)
    )  # generates file to be imported to anki with flashcards of all your highlights in kindle myclipplings.txt


def outdated_dynalist_text_gen(inputName, outputName, separatedBy, tag):
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    originalTag = tag
    outName = open(outputName, "w")
    mistaketag = r"\#mistake"
    noteTag = r"\#note"
    numCards = 0
    n = 0
    while n < (len(lines) - 1):  # skip the last line
        if re.match(mistaketag, lines[n]):
            tag = "mistakes"
            lines[n] = " " + lines[n]  # Anki doesn't allow # as first sign it seems?
        elif re.match(noteTag, lines[n]):
            tag = "notes"
            lines[n] = " " + lines[n]  # Anki doesn't allow # as first sign it seems?
        else:
            tag = originalTag
        nextCard = separatorPadding(lines[n], separatedBy, 2, tag, " ")
        outName.write(nextCard)

        numCards += 1
        n += 1
    outName.close()
    print(
        "%s cards where created" % (numCards)
    )  # outdated version of generalTextParser


def regexTags():
    dailyEvalTag = r"Daily eval"  # 0
    mistaketag = r"\#mistake"  # 1
    newBook = r"Book:"  # tag that identifies when transcription starts on new book
    newSummary = r"30sec:"  # 3
    noteTag = r"\#note"  # 4
    protip = r"LPT"  # 5
    breakTag = r"break:"  # 6
    spreedReg = r"Spreed"  # 7
    messengerTag = (
        r"(JAN|FEB|MAR|APR|MAY|JUN|Jun|JUL|Jul|AUG|Aug|SEP|OCT|NOV|DEC|Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
    )  # 8

    tagArray = [
        dailyEvalTag,
        mistaketag,
        newBook,
        newSummary,
        noteTag,
        protip,
        breakTag,
        spreedReg,
        messengerTag,
    ]
    tagCounter = [0]*(len(tagArray))
    # regexArray = [tagArray, tagCounter]
    print("In regex Tags, tagA:")
    print(tagArray)
    print("tagCount")
    print(tagCounter)
    return tagArray, tagCounter


def printNumCards(
    tagCounter, numCards
):  # parses files and specified input lines to anki files and sends unspecified lines to BackToDynalist.txt
    # @newCardArray : array where the number at each index indicates how many cards were written to that file
    # totCards = 0
    print("%s daily evals where created" % tagCounter[0])
    print("%s mistake where created" % tagCounter[1])
    print("%s Book where created" % tagCounter[2])
    print("%s 30sec where created" % tagCounter[3])
    print("%s note where created" % tagCounter[4])
    print("%s LPT where created" % tagCounter[5])
    print("%s break where created" % tagCounter[6])
    print("%s Spreed where created" % tagCounter[7])
    print("%s messenger where created" % tagCounter[8])
    print(
        "a total of %s cards were sent to backToDynalist" % (numCards)
    )  # prints how many cards/lines where written to each file


def old_generalTextParser(
    inputName
):  # got bored with this midwaythrough so its not done
    # A general parser that splits up the text into arrays for each regex and sends those arrays to the approrpiate method for that regex
    # Ex if it identifies the #mistake tag it will add it to a list of #mistake s which will then be turned into a mistake anki deck by a later function
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()

    # Regexes, ev todo: make this into argument instead
    dailyEvalTag = (
        r"(daily)+\s*(eval)+(uation)*"
    )  # regex noticing when I start a daily evaluation
    mistakeTag = r"\#mistake"
    spreedTag = r"Book:"

    # lists
    dailyEvalList = []  # if error, try changing this to other data structure
    mistakeList = []
    spreedList = []
    listList = []
    listList.append(dailyEvalList)
    listList.append(mistakeList)
    listList.append(spreedList)
    listList.append([0], "corn")
    # todo make the list of list work
    # Alteratively, figure out some other method of splitting lines into lists that then can be processed by submethods
    print(listList)
    currentReg = ""
    startPos = 0
    endPos = 0


def book_source_padder(line, separatedBy, book, tag):
    # Standard padding for books
    return (
        line.strip() + separatedBy + book + separatedBy + tag + "\n"
    )  # pads book cards with correct amount of separators for anki import


def separatorCounter(line, separatedBy):
    # Counts the number of serperatedBy in line. Used for ensuring correct amount of separatedBy
    pattern = r"" + re.escape(separatedBy)
    separations = re.findall(pattern, line)
    numSeparations = len(separations)
    return numSeparations  # counts number of separator signs in line


def separatorPadding(
    line, separatedBy, fieldNum, tag, backSide
):  # note- it assumes that if it gets 2 fields, the first is the front and the second is the back
    # returns the line split into or padded with the separatedBy fieldNum times

    numSeparations = separatorCounter(line, separatedBy)
    missingSeparators = fieldNum - numSeparations
    if missingSeparators > 3:
        print("Error in sepatorPadding, more than 2 separators missing")
    elif missingSeparators == 2:
        line = line.strip() + separatedBy + backSide + separatedBy + tag + "\n"
    elif missingSeparators == 1:
        line = line.strip() + " " + backSide + separatedBy + tag + "\n"
    elif missingSeparators:
        return line
    else:
        print("Error in sepatorPadding, more separators than indicated fields")

    return line  # pads cards with correct amount of separators


def dynalistCardGenerator(dynalistHTMLFile, outputName, separatedBy, tag):
    # Todos
    # look into how to use either the raw text or OPML to automatically create ankis from dynalist lists
    # Ideally it can look at the entire structure and break it up pseudo recursively
    # ie it will ask you about what the n top structures are and then what the n entries of each structure is

    # dynaListAllSteps: takes in html file and picks a list and outputs cards with front being the head and number of elements in list. Back is the list
    dynaListAllSteps(dynalistHTMLFile)
    # things i do with dyna anki: paste lists. take
    # htmlParser(dynalistHTMLFile)


def dynaListAllSteps(dynalistHTMLFile, lookForLeaves=False, outputName="out-dyna.txt"):
    # @param lookForLeaves, boolean of if the program should look for the leaves in the html and create card from that or just do cards of the topmost list
    if lookForLeaves:
        head, list = findList(dynalistHTMLFile, leaves=True)
    else:
        head, list = findList(dynalistHTMLFile, leaves=False)
    mode = 1
    dynaCardWriter(head, list, mode, outputName)


def dynaCardWriter(head, list, mode, outputFile):
    out = open(outputFile, "w")
    tag = "dynaAuto"
    if mode == 1:
        stepStr = numStepStr(list)
        front = head + stepStr
        back = " \n".join(list)
        card = front + "^" + back + "^" + tag
        return card

    return "error: mode not found"


def numStepStr(list):
    stepsString = "\n"
    n = 1
    while n < len(list) + 1:
        stepsString += str(n) + ") ... \n"
        n += 1
    return stepsString


def findList(HTMLFile, leaves):
    # res = hp.feed(dynalistHTMLFile)
    with open(HTMLFile) as f:

        parser = HTMLParser()
        # print(HTMLFile)
        print(parser.feed(f))
        #                "<!DOCTYPE html><html><body><ul><li>test<ul><li>ma</li><li>asd<ul><li>lksdfn</li></ul></li></ul></li></ul></body></html>"

        # print(hp.get_starttag_text())
        print("ended coding here")
    return None


main()
