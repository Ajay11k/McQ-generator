# import spacy
import spacy
 
# load spacy model
def impWords(sentence):
      nlp = spacy.load('en_core_web_md')
      keyword=[]


      doc = nlp(sentence)
 

      for ent in doc.ents:
         keyword.append(ent.text)
      return keyword
sentence = "The Internet was developed by Bob Kahn and Vint Cerf in the 1970s. They began the design of what we today know as the 'internet. ' It was the result of another research experiment which was called ARPANET, which stands for Advanced Research Projects Agency Network."
impkey=impWords(sentence)
print(*impkey,sep=" ,")