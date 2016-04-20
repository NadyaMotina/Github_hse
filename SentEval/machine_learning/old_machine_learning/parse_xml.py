#!/usr/bin/python
# coding: utf-8
import sys
from xml.dom import minidom

## argument should be 	SentiRuEval_rest_markup.xml
argument = sys.argv[1]

print 'Parsing XML tree...'
doc = minidom.parse(argument)
node = doc.documentElement
print 'Finished parsing.'

reviews = doc.getElementsByTagName("review")
text_list = []
cat_all = []

## Now we make a csv-file with id, raw review string, aspect sentiments 
outfile = open('Raw_reviews.csv', 'w')

for review in reviews:

	texts = review.getElementsByTagName("text")
	for text in texts:
		text_list.append(text.childNodes[-1].data)
	
	categories = review.getElementsByTagName("categories")
	cat_list = []
	for category in categories:
		cats = category.getElementsByTagName('category')
		for cat in cats:
			#cat_name = cat.getAttributeNode('name')
			#cat_name = cat_name.childNodes[-1].data
			cat_sentiment = cat.getAttributeNode('sentiment')
			cat_sentiment = cat_sentiment.childNodes[-1].data
			cat_list.append(cat_sentiment.encode('utf-8'))
	cat_text = ";".join(cat_list)
	cat_all.append(cat_text)
        
    	    
for i in range(0,len(reviews)):
    outfile.write(str(i)+';'+str(text_list[i].encode('utf-8'))+';'+str(cat_all[i])+'\n')  	    

outfile.close()
