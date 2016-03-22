# -*- coding: utf-8 -*-

# input1 : restaurant name

# 1) crawl zoon and foursquare
# 2) clean and lemmatize
# 3) classify
# 4) return statistics
###############################################################################

from bs4 import BeautifulSoup
import time
import urllib
import codecs
import foursquare
import pickle
from sklearn.externals import joblib
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pymystem3 import Mystem
m = Mystem()
trash = [' ','\n','.','!','?', '']

def foursquare_crawl(name):
	client = foursquare.Foursquare(client_id='3XM4S22O2C4HRHW1WSGIVMMNJZPMMYS3YYUFNGS1BNBNJMDY', \
								   client_secret='3L3MP0TQBPN05KPMM2AL0DO2L5XNL1AP30TCGDR4GQEKBLXW')
	place=client.venues.search(params={'near': 'Moscow', 'limit': 10, 'query': name})
	tr1=json.dumps(place)
	tr2=json.loads(tr1)
	tr3=json.dumps(tr2, indent=4, sort_keys=True)
	reviews = []
	for i in tr2['venues']:
		cafeid=i['id']
		e=client.venues.tips(cafeid)
		pop1=json.dumps(e)
		pop2=json.loads(pop1)
		pop3=json.dumps(pop2, indent=4, sort_keys=True, encoding='utf-8')
		for tip in pop2['tips']['items']:
			text=tip['text']
			reviews.append(text)
	return reviews
		
def zoon_crawl(name, reviews):
	respData = urllib.urlopen("http://zoon.ru/search/?query=" + name).read()
	rutext = respData.decode("utf-8")
	soup1 = BeautifulSoup(rutext, 'html.parser')
	links = soup1.find_all('li', 'service-item pd20 js-results-item  ')
	for link in links:
		if 'restaurant' in str(link):
			url = re.findall(r'href="(.*?)"', str(link))[1]
			x = urllib.urlopen(url).read()
			soup = BeautifulSoup(x, 'html.parser')
			texts = soup.find_all('div', 'simple-text comment-text js-comment-text')
			for text in texts:
				reviews.append(text.get_text())
	return reviews

def mystem(sentence):
    # Preprocess reviews.
    sentence = sentence.strip()
    lemmas = m.lemmatize(sentence)
    return lemmas

def preprocess(reviews):
	processed = []
	for review in reviews:
		review = mystem(review)
		lemmatized = ''
		for i in review:
			i = i.strip()
			lemmatized += i + ' '
		processed.append(lemmatized)
	return processed

###############################################################################
start = time.time()
name = "Рецептор"
# reviews = foursquare_crawl(name)
# reviews = zoon_crawl(name, reviews)
# print 'Foursquare and Zoon reviews ready! - got {} reviews in '.format(len(reviews)), time.time() - start, "seconds."

###############################################################################
#Lemmatizing and preprocessing for classifier

start = time.time()
# processed = preprocess(reviews)
print "it took", time.time() - start, "seconds."

###############################################################################
# Classify reviews

food_model = joblib.load("models/food.pkl")

# def classify(review):
# 	#input: lemmatized sentence
# 	#output: number from 1 and 5
# 	pass
#
# sentiments = []
# for review in processed:
# 	sentiment.append(classify(review))
#
# result = sum(sentiments) / len(sentiments)

##################################################
# start = time.time()
# import pymorphy2
# morph = pymorphy2.MorphAnalyzer()
# trash = [' ','\n','.','!','?', '']
#
# def mymorph(word):
#     # Preprocess reviews.
# 	p = morph.parse(word)[0]
# 	return p.normal_form
#
# processed = []
# for review in reviews:
# 	review = review.split()
# 	lemmatized = ''
# 	for word in review:
# 		word = word.strip('!,.?:;()"\'')
# 		if word not in trash:
# 			lemma = mymorph(word)
# 			lemmatized += lemma + ' '
# 	processed.append(lemmatized)
#
# print "it took", time.time() - start, "seconds."
