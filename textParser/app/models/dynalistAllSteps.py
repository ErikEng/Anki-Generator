def dynaListAllSteps(dynalistHTMLFile, lookForLeaves, outputName):
    #@param lookForLeaves, boolean of if the program should look for the leaves in the html and create card from that or just do cards of the topmost list
    if(lookForLeaves):
        head, list = findList(dynalistHTMLFile, leaves == True)
    else:
        head, list = findList(dynalistHTMLFile, leaves == False)
    mode = 1
    dynaCardWriter(head,list, mode, outputName)
