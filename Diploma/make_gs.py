import codecs
import re
import json
import pandas
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

infile = codecs.open('freqrnc2011.csv', 'r')
freq_dict = pandas.read_csv(infile, sep='\t')
infile.close()
gs_lemmas = list(freq_dict.Lemma[:1150])

with open('../../Docs/ruwiktionary-20160501-pages-articles.xml', 'r') as file:
    wiktionary = file.read()

pages = wiktionary.split('</page>\n  <page>')

gs = {}

for page in pages:
    word = BeautifulSoup(page, 'xml').text.encode('utf8')
    if word in gs_lemmas:
        gs[word] = []
        parts = page.split('\n\n===')
        for part in parts:
            if 'Значение ===' in part:
                part = part.split('\n')
                senses = [sense for sense in part if '#' in sense]
                for sense in senses:
                    sense = sense.split('{{пример')[0]
                    sense = re.sub('{{.*?}}', '', sense)
                    sense = re.sub('[\[\]]', '', sense)
                    sense = sense.strip(' ,#;:\n')
                    if sense == '':
                        continue
                    else:
                        gs[word].append(sense)
        if len(gs[word]) == 0:
            del gs[word]

sense_num = []

for key in gs.keys():
    sense_num.append(len(gs[key]))

plt.figure(figsize=(10,13))
plt.hist(sense_num, 25)
plt.title('Number of senses histogram')
plt.show()

with open('gold_standard.json', 'w') as file:
    json.dump(gs, file, indent=4)
