# Bag of words for SentEval

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

if __name__ == '__main__':
    train = pd.read_csv('train.csv', header=0, \
                    delimiter="\t", quoting=3)

    test = pd.read_csv('test.csv', header=0, \
                    delimiter="\t", quoting=3)

    # Initialize an empty list to hold the clean reviews
    clean_train_reviews = []

    # Loop over each review; create an index i that goes from 0 to the length
    # of the review list

    print "Cleaning and parsing the training set movie reviews...\n"
    for i in xrange( 0, len(train["review_lemmas"])):
        words = train["review_lemmas"][i].split()
        clean_train_reviews.append(" ".join(words))


    # ****** Create a bag of words from the training set
    #
    print "Creating the bag of words...\n"

    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 1000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    # ******* Train a random forest using the bag of words
    #
    print "Training the random forest (this may take a while)..."


    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit( train_data_features, train["food"] )

    # Create an empty list and append the clean reviews one by one
    clean_test_reviews = []

    print "Cleaning and parsing the test set movie reviews...\n"
    for i in xrange(0,len(test["review_lemmas"])):
        words = train["review_lemmas"][i].split()
        clean_test_reviews.append(" ".join(words))

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    print "Predicting test labels for food ...\n"
    result_food = forest.predict(test_data_features)

    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit( train_data_features, train["interior"] )
    print "Predicting test labels for interior ...\n"
    result_interior = forest.predict(test_data_features)

    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit( train_data_features, train["price"] )
    print "Predicting test labels for price ...\n"
    result_price = forest.predict(test_data_features)

    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit( train_data_features, train["service"] )
    print "Predicting test labels for service ...\n"
    result_service = forest.predict(test_data_features)

    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit( train_data_features, train["whole"] )
    print "Predicting test labels for whole ...\n"
    result_whole = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe 
    output = pd.DataFrame( data={"food":result_food,
                                 "interior":result_interior, "price":result_price,
                                 "service":result_service, "whole":result_whole,
                                 "id":test["id"]} )

    # Use pandas to write the comma-separated output file
    output.to_csv('Bag_of_Words_model.csv', index=False, quoting=3)
    print "Wrote results to Bag_of_Words_model.csv"
