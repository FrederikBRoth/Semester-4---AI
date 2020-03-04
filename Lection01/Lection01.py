import re

alphabetList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

morseList = [". -", "- . . .", "- . - .", "- . .", ".", ". . - .", "- - .", ". . . .", ". .", ". - - -", "- . -",
             ". - . .", "- -", "- .", "- - -", ". - - .", "- - . -", ". - .", ". . .", "-", ". . -", ". . . -",
             ". - -", "- . . -", "- . - -", "- - . .", ". - - - -", ". . - - -", ". . . - -", ". . . . -", ". . . . .",
             "- . . . .", "- - . . .", "- - - . .", "- - - - .", "- - - - -"]


def stringtomorse(text):
    output = ""
    for char in text:
        x = 0
        for letter in alphabetList:
            if char == letter:
                output += morseList[x] + "|"
            x += 1

    return output


def morsetostring(text):
    output = ""
    textMorseList = text.split("|");
    for morse in textMorseList:
        x = 0
        for letter in morseList:
            if morse == letter:
                output += alphabetList[x]
            x += 1

    return output


print(stringtomorse("hello"))

print(morsetostring(stringtomorse("okaymand")))
