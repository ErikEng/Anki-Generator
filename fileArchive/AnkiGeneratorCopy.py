#Standard Modules
#3d party Modules
#Internal Modules
import re
import time  # just for a joke function
#from autocorrect import spell
from typing import List, Dict
import logging
# import html.parser as hp
#from html.parser import HTMLParser
from spellchecker import SpellChecker
from get_my_errors import get_my_errors
from dto import get_mode_dto

summary_dict = {}

def main():
    desired_mode = get_mode_from_user()
    modePicker(desired_mode)
    archive_input_file("input.txt") #HACK this shouldn't be hardcoded to only take in input.txt file
    print_parsing_summary()


#TODO move this to Viewer
def get_mode_from_user():
    desired_mode = int(
        input(
            "Welcome to the Fantastic Anki Generator. "
            "What function do you want to use? \n "
            "1: Generate Kindle Anki cards \n "
            "2: Run general generator in quick mode \n "
            "3: Run general generator in step by step mode \n "
            "4 : take over the world \n "
            "5 : run testing mode \n "
            "6 : run splitting mode \n "
            "7 : run timespamp removal mode \n "
            "8 : format to ascii \n "
            "Your desired mode: \n"
        )
    )
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
        general_mode("input.txt", "output", "^", "AnkiGenerator")

    elif runMode == 3:
        user_input_mode()

    elif runMode == 4:
        hack_mainframe_mode()

    elif runMode == 5:
        testMode()

    elif runMode == 6:
        mode = get_mode_dto("split_mode")
        locked_triggers_mode(mode)

    elif runMode == 7:
        mode = get_mode_dto("timestamp_removal_mode")
        locked_triggers_mode(mode)

    elif runMode == 8:
        mode = get_mode_dto("format_to_ascii")
        locked_triggers_mode(mode)
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
    general_mode(inputFile, outputFile, separator, tag)

def hack_mainframe_mode():
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
def general_mode(inputName, output_file_name, separatedBy, tag):
    # BUG : (minor) tries to create cards from empty lines
    lines = get_input_text(inputName)

    #TODO move this to Repo
    desired_lists_to_sort_to = {
        output_file_name : [],
        "notes_and_mistakes" : [],
        "trash" : [],
        "anki_list" : [],
        "daily_evaluations" : [],
        "unhandled_text": [],
        "corrections_dict":[],
    }


    cardBack = ""

    regex_dict = get_regexes()

    desired_lists_to_sort_to = sort_text_into_lists(lines, desired_lists_to_sort_to, regex_dict, tag, separatedBy, output_file_name)


    save_dict_of_lists_to_files(desired_lists_to_sort_to)

def locked_triggers_mode(mode_name):
    #parsing mode that manually locks parser to not look for other triggers. used for long texts that might contain other triggers that should be ignored
    lines = get_input_text("input.txt")
    results = {"output":[]}
    for line in lines:
        result_dict = run_mode(mode_name, line)
        results = combine_dictionaries(result_dict, results )
    results = post_process_results(results, mode_name)
    print(results)
    save_dict_of_lists_to_files(results)

def run_mode(mode, line) ->Dict[str, List[str]]:
    result_dict = {}
    if mode.name == "timestamp_removal":
        str_line = timestamp_removal(line)
        word_list = split_line_into_words(str_line)

    elif mode.name == "split_mode":
        #adds to a list that gets split up in post-processing
        word_list = split_line_into_words(line)

    elif mode.name == "format_to_ascii":
        word_list = format_to_ascii(line)

    else:
        raise Exception(f"mode {mode} not found")
    assert isinstance(word_list, List)
    key = mode.output_name
    result_dict[key] = word_list
    return result_dict

def post_process_results(results, mode):
    if mode == "split_mode":
        smaller_lists_dict = split_list_to_smaller_lists(results)
        processed = combine_dictionaries(results, smaller_lists_dict)
        return processed
    return results

def format_to_ascii(line):
    line = str(line)
    line = line.replace("\n", " .")
    line = line.replace("'b'", "")
    line = line.replace("'b", "")
    line = line.replace("\'b", "")
    line_str = str(line)
    line_str = line_str.encode('ascii', errors='ignore')
    line_str = line_str.decode('ascii')
    if isinstance(line_str, str):

        word_list = line_str.split(" ")
    else:
        print(f"line_str:{line_str}, was type: {type(line_str)}")
        word_list = line_str
    return word_list

def combine_dictionaries( new_dict , original_dict):
    for key, value in new_dict.items():
        if key not in original_dict:
            original_dict[key]=[]

        original_dict[key]=original_dict[key] + value # desired behaviour {'test': [1,2]}+{'test': [3,4]} = {'test': [1,2,3,4]}
    return original_dict

def split_line_into_words(line):
    words = (str(line).split(" "))
    word_list =  []
    for word in words:
        word_list.append(word+ " ")
    return word_list

