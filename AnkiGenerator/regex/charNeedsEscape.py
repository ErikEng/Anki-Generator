def charNeedEscape(character):
    #true if character needs to be escaped for the regex
    normalChar = r"[a-zA-Z1-9]"
    if (re.match(normalChar, character)):
        print("False" + character )
        return False
    else:
        print("true"+ character)
        return True #determines if the char should be escaped for regex
