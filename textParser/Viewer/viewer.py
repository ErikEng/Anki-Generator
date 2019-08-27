def introMessage():
    runMode = 0
    possibleModes = 5
    while (runMode > possibleModes or runMode < 1):
        runMode = int(input("Welcome to the Fantastic Anki Generator."
         "What function do you want to use? \n "
         "1: Generate Kindle Anki cards \n "
          "2: Run general generator in quick mode \n "
          "3: Run general generator in step by step mode \n "
          "4 : take over the world \n "
          "5 : run testing mode \n "
      "Your desired mode:"))
    #4: generate anki deck with custom target input and output (not implemented yet) "")
    return runMode #greets used and prompts them to pick run mode

def modePicker(runMode):
    if(runMode == 1):
        ignoreFirstXCards(970) #creates anki cards from kindle clippings, the 970 is the number of cards that are corrupted in my anki-kindle deck, can be omitted for others.
    elif(runMode == 2):
        generalTextParser("input.txt", "output.txt", "^", "AnkiGenerator")
    elif (runMode == 3):
        defaultIn = "input.txt"
        defaultOut = "output.txt"
        defaultTag = "AnkiGenerator"
        defaultSeparator = "^"
        inputFile = input("What file do you want to take from? \n if you want the default of 'input.txt', just press enter")
        outputFile = input("What file do you want the cards to be written to? \n if you want the default of " + defaultOut+ ", press enter")
        separator = input("What separator sign do you want? \n space to keep "+defaultSeparator +" as default")
        tag = input("What tag do you want? \n space to keep " + defaultTag + "as default tag")
        if(inputFile == ''):
            inputFile = defaultIn
        if(outputFile == ''):
            outputFile = defaultOut
        if(separator == ''):
            separator = defaultSeparator

        if(tag == ''):
            tag = defaultTag

        #print("debugg, in: " + inputFile + "out: "+ outputFile)
        generalTextParser(inputFile, outputFile, separator, tag)


    elif(runMode == 4):
        print("Order 66 initiated")
        time.sleep(3)
        main()

    elif(runMode == 5):
        print("running test mode")
        testMode()
    else:
        print("invalid input")
        main()  #calls differnt functions based on result from greeter
