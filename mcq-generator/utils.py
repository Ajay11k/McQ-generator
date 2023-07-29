import nltk
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








def getimpWords(sentence):
             nlp = spacy.load('en_core_web_sm')
             keyword=[]


             doc = nlp(sentence)
        

             for ent in doc.ents:
                keyword.append(ent.text)
             return keyword
def splitTextToSents(art):
            s=[sent_tokenize(art)]
            s=[y for x in s for y in x]
            s=[sent.strip() for sent in s if len(sent)>15] #Removes all the sentences that have length less than 15 so that we can ensure that our questions have enough length for context
            return s
def mapSents(impWords,sents):
            processor=KeywordProcessor() #Using keyword processor as our processor for this task
            keySents={}
            for word in impWords:
                keySents[word]=[]
                processor.add_keyword(word) #Adds key word to the processor
            for sent in sents:
                found=processor.extract_keywords(sent) #Extract the keywords in the sentence
                for each in found:
                    keySents[each].append(sent) #For each keyword found, map the sentence to the keyword
            for key in keySents.keys():
                temp=keySents[key]
                temp=sorted(temp,key=len,reverse=True) #Sort the sentences according to their decreasing length in order to ensure the quality of question for the MCQ 
                keySents[key]=temp
            return keySents

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
def getDistractors2(word):
            word=word.lower()
            actword=word
            if len(word.split())>0: #Splits the word with underscores(_) instead of spaces if there are multiple words
                word=word.replace(" ","_")
            dists=[]
            url= "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word) #To get ditractors from ConceptNet's API
            obj=requests.get(url).json()
            for edge in obj['edges']:
                link=edge['end']['term']
                url2="http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
                obj2=requests.get(url2).json()
                for edge in obj2['edges']:
                    word2=edge['start']['label']
                    if word2 not in dists and actword.lower() not in word2.lower(): #If the word is not already present in the list and is different from he actial word
                        dists.append(word2)
            return dists
        
def generate_mcq(read):
    
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('popular')
        
        impWords=getimpWords(read)

       
        sents=splitTextToSents(read) 
        
        mappedSents=mapSents(impWords,sents)
        
        
        
        mappedDists={}
        for each in mappedSents:
            wordsense=getWordSense(mappedSents[each][0],each) #gets the sense of the word
            if wordsense: #if the wordsense is not null/none
                dists=getDistractors(wordsense,each) #Gets the WordNet distractors
                if len(dists)==0: #If there are no WordNet distractors available for the current word
                    dists=getDistractors2(each) #The gets the distractors from the ConceptNet API
                if len(dists)!=0: #If there are indeed distractors from WordNet available, then maps them
                    mappedDists[each]=dists
            else: #If there is no wordsense, the directly searches/uses the ConceptNet
                dists=getDistractors2(each)
                if len(dists)>0: #If it gets the Distractors then maps them
                    mappedDists[each]=dists
        return mappedDists,mappedSents
    
def write_mcq(mappedDists, mappedSents, text_widget,END):
    iterator = 1  # To keep the count of the questions
    for each in mappedDists:
        sent = mappedSents[each][0]
        p = re.compile(each, re.IGNORECASE)  # Converts into a regular expression for pattern matching
        op = p.sub("________", sent)  # Replaces the keyword with underscores (blanks)
        text_widget.insert(END, f"Question {iterator}-> {op}\n")  # Prints the question along with a question number
        options = [each.capitalize()] + mappedDists[each]  # Capitalizes the options
        options = options[:4]  # Selects only 4 options
        opts = ['a', 'b', 'c', 'd']
        for i, ch in enumerate(options):
            text_widget.insert(END, f"\t{opts[i]} {ch}\n")  # Print the options
        text_widget.insert(END, "\n")
        iterator += 1

            
            
        
       
    