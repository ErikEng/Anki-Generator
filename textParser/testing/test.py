def testMode():
    #hackytest
    #if(charNeedEscape('d')):
    #    print("why?")
    #    return False
    #print("inTest")
    #refString = "distribution arises naturally in Bayesian"
    #testString = "observedfeaturevector is X =(X1. . .XL, XL +1. . . X2L)"
    #regex = hackyRegExGen(testString)
    #fileSearch(testString, 'referenceFiles.txt') #mode for testing specific fuctions faster

    #regTest
    line = "you have 2 cycles that control your sleep, so you need to keep them synchronisted to avoid being fatigued, how do you do that?; Go to sleep at a very regular rate and don't vary it at all if possible. Track your sleep with pulse trackers"
    tag = "30secSummaries"
    cardBack = "30sec: Biohacker/super-selfmedicator summary"
    separatedBy = ";"
    #card = book_source_padder(line, separatedBy, cardBack, tag)
    res = (separatorPadding(line, separatedBy, 2, tag, cardBack))
    #regList , muu = regexTags()
    #print(regList)
    #print(len(regList))
    #print(re.match(regList[0], refString))



    #dynatest
    # testHead = "Gnome Plan"
    # testList = ["Steal Socs", "???", "Profit"]
    # testOut = 'dynaAutoOut.txt'
    # #res = dynaCardWriter(testHead, testList, 1, testOut)
    # #res = numStepStr(testList)
    # res = findList('test.html', False)
    # print(res)
