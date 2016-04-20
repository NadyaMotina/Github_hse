# -*- coding: utf-8 -*-

from pprint import pprint
import yaml,sys,os,re,json,codecs,subprocess
from pymystem3 import Mystem

m = Mystem()
trash = set([' ','\n','.','!','?'])

def mystem(sentence):
    sentence = sentence.strip()
    lemmas = m.lemmatize(sentence)
    lemmas = [(l,[]) for l in lemmas if not l in trash]
    return lemmas

class POSTagger(object):

    def __init__(self):
        pass   
    
    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
        """
        pos = [mystem(sentence) for sentence in sentences]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=True):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_lemma = ' '.join([word[0] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    
                    #print literal+' '+str(self.dictionary[literal])
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_lemma, taggings)
                    if is_single_token:
                        original_token_tagging = sentence[original_position][1]
                        tagged_expression[1].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
	current_token = sentence_tokens[0]
	tags = current_token[1]
	token_score = sum([value_of(tag) for tag in tags])
    	if previous_token is not None:
	    previous_tags = previous_token[1]
    	    if 'inc' in previous_tags:
        	token_score *= 2.0
    	    elif 'dec' in previous_tags:
        	token_score /= 2.0
    	    elif 'inv' in previous_tags:
        	token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])

def final(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

def sentiment(text):
    postagger = POSTagger()
    dicttagger_total = DictionaryTagger([ 'dicts/food_positive.yml', 'dicts/food_negative.yml',  'dicts/price_positive.yml', 'dicts/price_negative.yml', 'dicts/whole_positive.yml', 'dicts/whole_negative.yml', 'dicts/service_positive.yml', 'dicts/service_negative.yml', 'dicts/interior_positive.yml', 'dicts/interior_negative.yml', 'dicts/positive.yml', 'dicts/negative.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])
    dicttagger_food = DictionaryTagger(['dicts/food_positive.yml', 'dicts/food_negative.yml'])
    dicttagger_interior = DictionaryTagger(['dicts/interior_positive.yml', 'dicts/interior_negative.yml'])
    dicttagger_service = DictionaryTagger(['dicts/service_positive.yml', 'dicts/service_negative.yml'])
    dicttagger_price = DictionaryTagger(['dicts/price_positive.yml', 'dicts/price_negative.yml'])
    dicttagger_whole = DictionaryTagger(['dicts/whole_positive.yml', 'dicts/whole_negative.yml'])
    splitted_sentences = []
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    for sentence in sentences:
        sentence = sentence.split()
        splitted_sentences.append(sentence)

    pos_tagged_sentences = postagger.pos_tag(sentences)

    dict_tagged_sentences_total = dicttagger_total.tag(pos_tagged_sentences)
    dict_tagged_sentences_food = dicttagger_food.tag(pos_tagged_sentences)
    dict_tagged_sentences_interior = dicttagger_interior.tag(pos_tagged_sentences)
    dict_tagged_sentences_price = dicttagger_price.tag(pos_tagged_sentences)
    dict_tagged_sentences_service = dicttagger_service.tag(pos_tagged_sentences)
    dict_tagged_sentences_whole = dicttagger_whole.tag(pos_tagged_sentences)

    score_total = sentiment_score(dict_tagged_sentences_total)
    score_food = sentiment_score(dict_tagged_sentences_food)
    score_interior = sentiment_score(dict_tagged_sentences_interior)
    score_service = sentiment_score(dict_tagged_sentences_service)
    score_price = sentiment_score(dict_tagged_sentences_price)
    score_whole = sentiment_score(dict_tagged_sentences_whole)
    
    total = final(score_total)
    food = final(score_food)
    interior = final(score_interior)
    service = final(score_service)
    price = final(score_price)
    whole = final(score_whole)
    return {'food':food,'interior':interior,"price":price,"whole":whole,"service":service}