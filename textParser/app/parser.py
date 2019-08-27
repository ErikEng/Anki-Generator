def generalTextParser(inputName, outputName, separatedBy, tag):
    #Bugs : (minor) tries to create cards from empty lines
    tag = tag
    #File init

    inputfile = open(inputName, "r")
    lines = inputfile.readlines()
    inputfile.close()
    f = open(outputName, 'w')
    noteMistOut = open("NotesAndMistakesOut.txt", 'w')
    backToDyna = open("BackToDynalist.txt", 'w') #text file of things that shouldn't be ankified
    trash = open("Trash.txt", 'w')
    catchAnki = open("catchallAnki.txt", 'w')
    DailyEvalFile = open("DailyEval.txt", 'w')


    cardBack = ""

    dailyEval = r"(daily)+\s*(eval)+(uation)*"  #regex noticing when I start a daily evaluation

    numCards = 0
    n = 0
    ##regex list
    regexArray, tagCounter = regexTags()

    ##textParser
    while n < (len(lines)-1): #skip the last line
        line = lines[n]
        #print("current tag = "+ tag )
        if(len(line)==0): #This doesnt actually fix the empty line bug. todo think of other fixes
            trash.write(line)
        elif(re.match(regexArray[0], line, re.IGNORECASE) ):
            tag = "DailyEval"
            #print("I like to moce it")
            DailyEvalFile.write(line)
            tagCounter[0]+= 1

        elif(re.match(regexArray[1], line)):
            tag = "mistakes"
            line = " " + line #Anki doesn't allow # as first sign it seems?
            noteMistOut.write(" "+ separatorPadding(line, separatedBy,2 , tag, ""))
            tagCounter[1]+= 1

        elif(re.match(regexArray[2], line) ):
            cardBack = line.strip()
            tag = "Book:"


        elif(re.match(regexArray[3], line)):
            #print("mui")
            cardBack = line.strip()
            tag = "30secSummaries"


        elif(re.match(regexArray[4], line)):
            tag = "notes"
            line = " " + line #Anki doesn't allow # as first sign it seems?
            noteMistOut.write(" "+separatorPadding(line, separatedBy,2 , tag, ""))
            tagCounter[4]+= 1

        elif(re.match(regexArray[5], line)):
            tag = "LifeProTips"
            catchAnki.write(separatorPadding(line, separatedBy, 3, tag ,"LPT"))
            tagCounter[5]+= 1

        elif(re.match(regexArray[6], line) or tag == "break"):
            tag = "break"
            #print("Howdy Yall,  the line is : "+ line)
            backToDyna.write(line)
            tagCounter[6]+= 1

        elif(re.match(regexArray[7], line)):
            cardBack = line.strip()
            tag = "Spreed"
            tagCounter[7]+= 1

        elif(re.match(regexArray[8], line)):
            tag = "messenger"
            trash.write(line)
            tagCounter[8]+= 1

        elif(re.match(regexArray[7], tag)):
            f.write(book_source_padder(line, separatedBy, cardBack, tag))
            tagCounter[7]+=1





        elif(tag =="30secSummaries"):
            #card = book_source_padder(line, separatedBy, cardBack, tag)

            f.write(separatorPadding(line, separatedBy, 2, tag, cardBack))
            tagCounter[3]+= 1

        elif(tag == "Book:"):
            #card = book_source_padder(line, separatedBy, cardBack, tag)
            f.write(separatorPadding(line, separatedBy,2, tag, cardBack))
            tagCounter[2]+= 1


        elif(tag == "DailyEval"):
            DailyEvalFile.write(line)
            tagCounter[0]+= 1
        else:
            backToDyna.write(line)
            numCards+=1

        n+= 1
        #print("1    " + line)
    #    currentBook = "KaosCows"


    #    n+=1
    f.close()
    noteMistOut.close()
    backToDyna.close()
    trash.close()
    catchAnki.close()
    printNumCardsGenerated(tagCounter, numCards)
