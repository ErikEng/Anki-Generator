def numStepStr(list):
    stepsString = "\n"
    n = 1
    while (n < len(list)+1):
        stepsString += str(n) + ") ... \n"
        n+=1
    return stepsString
