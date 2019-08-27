# standard imports
import re  # regex

# 3d pary imports

# internal imports

# TODOs
"""
skapa classeer för anki korten och skapa ocks skapa standard funktioner för det.
t.ez check anki card formatiing.
roadmap
fix all importans and depemdemcies so that the code can be run with the new infrastructure
make clss for annki numCards
front
back
tag
(something else?)
anki-kort metoder:
ensure_enogh_fields,
count_fields
set_fields()
get_fields()


make profram for general (???)
thoughts make it a class and then rewrite it graduallu
make a general parser, but how do i make it able to dynamically send text?
and how to deal with texts with text in middle of it
ideas:
General text parsing and triggers for other behaviour.
ex
text_parse(input_document, mode)
    check_for_keywords(active_flags?)
    <keyword>_reaction(line?)
        add_to_card
        set_flags
        add_to_document


"""


def kindleGenerateCards(firstCard, inputName, outputName, separatorSign, cardTag):
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
    # space = r" +"
    # teststring = "PattRecKomp (Arne Leijon & Gustav Eje Henter)"
    # test2 = "ff a bab  aa "
    # print(re.search(refFiles, teststring))
    # print(re.search(refFiles, test2))
    while n < (len(lines) - 1):  # skip the last line
        # logic for formatting ankikindle anki cards
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
