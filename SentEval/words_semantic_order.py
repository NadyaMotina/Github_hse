__author__ = 'thatdau'

def formWordsDictionary(dict_path):
    dictionary = []
    with open(dict_path) as dict_file:
        idx = 0
        for line in dict_file:
            wordpair_id = line.strip().split('\t')[0]
            wordpair_word = line.strip().split('\t')[2]
            if (idx != 0):
                dictionary.append((wordpair_id, wordpair_word))
            idx += 1
    return dictionary, idx-1

def compute_sim(word, other_word, model):
    sim = 0

    if too_similar(word, other_word):
        sim = -100
        return sim

    try:
        # if space in word, split it and take a mean of both words similarities
        word0 = None
        word1 = None
        if '_' in word:
            word0 = word.split('_')[0]
            word1 = word.split('_')[1]
        if ' ' in word:
            word0 = word.split(' ')[0]
            word1 = word.split(' ')[1]
        if word0 is not None and word1 is not None:
            sim0 = model.similarity(other_word, word0)
            sim1 = model.similarity(other_word, word1)
            sim = (sim0 + sim1) / 2
        else:
            sim = model.similarity(other_word, word)
    except:
        # if there is no such word in the model Word2Vec
        sim = -10
    return sim

def too_similar(word, previous):
    # Check if words have same stem
    len1 = len(previous) /2 + 1
    len2 = len(word) /2 + 1
    if len1 > 2 and word[:len1] == previous[:len1]:
        return True
    elif len2 > 2 and previous[:len2] == word[:len2]:
        return True
    else:
        return False

from gensim.models import Word2Vec
model = Word2Vec.load_word2vec_format('/Users/thatdau/Documents/EasyTen/Semantic_sim/models/GoogleNews-vectors-negative300.bin', binary=True)
print 'Model loaded!'

dict_path = '/Users/thatdau/Documents/EasyTen/New_words/from_search/orders_mapped_22_03_2016/eng.rus.tsv'
dictionary, total = formWordsDictionary(dict_path)
print 'Dictionary loaded!'

import random

def orderForWord(wordpair, dictionary, model):
    sorted_words = sorted([some_wordpair for some_wordpair in dictionary if some_wordpair[0] != wordpair[0]],
                          key = lambda w: (compute_sim(wordpair[1], w[1], model), random.random()),
                          reverse = True)
    return sorted_words

import os
import json

idx = 0
directory = '/Users/thatdau/Documents/EasyTen/words_semantic_order/'
if not os.path.exists(directory):
    os.makedirs(directory)

for wordpair in dictionary:
    if (idx % 100 == 0):
        print 'Done words:', idx

    sorted_order = orderForWord(wordpair, dictionary, model)
    ids = [w[0] for w in sorted_order]

    with open(directory+str(wordpair[0])+'.json', 'wb') as word_file:
        json.dump(ids, word_file)

    idx += 1