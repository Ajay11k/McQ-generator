from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn
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
sent="I can hear bass sound. "
word="bass"
sent1="I love to play cricket"
word1="cricket"
meaning=getWordSense(sent1,word1)
print(meaning.definition())