
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
