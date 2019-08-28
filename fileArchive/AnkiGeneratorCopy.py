import re
import time  # just for a joke function
#from autocorrect import spell
from typing import List, Dict
import logging
# import html.parser as hp
#from html.parser import HTMLParser

def main():
    desired_mode = get_mode_from_user()
    modePicker(desired_mode)

def get_mode_from_user():
    desired_mode = 0
    possibleModes = 5
    while desired_mode > possibleModes or desired_mode < 1:
        desired_mode = int(
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
    #TODO 4: generate anki deck with custom target input and output (not implemented yet) "")
    return desired_mode


def modePicker(runMode):
    if runMode == 1:
        kindle_corrupt_bypass(
            970
        )  # creates anki cards from kindle clippings, the 970 is the number of cards that are corrupted in my anki-kindle deck, can be omitted for others.
        #For other users, uncomment the line below

    elif runMode == 2:
        generalTextParser("input.txt", "output.txt", "^", "AnkiGenerator")

    elif runMode == 3:
        init_default_mode()

    elif runMode == 4:
        hack_mainframe()

    elif runMode == 5:
        testMode()
    else:
        print("invalid input")
        main()  # calls differnt functions based on result from get_mode_from_user




def generalTextParser(inputName, outputName, separatedBy, tag):
    # Bugs : (minor) tries to create cards from empty lines
    tag = tag
    lines = get_input_text(inputName)

    #TODO change this to a repository
    desired_lists_to_sort_to = {
        outputName : [],
        "notes_and_mistakes" : [],
        "trash" : [],
        "anki_list" : [],
        "daily_evaluations" : [],
        "unhandled_text": [],
    }

    #TODO make this into a DTO
    cardBack = ""

    regex_dict = get_regexes()

    ##textParser

    desired_lists_to_sort_to = sort_text_into_lists(lines, desired_lists_to_sort_to, regex_dict, tag, separatedBy, outputName)
    save_lists_to_files(desired_lists_to_sort_to)
    #NOTE I expect that each list, ex "trash", in desired_lists_to_sort_to get updated if trash gets updated
    #printNumCards(tagCounter, numCards)

def sort_text_into_lists(lines, desired_lists_to_sort_to, regex_dict, tag, separatedBy, outputName):
    for line in lines: #HACK previous version of this skipped the last line, unsure why
        if re.match(regex_dict["dailyEvalTag"], line, re.IGNORECASE):
            tag = "DailyEval"
            # print("I like to moce it")
            desired_lists_to_sort_to["daily_evaluations"].append(line)
        elif re.match(regex_dict["mistaketag"], line):
            tag = "mistakes"
            line = " " + line  # Anki doesn't allow # as first sign it seems?
            desired_lists_to_sort_to["notes_and_mistakes"].append(" " + separatorPadding(line, separatedBy, 2, tag, ""))
        elif re.match(regex_dict["newBook"], line):
            cardBack = line.strip()
            tag = "Book:"
        elif re.match(regex_dict["newSummary"], line):
            cardBack = line.strip()
            tag = "30secSummaries"
        elif re.match(regex_dict["noteTag"], line):
            tag = "notes"
            line = " " + line  # Anki doesn't allow # as first sign it seems?
            desired_lists_to_sort_to["notes_and_mistakes"].append(" " + separatorPadding(line, separatedBy, 2, tag, ""))

        elif re.match(regex_dict["protip"], line):
            tag = "LifeProTips"
            desired_lists_to_sort_to["anki_list"].append(separatorPadding(line, separatedBy, 3, tag, "LPT"))

        elif re.match(regex_dict["breakTag"], line) or tag == "break":
            tag = "break"
            # print("Howdy Yall,  the line is : "+ line)
            desired_lists_to_sort_to["unhandled_text"].append(line)

        elif re.match(regex_dict["spreedReg"], line):
            cardBack = line.strip()
            tag = "Spreed"

        elif re.match(regex_dict["messengerTag"], line, re.IGNORECASE):
            tag = "messenger"
            desired_lists_to_sort_to["trash"].append(line)

        elif re.match(regex_dict["spreedReg"], tag):
            desired_lists_to_sort_to[outputName].append(book_source_padder(line, separatedBy, cardBack, tag))

        elif tag == "30secSummaries":
            # card = book_source_padder(line, separatedBy, cardBack, tag)

            desired_lists_to_sort_to[outputName].append(separatorPadding(line, separatedBy, 2, tag, cardBack))

        elif tag == "Book:":
            # card = book_source_padder(line, separatedBy, cardBack, tag)
            desired_lists_to_sort_to[outputName].append(separatorPadding(line, separatedBy, 2, tag, cardBack))

        elif tag == "DailyEval":
            desired_lists_to_sort_to["daily_evaluations"].append(line)
        else:
            desired_lists_to_sort_to["unhandled_text"].append(line)

    return desired_lists_to_sort_to

def save_lists_to_files(desired_lists_to_sort_to):
    for listname, lines in desired_lists_to_sort_to.items():
        with open(listname, "w") as text_file:
            for line in lines:
                # print(f"list:",listname)
                # print(f"line:",line)
                text_file.write(line)

def get_input_text(inputName):
    with open(inputName, "r") as inputfile:
        lines = inputfile.readlines()
    return lines

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

            if m:
                finRes2 = m.group()
                print(finRes2)
                ref.close()
                return m.group()

            else:
                ref.close()

        except:
            print("Trashman")
            trash.write(inputline)

    print(finRes2)
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




def get_regexes()->Dict[str, str]: #Q Unsure if the regex is counted as a str or some other format?
    regexes = {
        "dailyEvalTag": r"Daily eval",
        "mistaketag": r"\#mistake",
        "newBook": r"Book:",
        "newSummary": r"30sec:",
        "noteTag": r"\#note",
        "protip": r"LPT",
        "breakTag": r"break:",
        "spreedReg": r"Spreed",
        "messengerTag": r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|MON|TUE|WED|THU|FRI|SAT|SUN)",
    }
    return regexes

