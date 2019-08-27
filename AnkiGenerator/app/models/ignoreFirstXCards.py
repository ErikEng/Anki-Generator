def ignoreFirstXCards(corruptedCards):
    #Normal parser but it bypassess some cards in my kindle/anki dexk that are currupted
    #The corrupted cards are part of the anki deck, but will not prevent duplicates to be added, so to bypass this we ignore the first n cards that are corrupted

    kindleGenerateCards(corruptedCards, 'My Clippings.txt', 'outputcorrupt.txt' , '^', 'TestCorrupt') #bypasses the first n cards in myclipplings due to them being corrupted
