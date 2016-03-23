# -*- coding: utf-8 -*-
# WORD2VEC MODELS
import numpy as np
from gensim.models import word2vec

model = word2vec.Word2Vec.load_word2vec_format('./models/webcorpora.model.bin', binary= True)

def main(line, model, window):
    lemmas = line.split(" ")
    matrix = list()
    for lemma in lemmas:
        try:
            matrix.append(model[lemma])
        except KeyError:
            pass
    return np.mean(np.array(matrix), axis = 0))
        
