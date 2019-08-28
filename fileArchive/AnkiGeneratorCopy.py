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

#TODO move this to Viewer
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

        # kindle_text_to_anki(
        #     970, "My Clippings.txt", "outputcorrupt.txt", "^", "TestCorrupt"
        # )
        #

        kindle_text_to_anki(
            0, "My Clippings.txt", "outputcorrupt.txt", "^", "TestCorrupt"
        )


    elif runMode == 2:
        generalTextParser("input.txt", "output.txt", "^", "AnkiGenerator")

    elif runMode == 3:
        user_input_mode()

    elif runMode == 4:
        hack_mainframe()

    elif runMode == 5:
        testMode()
    else:
        print("invalid input")
        get_mode_from_user()


def user_input_mode():
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

def hack_mainframe():
    print("Hacking all main frames")
    time.sleep(3)
    print("You've now hacked all computers, you are the hackerman")
    main()

def testMode():

    print("running test mode")
    # regTest
    line = "you have 2 cycles that control your sleep, so you need to keep them synchronisted to avoid being fatigued, how do you do that?; Go to sleep at a very regular rate and don't vary it at all if possible. Track your sleep with pulse trackers"
    tag = "30secSummaries"
    cardBack = "30sec: Biohacker/super-selfmedicator summary"
    separatedBy = ";"
    # card = book_source_padder(line, separatedBy, cardBack, tag)
    res = separatorPadding(line, separatedBy, 2, tag, cardBack)
    # print(res)

def get_input_text(inputName):
    with open(inputName, "r") as inputfile:
        lines = inputfile.readlines()
    return lines

#TODO move this to Model
def generalTextParser(inputName, outputName, separatedBy, tag):
    # BUG : (minor) tries to create cards from empty lines
    lines = get_input_text(inputName)

    #TODO move this to Repo
    desired_lists_to_sort_to = {
        outputName : [],
        "notes_and_mistakes" : [],
        "trash" : [],
        "anki_list" : [],
        "daily_evaluations" : [],
        "unhandled_text": [],
    }

    cardBack = ""

    regex_dict = get_regexes()

    desired_lists_to_sort_to = sort_text_into_lists(lines, desired_lists_to_sort_to, regex_dict, tag, separatedBy, outputName)

    save_lists_to_files(desired_lists_to_sort_to)

def sort_text_into_lists(lines, desired_lists_to_sort_to, regex_dict, tag, separatedBy, outputName):
    for line in lines:
        if re.match(regex_dict["dailyEvalTag"], line, re.IGNORECASE):
            tag = "DailyEval"
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

#TODO move this to repo
def save_lists_to_files(desired_lists_to_sort_to):
    for listname, lines in desired_lists_to_sort_to.items():
        with open(listname+".txt", "w") as text_file:
            for line in lines:
                text_file.write(line)

#TODO move this to Regex?
def get_regexes()->Dict[str, str]:
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

def kindle_text_to_anki(firstCard, inputName, outputName, separatorSign, cardTag):
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
                # newFront = compare_incorrect_spacing_to_referece(front, "referenceFiles.txt")
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


main()
