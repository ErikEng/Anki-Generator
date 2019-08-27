def printNumCardsGenerated(tagCounter, numCards): #parses files and specified input lines to anki files and sends unspecified lines to BackToDynalist.txt
    #@newCardArray : array where the number at each index indicates how many cards were written to that file
    #totCards = 0
    print("%s daily evals where created" %tagCounter[0])
    print("%s mistake where created" %tagCounter[1])
    print("%s Book where created" %tagCounter[2])
    print("%s 30sec where created" %tagCounter[3])
    print("%s note where created" %tagCounter[4])
    print("%s LPT where created" %tagCounter[5])
    print("%s break where created" %tagCounter[6])
    print("%s Spreed where created" %tagCounter[7])
    print("%s messenger where created" %tagCounter[8])
    print("a total of %s cards were sent to backToDynalist" %(numCards)) #prints how many cards/lines where written to each file
