import pke
from nltk.corpus import stopwords #Stopwords are the words that we need to avoid while considering keyword extraction
import string
def getImportantWords(art): 
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
text="Java is a high-level, general-purpose, object-oriented, and secure programming language developed by James Gosling at Sun Microsystems, Inc. in 1991. It is formally known as OAK. In 1995, Sun Microsystem changed the name to Java. In 2009, Sun Microsystem takeover by Oracle Corporation."

impWords=getImportantWords(text) 
print(*impWords,sep=",")