
def fileSearch(inputline, comparisonFile):
    print("it fucking works, my god it works")
    m = ""
    #comparison = open(comparisonFile, "r")
    ref = open("referenceFiles.txt", 'r')
    lines = ref.readlines()
    print(len(lines))
    ref.close()
    trash = open("Trash.txt", 'w')
    finalRes = ""
    finRes2 = ""
    reg = hackyRegExGen(inputline)
    print(reg)
    #print(lines[1])
    for line in lines:
        #print("mi")
        try:
            m = re.search(reg, line, re.IGNORECASE)
            #m = splitCompare(inputline, line) #fucking damn it this was here
            #print("in try")
            if m:
                #print("in if")
                #finalRes = m.group(1)
                finRes2 = m.group()
                print(finRes2)
                ref.close()
                #print("in m")
                #print(finalRes)
                #print(line[116085: 116122])
                return(m.group())

            else:
                #print("in else")
                #print(inputline)
                #print(reg)
                #print(regline)
                ref.close()


        except:
            print("Trashman")
            trash.write(inputline)

    #print("int the end")
    #print(finalRes)
    print(finRes2)

    #print("in the end")
    ref.close() #searches comparisonFile for inputline with added spaces