def sort_text_into_lists(lines, desired_lists_to_sort_to, regex_dict, tag, separatedBy, output_file_name):
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
            desired_lists_to_sort_to[output_file_name].append(book_source_padder(line, separatedBy, cardBack, tag))

        elif re.match(regex_dict["spellcheck"], line):
            tag = "spellcheck"

        elif re.match(regex_dict["yt_transcribe"], line):
            tag = "yt_transcribe"

        elif tag == "yt_transcribe":
            transcibed_text = timestamp_removal(line)
            desired_lists_to_sort_to[output_file_name].append(transcibed_text)

        elif tag == "spellcheck":
            spell_checked_line, new_corrections = spell_check_handler(line)
            desired_lists_to_sort_to["corrections_dict"].append(new_corrections)
            desired_lists_to_sort_to[output_file_name].append(spell_checked_line)


        elif tag == "30secSummaries":
            # card = book_source_padder(line, separatedBy, cardBack, tag)

            desired_lists_to_sort_to[output_file_name].append(separatorPadding(line, separatedBy, 2, tag, cardBack))

        elif tag == "Book:":
            # card = book_source_padder(line, separatedBy, cardBack, tag)
            desired_lists_to_sort_to[output_file_name].append(separatorPadding(line, separatedBy, 2, tag, cardBack))

        elif tag == "DailyEval":
            desired_lists_to_sort_to["daily_evaluations"].append(line)
        else:
            desired_lists_to_sort_to["unhandled_text"].append(line)

    return desired_lists_to_sort_to

#TODO move this to repo
def save_dict_of_lists_to_files(desired_lists_to_sort_to):
    for listname, lines in desired_lists_to_sort_to.items():
        with open(listname+".txt", "w") as text_file:
            for line in lines:
                if isinstance(line, str):
                    text_file.write(line + " ")
                    add_to_parsing_summary(listname, line)
                else:
                    logging.error(f"line:{line} was not a str")


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
        "spreedReg": r"Spreed:",
        "messengerTag": r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|MON|TUE|WED|THU|FRI|SAT|SUN)",
        "spellcheck": r"spellcheck:",
        "academic_check": r"academic:",
        "gdocs_split": r"gdocs_split:",
        "yt_transcribe": r"yt_transcribe:",
    }
    return regexes

def split_list_to_smaller_lists(word_list):
    number_of_words_per_gdoc = 22000
    number_of_splits = (len(word_list)//number_of_words_per_gdoc )+ 1 #integer division rounded up
    if number_of_splits > 30: #to avoid creating massive amount of files by accident
        number_of_splits = 30
    current_list_num = 0
    smaller_lists = {}
    while current_list_num < number_of_splits:
        start_of_current_list = 0+current_list_num*number_of_words_per_gdoc

        end_of_current_list = number_of_words_per_gdoc +current_list_num*number_of_words_per_gdoc

        current_list = word_list[start_of_current_list:end_of_current_list] #picks the current 22000 word interval
        smaller_lists["gdocs_split"+str(current_list_num)]= ' '.join(current_list) #Saves to dict
        current_list_num+=1

    return smaller_lists

def timestamp_removal(line):
    is_timestamp = r"\d{2}.\d{2}"
    if not re.match(is_timestamp, line):
        return line
    return ""

def spell_check_handler(line):
    spell = SpellChecker()
    #load ok words
    spell.word_frequency.load_words(['imp', '\n'])
    my_common_errors = get_my_errors()
    corrected_line = ""
    new_corrections=""
    for word in line.split(" "):
        try:
            corrected_word = my_common_errors[word]
            print(f"Erik correction:{word}, to:{corrected_word}")

        except:

            corrected_word = spell.correction(word)
            if not corrected_word==word:
                new_corrections+=f"\"{word}\": \"{corrected_word}\", \n"
        # else:
        #     corrected_word = word
        #     print(f"no prob:{word}")

        corrected_line+= " "+corrected_word
    return corrected_line, new_corrections

def kindle_text_to_anki(firstCard, inputName, output_file_name, separatorSign, cardTag):
    # todo make the referenceFiles approach work. Adding a parenthesis to hackyRegExGen might work, but makes it even hackier
    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    outPut = open(output_file_name, "w")
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

def separatorPadding(line, separatedBy, fieldNum, tag, backSide):
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

def archive_input_file(inputfile):
    archive_file = "archive.txt"
    with open(archive_file, "a") as archive:
        with open(inputfile, "r") as input:
            archive.write(input.read())

def add_to_parsing_summary(list, line):
    global summary_dict
    try:
        summary_dict[list] = summary_dict[list] + 1
    except:
        summary_dict[list] = 0

def print_parsing_summary():
    global summary_dict
    print("The parsing printed lines to the following files")
    print(summary_dict)

main()
