def regexTags():
    dailyEvalTag= r"Daily eval"     #0
    mistaketag = r"\#mistake"       #1
    newBook = r"Book:" #tag that identifies when transcription starts on new book
    newSummary = r"30sec:"          #3
    noteTag = r"\#note"             #4
    protip = r"LPT"                 #5
    breakTag = r"break:"            #6
    spreedReg = r"Spreed"           #7
    messengerTag = r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|MON|TUE|WED|THU|FRI|SAT|SUN)" #8

    tagArray = [dailyEvalTag, mistaketag, newBook, newSummary, noteTag, protip, breakTag, spreedReg, messengerTag]
    tagCounter = np.zeros(len(tagArray))
    #regexArray = [tagArray, tagCounter]
    print("In regex Tags, tagA:")
    print(tagArray )
    print( "tagCount")
    print(tagCounter)
    return tagArray, tagCounter
