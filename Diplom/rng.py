# -*- coding: utf-8 -*-

import codecs
import pandas

infile = codecs.open('freqrnc2011.csv', 'r', 'utf8')
data = pandas.read_csv(infile, sep='\t')
infile.close()
print data.head()
quit()

#(wg - это граф, в котором узлы - слова):
neighbors = wg.vs
for pair in combinations(neighbors, 2):
    word0 = pair[0]["name"]
    word1 = pair[1]["name"]
    similarity = model.similarity(word0, word1)
    remaining = [vertex for vertex in wg.vs if vertex != pair[0] and vertex != pair[1]]
    drawedge = True
    for vertex in remaining:
        candidate = vertex["name"]
        if model.similarity(candidate, word1) > similarity and model.similarity(candidate, word0) > similarity:
            drawedge = False
            break
    if drawedge == True:
        wg.add_edge(pair[0].index, pair[1].index, cos_sim=similarity)