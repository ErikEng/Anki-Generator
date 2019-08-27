def hackyRegExGen(inputline):
    #creates a regex with optional space between each character of the input. used for matching texts without space to the corresponding text with spaces
    inputline = "".join(inputline.split())
    reg = ""
    #if ((len(inputline)-1) < cutoff):
    #    cutoff = (len(inputline)-1)
    for character in inputline:
        if(charNeedEscape(character)): #hacky solution to escape chara
                character= '\\'+ character

        reg = reg + character + "\s*"


    #print("hax")
    #print(reg)
    return reg#, creates regex with possible spaces between each letter and digit (used for adding spaces to highlights from pdfs where spaces disapear)
