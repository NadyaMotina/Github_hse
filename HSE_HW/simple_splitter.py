import re

print("Please, type a text to be splitted: ")
text = input()

def splitter(text):
        """
        Split Russian text by sentences.

        Example:
        >>> splitter("Маша уронила мячик. Мячик уплыл.")
        ['Маша уронила мячик.', 'Мячик уплыл.']
        """
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-ZА-Я][a-zа-я]\.)(?<=\.|\?|\!)\s', text)
        for s in sentences:
                if s=="" or s==" ":
                        sentences.pop(sentences.index(s))
        return sentences

sentences = splitter(text)

print("Here are the splitted sentences: \n")
for s in sentences:
        print(s)

##Explanation for regex: (?<!\w\.\w.)(?<![A-ZА-Я][a-zа-я]\.)(?<=\.|\?|\!)\s

##(?<!\w\.\w.) Negative Lookbehind =
##              Matches if the current position in the string is not preceded by a match for
##              \w\.\w. This is called a negative lookbehind assertion.
##\w match any word character [a-zA-Z0-9_]
##\. matches the character . literally
##\w match any word character [a-zA-Z0-9_]
##. matches any character (except newline)

##(?<![A-ZА-Я][a-zа-я]\.) Negative Lookbehind 
##[A-ZА-Я] match a single character present in the list below
##[a-zа-я] match a single character present in the list below
##\. matches the character . literally

##(?<=\.|\?|/!) Positive Lookbehind
##1st Alternative: \.
##2nd Alternative: \?
##3rd Alternative: \!
##\s match any white space character [\r\n\t\f ]
