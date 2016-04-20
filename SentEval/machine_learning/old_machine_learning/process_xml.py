#!/usr/bin/python
# coding: utf-8
import sys,codecs,re
from xml.dom import minidom
from pymystem3 import Mystem
stoplist = set([w.strip() for w in codecs.open('stopwords_ru','r','utf-8').readlines()])
stoplist.add('\n')

m = Mystem()

def mystem(sentence):
    sentence = sentence.strip().decode('utf-8')
    lemmas = m.lemmatize(sentence)
    lemmas = [l.strip() for l in lemmas if not l.strip() in stoplist and not l.strip().isdigit()]
    return lemmas


argument = sys.argv[1]

def extract_reviews(xml):
    doc = minidom.parse(xml)
    node = doc.documentElement
    reviews = doc.getElementsByTagName("review")
    
    text_dic = []
 
    for review in reviews:
        ident = review.getAttributeNode('id')
        marks = review.getElementsByTagName("scores")
        for mark in marks:
    	    foodmark = mark.getElementsByTagName("food")[0].childNodes[-1].data
    	    interiormark = mark.getElementsByTagName("interior")[0].childNodes[-1].data
    	    servicemark = mark.getElementsByTagName("service")[0].childNodes[-1].data
    	categories = review.getElementsByTagName("categories")
    	categories_list = []
        for category in categories:
    	    cats = category.getElementsByTagName('category')
    	    for cat in cats:
    		cat_name = cat.getAttributeNode('name')
    		cat_sentiment = cat.getAttributeNode('sentiment')
    		#categories_list.append(cat_name.nodeValue+":"+cat_sentiment.nodeValue)
    		categories_list.append(cat_sentiment.nodeValue)
        texts = review.getElementsByTagName("text")
        for text in texts:
    	    text_dic.append((text.childNodes[-1].data.replace(u'`','').encode('utf-8'),foodmark,interiormark,servicemark,ident.nodeValue,categories_list))
    	#try:
	#    tok_dic.append(sentence.childNodes[-1].data.strip()+'SENTENCESENTENCE')
	#except AttributeError:
	#    tok_dic.append(' '+'SENTENCESENTENCE')
    return text_dic

a = extract_reviews(argument)

print 'ID\ttext\tFood\tInterior\tPrice\tWhole\tService'

for i in a:
    lemmas = ' '.join(mystem(i[0])).strip()
    text = re.sub('\s{2,}',' ',lemmas)
    print i[4],'\t',text.encode('utf-8'),'\t','\t'.join(i[5])