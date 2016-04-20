######################################################################
# LDA model from
# based on http://nbviewer.ipython.org/urls/dl.dropbox.com/s/upx30tfijtlkv9t/Topic%20Modeling%20Demo.ipynb?dl=0

import nltk
import sys
import os
from math import log
import numpy as np
from time import time
from gensim import corpora, models, similarities

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

# nltk.download() #download WordNet corpora

def preprocess(text):
    wnl = nltk.WordNetLemmatizer()
    return [wnl.lemmatize(t) for t in text.lower().split()]

texts = []
for filename in os.listdir("text_data/"):
    with open("text_data/" + filename) as f: 
        texts.append(preprocess(f.read().decode('ascii')))

dictionary = corpora.Dictionary(texts)
print 'Original: {}'.format(dictionary)
dictionary.filter_extremes(no_below = 5, no_above = 0.5, keep_n=None)
dictionary.save('text.dict')
print 'Filtered: {}'.format(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('texts.mm', corpus) # store on disc

print corpus[0][0:20]

start = time()
model = models.ldamodel.LdaModel(corpus, id2word=dictionary,
                                 num_topics=10, chunksize=50,
                                 update_every=1, passes=2)
print 'Evaluation time: {}'.format((time()-start) / 60)

for position in range(10):
    for topic in range(0, 6):
        print model3.show_topic(topic)[position][1].center(20, ' '),
    print

some_document = corpus[0]
print model[some_document]

######################################################################
# Evaluation

def perplexity(model, corpus):
    corpus_length = 0
    log_likelihood = 0
    topic_profiles = model.state.get_lambda() / np.sum(model.state.get_lambda(), axis=1)[:, np.newaxis]
    for document in corpus:
        gamma, _ = model.inference([document])
        document_profile = gamma / np.sum(gamma)
        for term_id, term_count in document:
            corpus_length += term_count
            term_probability = np.dot(document_profile, topic_profiles[:, term_id])
            log_likelihood += term_count * log(term_probability)
    perplexity = np.exp(-log_likelihood / corpus_length)
    return perplexity

print 'Perplexity: {}'.format(perplexity(model, corpus))

######################################################################
# Second try

start = time()
model2 = models.ldamodel.LdaModel(corpus, id2word=dictionary,
                                  num_topics=100, update_every=0, passes=40)
print 'Evaluation time: {}'.format((time()-start) / 60)
print 'Perplexity: {}'.format(perplexity(model2, corpus))

######################################################################
# Third try

start = time()
model3 = models.ldamodel.LdaModel(corpus, id2word=dictionary,
                                  num_topics=5, update_every=0, passes=40)
print 'Evaluation time: {}'.format((time()-start) / 60)
print 'Perplexity: {}'.format(perplexity(model2, corpus))
