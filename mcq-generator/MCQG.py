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

from tkinter import *
from tkinter import *
from tkinter import ttk,messagebox
# import filedialog module
from tkinter import filedialog
from PIL import Image,ImageTk


  
# import filedialog module

from tkinter import filedialog

#file=open("articles/fiverules.txt","r", encoding="utf-8") #"r" deontes read version open
#text=file.read()

'''def getImportantWords(art): 
    extractor=pke.unsupervised.MultipartiteRank() #Using the Multipartite Unsupervised Extractor as our extractor
    extractor.load_document(input=art,language='en')
    pos={'PROPN'} #We are only considering proper nouns as valid candidates for our keywords
    stops=list(string.punctuation) #Stoplist contains the words to be avoided
    stops+=['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-'] #These stand for the brackets as in lrb=left round bracket="(" and so on
    stops+=stopwords.words('english')
    extractor.candidate_selection(pos=pos,stoplist=stops) #Sets the candidate selection criteria, as in, which should be considered and which should be avoided
    extractor.candidate_weighting() #Sets the preference criteria for the candidates
    result=[] 
    ex=extractor.get_n_best(n=25) #Gets the 25 best candidates according to the criteria set
    for each in ex:
        result.append(each[0]) 
    return result
impWords=getImportantWords(text)'''
 #Increase the counter
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
def browseFiles():
	

        filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))

        file = open(filename,encoding='utf-8')
        read = file.read()
	    
        print(read)
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('popular')
        
        impWords=getimpWords(read)
#print(*impWords,sep=",")
       
        sents=splitTextToSents(read) 
        
        mappedSents=mapSents(impWords,sents)
        
        
        
        mappedDists={}
        

        window1 = Tk()
        window1.title("MCQ Questions")
        window1.geometry("1100x1100+600+100")
        v = Scrollbar(window1,orient='vertical')
        v.pack(side=RIGHT,fill='y')
        t = Text(window1,height=200,width=200,bg="#C1C1CD",font="arial 15 bold",yscrollcommand=v.set)
        v.config(command=t.yview)
        t.pack()
        
        

       # favt = 'ajay is good boy.\n'
       # das = 'ajay is grat person'
        #t.insert(END,f"hello,{favt}")
       # t.insert(END,das)
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

                    t.insert(END,"**************************************        Multiple Choice Questions        *******************************")
                  
        t.insert(END,"\n")
        

        iterator = 1 #To keep the count of the questions
        for each in mappedDists:
            sent=mappedSents[each][0]
            p=re.compile(each,re.IGNORECASE) #Converts into regular expression for pattern matching
            op=p.sub("________",sent) #Replaces the keyword with underscores(blanks)
            t.insert(END,f"Question {iterator}-> {op}")#Prints the question along with a question number
            options=[each.capitalize()]+mappedDists[each] #Capitalizes the options
            options=options[:4] #Selects only 4 options
            opts=['a','b','c','d']
            t.insert(END,"\n")

            random.shuffle(options) #Shuffle the options so that order is not always same
            for i,ch in enumerate(options):
                t.insert(END,f"\t{opts[i]} {ch}\n") #Print the options
            t.insert(END,"\n")
            iterator+=1
        def save_text():
                s = t.get("1.0",END)
                fob = filedialog.asksaveasfile(filetypes=[('text file','*.txt')],defaultextension ='.txt',initialdir = "/",mode= 'w')
                fob.write(s)
            
                fob.close()
                t.delete('1.0',END)
                t.update()

        #save_text()
        bimg2 = PhotoImage(file='download.png')	
        button_save = Button(window,
                            text = "Save",compound=LEFT,image=bimg2,width=150,font="arial 10 bold",bg="black",fg="white",
                            command = save_text)
        button_save.place(x=190,y=450)	
            #b1.place(x=200,y=200)				
            
            
        file.close()
        window1.resizable(False,False)
        window1.pack()
            
        window1.mainloop()

	# Change label contents
	#label_file_explorer.configure(text="File Opened: "+filename)
	
	
																								
# Create the root window
window=Tk()

# Set window title
window.title('MCQ Generator')

# Set window size
window.geometry("500x500+100+100")
window.configure(bg="#C1FFC1")

image_icon = PhotoImage(file='base.png')
window.iconphoto(FALSE,image_icon)

#Set window background color

#window.config(background = "white")
'''bg = PhotoImage(file='base.png')
canvas1 = Canvas(window,width=500,height=500)
canvas1.pack(fill="both",expand=True)
canvas1.create_image(0,0,image=bg,anchor="nw")'''
# Create a File Explorer label

top_frame=Frame(window,bg="#FFA07A",width=500,height=100)
top_frame.place(x=0,y=0)
image = Image.open("MCq.png")
image = image.resize((64,64))
logo = ImageTk.PhotoImage(image)
Label(top_frame,image=logo,bg="#FFA07A").place(x=10,y=11)
Label(top_frame,text = "MCQ Generator from text",font="Helvetica 20 bold italic",
							fg = "#4B4B00",bg="#FFA07A").place(x=100,y=30)
Label(window,text = "Upload any text file and \n see the magic.",font="Helvetica 15 bold",
							fg = "#333333",bg="#C1FFC1").place(x=155,y=130)

image1 = Image.open("txt-open-file-format.png")
image1 = image1.resize((128,128))
logo1 = ImageTk.PhotoImage(image1)
Label(window,image=logo1,bg="#C1FFC1").place(x=200,y=200)
#label_canvas=canvas1.create_window(1,10,anchor ="nw",window=label_file_explorer)
bimg = PhotoImage(file='upload-file (1).png')	
button_explore = Button(window,
						text = "  Choose a file",compound=LEFT,image=bimg,width=150,font="arial 10 bold",bg="black",fg="white",
						command = browseFiles)
button_explore.place(x=190,y=350)						
#explore_canvas=canvas1.create_window(100,100,anchor ="nw",window=button_explore)						
bimg1 = PhotoImage(file='exit (1).png')	
button_exit = Button(window,
					text = "Exit",compound=LEFT,image=bimg1,width=150,font="arial 10 bold",bg="black",fg="white",
					command = exit)
button_exit.place(x=190,y=400)					
#exit_canvas=canvas1.create_window(100,140,anchor ="nw",window=button_exit)					

# Grid method is chosen for placingimage
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
#label_file_explorer.grid(column = 1, row = 1)

#button_explore.grid(column = 1, row = 2)

#button_exit.grid(column = 1,row = 3)

# Let the window wait for any events
window.resizable(False,False)
window.mainloop()
