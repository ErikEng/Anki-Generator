
def get_left_swifted_word(inputWord):
    shifted_word=[]
    for letter in inputword:
        shifted_letter = get_swifted_letter(letter, "left")
        shifted_word.append(shifted_letter)
    word =  "".join(shifted_word)
    print(word)
    return word

def get_right_swifted_word(inputword):
    shifted_word=[]
    for letter in inputword:
     shifted_letter = get_swifted_letter(letter, "right")
     shifted_word.append(shifted_letter)
    word =  "".join(shifted_word)
    print(word)
    return word

def get_swifted_letter(input_letter, mode):
    letter_lists = get_letter_list()
    for list in letter_lists:
        for counter, letter in enumerate(list):
            if letter==input_letter:
                if mode == "left":
                    return list[counter+1]
                if mode == "right":
                    return list[counter-1]
    return "shift failed"


def get_letter_list():
    line_1 = "qwertyuiopå"
    line_2 = "asdfghjklöä"
    line_3 = "<zxcvbnm,.-"

    all_lines = [line_1, line_2, line_3]
    all_lists =[]
    for line in all_lines:
        all_lists.append(list(line))

    return all_lists
