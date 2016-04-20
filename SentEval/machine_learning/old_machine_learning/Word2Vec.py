# Word2Vec for SentEval

import pandas as pd
import cython
import re
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Read data from files 
train = pd.read_csv( "train.csv", header=0, delimiter="\t", quoting=3 )
test = pd.read_csv( "test.csv", header=0, delimiter="\t", quoting=3 )

# Initialize an empty list to hold the clean reviews
clean_train_reviews = []

# Loop over each review; create an index i that goes from 0 to the length
# of the review list

print "Cleaning and parsing the training set movie reviews...\n"
for i in xrange( 0, len(train["review_lemmas"])):
    words = train["review_lemmas"][i].split()
    clean_train_reviews.append(" ".join(words))

# Initialize an empty list to hold the clean reviews
clean_test_reviews = []

# Loop over each review; create an index i that goes from 0 to the length
# of the review list

print "Cleaning and parsing the test set movie reviews...\n"
for i in xrange( 0, len(test["review_lemmas"])):
    words = test["review_lemmas"][i].split()
    clean_test_reviews.append(" ".join(words))

# Initialize an empty list to hold the clean reviews
sentences = []

# Loop over each review; create an index i that goes from 0 to the length
# of the movie review list

print "Cleaning and parsing the training set movie reviews...\n"
for i in xrange( 0, len(train["review_lemmas"])):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s',
                         train["review_lemmas"][i])

def makeFeatureVec(words, model, num_features):
    # Function to average all of the word vectors in a given
    # paragraph
    #
    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((num_features,),dtype="float32")
    #
    nwords = 0.
    #
    # Index2word is a list that contains the names of the words in
    # the model's vocabulary. Convert it to a set, for speed
    index2word_set = set(model.index2word)
    #
    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec,model[word])
    #
    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec,nwords)
    return featureVec

def getAvgFeatureVecs(reviews, model, num_features):
    # Given a set of reviews (each one a list of words), calculate
    # the average feature vector for each one and return a 2D numpy array
    #
    # Initialize a counter
    counter = 0.
    #
    # Preallocate a 2D numpy array, for speed
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    #
    # Loop through the reviews
    for review in reviews:
       #
       # Print a status message every 1000th review
       if counter%1000. == 0.:
           print "Review %d of %d" % (counter, len(reviews))
       #
       # Call the function (defined above) that makes average feature vectors
       reviewFeatureVecs[counter] = makeFeatureVec(review, model, \
           num_features)
       #
       # Increment the counter
       counter = counter + 1.
    return reviewFeatureVecs

# Import the built-in logging module and configure it so that Word2Vec 
# creates nice output messages
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

# Set values for various parameters
num_features = 300    # Word vector dimensionality                      
min_word_count = 40   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words

# Initialize and train the model (this will take some time)
from gensim.models import word2vec
print "Training model..."
model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

# If you don't plan to train the model any further, calling 
# init_sims will make the model much more memory-efficient.
model.init_sims(replace=True)

# It can be helpful to create a meaningful model name and 
# save the model for later use. You can load it later using Word2Vec.load()
model_name = "300features_40minwords_10context"
model.save(model_name)


# ****** Create average vectors for the training and test sets
#
print "Creating average feature vecs for training reviews"

trainDataVecs = getAvgFeatureVecs( clean_train_reviews, model, num_features )

print "Creating average feature vecs for test reviews"

testDataVecs = getAvgFeatureVecs( clean_test_reviews, model, num_features )


# ****** Fit a random forest to the training set, then make predictions
#
# Fit a random forest to the training data, using 100 trees
forest = RandomForestClassifier( n_estimators = 100 )

print "Fitting a random forest to food..."
forest = forest.fit( trainDataVecs, train["food"] )

# Test & extract results
result_food = forest.predict( testDataVecs )

print "Fitting a random forest to interior..."
forest = RandomForestClassifier( n_estimators = 100 )
forest = forest.fit( trainDataVecs, train["interior"] )

# Test & extract results
result_interior = forest.predict( testDataVecs )

print "Fitting a random forest to price..."
forest = RandomForestClassifier( n_estimators = 100 )
forest = forest.fit( trainDataVecs, train["price"] )

# Test & extract results
result_price = forest.predict( testDataVecs )

print "Fitting a random forest to service..."
forest = RandomForestClassifier( n_estimators = 100 )
forest = forest.fit( trainDataVecs, train["service"] )

# Test & extract results
result_service = forest.predict( testDataVecs )

print "Fitting a random forest to whole..."
forest = RandomForestClassifier( n_estimators = 100 )
forest = forest.fit( trainDataVecs, train["whole"] )

# Test & extract results
result_whole = forest.predict( testDataVecs )

# Write the test results
output = pd.DataFrame( data={"food":result_food,
                                 "interior":result_interior, "price":result_price,
                                 "service":result_service, "whole":result_whole,
                                 "id":test["id"]} )
output.to_csv( "Word2Vec_AverageVectors.csv", index=False, quoting=3 )
print "Wrote Word2Vec_AverageVectors.csv"
