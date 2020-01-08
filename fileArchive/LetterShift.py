
def get_left_swifted_word(inputWord):
    shifted_word=[]
    for letter in inputWord:
        shifted_letter = get_swifted_letter(letter, "left")
        shifted_word.append(shifted_letter)
    word =  "".join(shifted_word)
    # pFrint(word)
    print(f"wird: {word}, input:{inputWord}")
    return word

def get_right_swifted_word(inputword):
    shifted_word=[]
    for letter in inputword:
     shifted_letter = get_swifted_letter(letter, "right")
     shifted_word.append(shifted_letter)
    word =  "".join(shifted_word)
    # print(word)
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
    return input_letter


def get_letter_list():
    line_1 = "qwertyuiopå"
    line_2 = "asdfghjklöä"
    line_3 = "<zxcvbnm,.-"

    all_lines = [line_1, line_2, line_3]
    all_lists =[]
    for line in all_lines:
        all_lists.append(list(line))

    return all_lists

def main():
    text = "dud rhoufh i sis ret ro PPWa gufhwe lwckk kiioa vt ewPWrubf nirubia qguxg rWT KUJWS UB IESWE RI BIR Gcw rgwn kYFG, U kai biruxws rgR RQGWWB NT KGUFG KIIOA QWEW UB SwaEEt diy á qA KIAR IB SWRuka kujw giq u qA VErgub fai uNUFG VW UNOIERbr ri vw oewoEWS DIE RGr arydd ub rgw dyryewm w reUAYEDxw ibwa ri m gn bi reUB GUFG KWCWK RI ARer ayedXW IBWA QNbyKKT DIE XUEXYKe vewRGUBF ai S RGWB DIXYA IB EWNUBSUBF AWKD RI BIR VW RII SUARErws BS SI UBAREIAOWXRUIB drwe rgR, kai a´rgua qa qT NIEW OIAURUCW U EWNWNVWEWS AI UR AGIYKS OEIKKIT VW YAUWS NIEW a  AReryo rgRB  ewqES YB DYRYEW, Q"
    shifted_right = []
    texti = text.split(" ")
    for word in texti:
         word = word.lower()
         shifted_right.append(get_left_swifted_word(word))
    string = " ".join(shifted_right)
    print(string)
main()
