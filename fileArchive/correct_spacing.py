def compare_incorrect_spacing_to_referece(inputline, comparisonFile):
    #GOAL: find
    #TODO finnish this one
    m = ""
    # comparison = open(comparisonFile, "r")
    ref = open("referenceFiles.txt", "r")
    lines = ref.readlines()
    print(len(lines))
    ref.close()
    trash = open("Trash.txt", "w")
    finalRes = ""
    finRes2 = ""
    reg = regex_padded_with_spaces(inputline)
    print(reg)
    # print(lines[1])
    for line in lines:
        # print("mi")
        try:
            m = re.search(reg, line, re.IGNORECASE)

            if m:
                finRes2 = m.group()
                print(finRes2)
                ref.close()
                return m.group()

            else:
                ref.close()

        except:
            print("Trashman")
            trash.write(inputline)

    print(finRes2)
    ref.close()  # searches comparisonFile for inputline with added spaces


def regex_padded_with_spaces(inputline):
    #creates a regex with "optional space" character between each character of the input.
    # This is used to match texts with incorrect spacing to the corresponding part of a text with correct spacing
    inputline = "".join(inputline.split())
    reg = ""
    #if ((len(inputline)-1) < cutoff):
    #    cutoff = (len(inputline)-1)
    for character in inputline:
        if not(is_special_char(character)):
                character= '\\'+ character #escape special characters

        reg = reg + character + "\s*"
    return reg

def is_special_char(character):
    #true if character needs to be escaped for the regex
    normalChar = r"[a-zA-Z1-9]"
    if (re.match(normalChar, character)):
        return True
    else:
        return False #determines if the char should be escaped for regex
