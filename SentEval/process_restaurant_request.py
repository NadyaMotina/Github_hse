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
import numpy as np
from gensim.models import word2vec
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
	# Preprocess reviews
	lemmas = m.analyze(sentence)
	lemmas_with_pos = []
	for i in lemmas:
		if 'analysis' in i.keys():
			if len(i['analysis']) != 0:
				l = i['analysis'][0]['lex']
				pos = i['analysis'][0]['gr'].split(',')[0].split('=')[0]
				lemmas_with_pos.append(l+'_'+pos)
	return lemmas_with_pos

def preprocess(reviews):
	# returns list of lists
	processed = []
	for review in reviews:
		review = mystem(review)
		processed.append(review)
	return processed

def classify(reviews, food_model, w2v_model): #, service_model, interior_model, ):
	matrix = list()
	for review in reviews:
		for lemma in review:
			try:
				matrix.append(w2v_model[lemma])
			except KeyError:
				pass
	result = np.mean(np.array(matrix), axis = 0)
	sentiment = food_model.predict(result)
	return sentiment

def main(name):
	start = time.time()
	reviews = foursquare_crawl(name)
	reviews = zoon_crawl(name, reviews)
	processed = preprocess(reviews)
	print 'Start model analysing'
	sentiment = classify(processed, food_model, w2v_model)
	print "it took", time.time() - start, "seconds."
	print sentiment
	return sentiment

###############################################################################
food_model = joblib.load("../../SentEval/models/food.pkl")
# service_model = joblib.load("../../SentEval/models/service.pkl")
# interior = joblib.load("../../SentEval/models/interior.pkl")
food_model = pickle.loads(food_model)
# service_model = pickle.loads(service_model)
# interior_model = pickle.loads(interior_model)

w2v_model = word2vec.Word2Vec.load_word2vec_format('../../SentEval/models/webcorpora.model.bin', binary= True)
print 'All models successfully loaded!'

start = time.time()
name = "Рецептор"
processed = main(name)
print processed