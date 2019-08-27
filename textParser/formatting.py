
def book_source_padder(line, separatedBy, book, tag):
    #Standard padding for books
    return(line.strip() + separatedBy + book + separatedBy + tag + "\n") #pads book cards with correct amount of separators for anki import

def separatorCounter(line, separatedBy):
    #Counts the number of serperatedBy in line. Used for ensuring correct amount of separatedBy
    pattern = r""+re.escape(separatedBy)
    separations = re.findall(pattern, line)
    numSeparations = len(separations)
    return numSeparations #counts number of separator signs in line

def separatorPadding(line, separatedBy, fieldNum, tag, backSide): #note- it assumes that if it gets 2 fields, the first is the front and the second is the back
    #returns the line split into or padded with the separatedBy fieldNum times

    numSeparations = separatorCounter(line, separatedBy)
    missingSeparators = fieldNum-numSeparations
    if (missingSeparators > 3):
        print("Error in sepatorPadding, more than 2 separators missing")
    elif (missingSeparators == 2):
        line = line.strip() + separatedBy + backSide + separatedBy + tag + "\n"
    elif (missingSeparators == 1):
        line = line.strip() + " " + backSide + separatedBy + tag + "\n"
    elif (missingSeparators):
        return line
    else:
        print("Error in sepatorPadding, more separators than indicated fields")

    return line #pads cards with correct amount of separators