def regex_padded_with_spaces(inputline):
    #creates a regex with "optional space" character between each character of the input.
    # This is used to match texts with incorrect spacing to the corresponding part of a text with correct spacing
    inputline = "".join(inputline.split())
    reg = ""
    #if ((len(inputline)-1) < cutoff):
    #    cutoff = (len(inputline)-1)
    for character in inputline:
        if not(is_special_char(character)):
                character= '\\'+ character #escape special characters

        reg = reg + character + "\s*"
    return reg

def is_special_char(character):
    #true if character needs to be escaped for the regex
    normalChar = r"[a-zA-Z1-9]"
    if (re.match(normalChar, character)):
        return True
    else:
        return False #determines if the char should be escaped for regex


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


#def dynalistCardGenerator(dynalistHTMLFile, outputName, separatedBy, tag):
    # Todos
    # look into how to use either the raw text or OPML to automatically create ankis from dynalist lists
    # Ideally it can look at the entire structure and break it up pseudo recursively
    # ie it will ask you about what the n top structures are and then what the n entries of each structure is

    # dynaListAllSteps: takes in html file and picks a list and outputs cards with front being the head and number of elements in list. Back is the list
    #dynaListAllSteps(dynalistHTMLFile)
    # things i do with dyna anki: paste lists. take
    # htmlParser(dynalistHTMLFile)


# def dynaListAllSteps(dynalistHTMLFile, lookForLeaves=False, outputName="out-dyna.txt"):
#     # @param lookForLeaves, boolean of if the program should look for the leaves in the html and create card from that or just do cards of the topmost list
    # if lookForLeaves:
    #     head, list = findList(dynalistHTMLFile, leaves=True)
    # else:
    #     head, list = findList(dynalistHTMLFile, leaves=False)
    # mode = 1
    # dynaCardWriter(head, list, mode, outputName)


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


#def findList(HTMLFile, leaves):
    # res = hp.feed(dynalistHTMLFile)
    #with open(HTMLFile) as f:

        #parser = HTMLParser()
        # print(HTMLFile)
        #print(parser.feed(f))
        #                "<!DOCTYPE html><html><body><ul><li>test<ul><li>ma</li><li>asd<ul><li>lksdfn</li></ul></li></ul></li></ul></body></html>"

        # print(hp.get_starttag_text())
        #print("ended coding here")
    #return None

# def spell_check_word(word):
#     return spell(word)


def hack_mainframe():
    print("Hacking all main frames")
    time.sleep(3)
    print("You've now hacked all computers, you are the hackerman")
    main()

def init_default_mode():
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
    generalTextParser(inputFile, outputFile, separator, tag)

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
    print("running test mode")
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

main()
