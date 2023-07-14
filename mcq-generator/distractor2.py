import nltk
#import pke
from nltk.corpus import stopwords
import string
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn
import requests
import json
import re
import random
import spacy
def getWordSense(sent,word):
    word=word.lower() 
    if len(word.split())>0: #Splits the word with underscores(_) instead of spaces if there are multiple words
        word=word.replace(" ","_")
    synsets=wn.synsets(word,'n') #Sysnets from Google are invoked
    if synsets:
        wup=max_similarity(sent,word,'wup',pos='n')
        adapted_lesk_output = adapted_lesk(sent, word, pos='n')
        lowest_index=min(synsets.index(wup),synsets.index(adapted_lesk_output))
        return synsets[lowest_index]
    else:
        return None


def getDistractors(syn,word):
    dists=[]
    word=word.lower()
    actword=word
    if len(word.split())>0: #Splits the word with underscores(_) instead of spaces if there are multiple words
        word.replace(" ","_")
    hypernym = syn.hypernyms() #Gets the hypernyms of the word
    if len(hypernym)==0: #If there are no hypernyms for the current word, we simple return the empty list of distractors
        return dists
    for each in hypernym[0].hyponyms(): #Other wise we find the relevant hyponyms for the hypernyms
        name=each.lemmas()[0].name()
        if(name==actword):
            continue
        name=name.replace("_"," ")
        name=" ".join(w.capitalize() for w in name.split())
        if name is not None and name not in dists: #If the word is not already present in the list and is different from he actial word
            dists.append(name)
    return dists
syn="country"
sent="india is very beautiful"
word="india"
dists=[]
wordsent=getWordSense(sent,word)
print(wordsent)
dists=getDistractors(syn,word)
print(*dists,sep=",")