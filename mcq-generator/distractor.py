import requests
import json
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
word="india"
dists=[]
dists=getDistractors2(word)
print(*dists,sep=",")