def dynaCardWriter(head, list, mode, outputFile):
    out = open(outputFile, 'w')
    tag = 'dynaAuto'
    if(mode == 1):
        stepStr = numStepStr(list)
        front = head + stepStr
        back = ' \n'.join(list)
        card = front + '^' + back + '^' + tag
        return card


    return "error: mode not found"
