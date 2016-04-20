import re

print("Please, type a text to be tokenized: ")
text = input()

def check_am_pm(token, tokens):
    if re.match('am|pm|a\.m|p\.m|%', token):
            index = tokens.index(token)
            new_token = tokens[index-1]+" "+token
            tokens[index-1] = new_token
            tokens.pop(index)

def check_extra_space(token, tokens):
    # to avoid misspelling
    if re.match('(.*\-$)', token):
            index = tokens.index(token)
            new_token = token+tokens[index+1]
            tokens[index] = new_token
            tokens.pop(index+1)
    if re.match('(^\-.*)', token):
            index = tokens.index(token)
            new_token = tokens[index-1]+token
            tokens[index-1] = new_token
            tokens.pop(index)

def process_numbers(token, tokens):
    # to avoid splitting tokens like 10 000 or 550 100
    index = tokens.index(token)
    if re.match('([0-9]+)', token) and re.match('([0-9]+)', tokens[index+1]):
            new_token = token+tokens[index+1]
            tokens[index] = new_token
            tokens.pop(index+1)

def avoid_misspelling(token, tokens):
    # to split tokens like "тёплое.Ну"
    if re.match('[a-zа-я]\.[A-ZА-Я]', token):
        index = tokens.index(token)
        new_tokens = token.split(".")
        tokens[index] = new_tokens[0]
        tokens = [tokens[index:] + [new_tokens[1]] + tokens[:index]]
        return tokens

def strip_token(token, tokens):
    index = tokens.index(token)
    tokens[index] = token.strip('.,!?:;"»«()[]<>')

def get_tokens(text):
    """
    Tokenize words.
    """
    tokens = text.split()
    for token in tokens:
        process_numbers(token, tokens)
    for token in tokens:
        check_am_pm(token, tokens)
    for token in tokens:
        check_extra_space(token, tokens)
    for token in tokens:
        avoid_misspelling(token, tokens)
    for token in tokens:
        strip_token(token, tokens)
    return tokens

print("Here are the tokens: \n")
for word in get_tokens(text):
    print(word)
print("Number of tokens: ", + len(get_tokens(text)))


"""
Sentence for testing:
20 % At 21.30 p.m. Mr. Smith bought cheapsite.com for 10 500 dollars in New -York, i.e. he paid a lot.
"""
