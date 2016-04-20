# evaluate the time needed for this code
import time
start = time.time()

import numpy as np
import codecs, sys
from pymystem3 import Mystem

m = Mystem()
trash = set([' ','\n','.','!','?'])

texts = []
food = []
interior = []
price = []
whole = []
service = []

## Argument should be Raw_reviews.csv
argument = sys.argv[1]

def reading(argument):
    file = codecs.open(argument, 'r')
    data = file.readlines()
    for line in data:
        """
        Allocate text and sentiments between lists.
        """
        line = line.strip()
        line = line.split(';')
        texts.append(line[1])
        food.append(line[2])
        interior.append(line[3])
        price.append(line[4])
        whole.append(line[5])
        service.append(line[6])
    file.close()

def mystem(sentence):
    """
    Preprocess reviews.
    """
    sentence = sentence.strip()
    lemmas = m.lemmatize(sentence)
    lemmas = [(l,[]) for l in lemmas if l not in trash]
    return lemmas

def make_vocab(texts):
    """
    1) make a vocabulary
    2) replace each review with a list of processed words
    """
    words = [] # all words from all reviews
    all_reviews = [] # list of lists for each review
    for t in texts:
        review = mystem(t)
        review_words = []
        for w in review:
            for i in w:
                words.append(w[0])
            review_words.append(w[0])
        all_reviews.append(review_words)
    vocabulary = list(set(words))
    return all_reviews, vocabulary 
    
if __name__ == "__main__":
    reading(argument)
    all_reviews, vocabulary = make_vocab(texts)
    
    ### making lemmatized csv
    outfile = open(str(argument).strip('.csv')+'_lemmatized.csv', 'w')
    for i in range(len(all_reviews)):
    	for l in all_reviews[i]:
    		lemma = l.strip()
    		if lemma in trash:
    			all_reviews[i].remove(l)
        lemmas = ' '.join(all_reviews[i])
        outfile.write(str(i)+'\t'+lemmas+'\t'+food[i]+'\t'+interior[i]+'\t'+price[i]+'\t'+service[i]+'\t'+whole[i]+'\t'+'\n')  	    
    outfile.close()
    
    ### BONUS!
    ### making a dictionary
    outfile_voc = open(str(argument).strip('.csv')+'_vocab.txt', 'w')
    for i in vocabulary:
        outfile_voc.write(str(i)+';')
    outfile_voc.close()

print "it took", time.time() - start, "seconds."
