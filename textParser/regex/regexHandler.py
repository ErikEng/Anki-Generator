#Standard Imports
from typing import Dict
import re






def get_regexes()->Dict[str, str]: #Q Unsure if the regex is counted as a str or some other format?
    regexes = {
        "dailyEvalTag": r"Daily eval",
        "mistaketag": r"\#mistake",
        "newBook": r"Book:",
        "newSummary": r"30sec:",
        "noteTag": r"\#note",
        "protip": r"LPT",
        "breakTag": r"break:",
        "spreedReg": r"Spreed",
        "messengerTag": r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|MON|TUE|WED|THU|FRI|SAT|SUN)",
    }
    return regexes

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
