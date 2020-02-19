# AUTHOR: KARTHIK PEDDI
"""To run the following program independently the files "BAGO1.txt","SmartStopList.txt" containing extra stopwords should be present and
file "conversation.txt" containing the dialogues of the conversation with one dialogue in each line should also be present, the inputs required
by the user are the points to be discussed in the conversation, after running the program displays the productivity of the conversation based on the
number of topics covered as entered by the user and it also prints which topics have not been covered in the meeting"""

import nltk 
from nltk.corpus import wordnet 
from nltk.corpus import stopwords
import re
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess

#The below line stores the synonyms of every word in the keywords entered by the user in the list synonyms


"""The following lines have to be un-commented to use this file independently       
print("Please enter what had to be discussed in the audio file to compute productivity:\n(Please make sure to enter atleast 15 words:)")
inp=input()
while len(inp)>=15:
    print("The input should contain atleast 15 words, please enter again:")
    inp=input()

get_productivity(inp)
"""
def get_productivity(inp, conv_file):
    synonyms = [] 
    stop_words = stopwords.words('english')
    #This function tokenizes a given sentence
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        
    def generate_ngrams(s, n):
        # Convert to lowercases
        s = s.lower()
    
        # Replace all none alphanumeric characters with spaces
        s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    
        # Break sentence in the token, remove empty tokens
        tokens = [token for token in s.split(" ") if token != ""]
    
        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]

    trigrams=generate_ngrams(inp, 3)
    bigrams=generate_ngrams(inp, 2)
    keywords=list(sent_to_words([inp]))
    keywords=set(keywords[0])
    keywords=list(keywords)
    keywords=[keywords]

    #"SmartStoplist.txt" is a file containing some extra stopwords
    #Some more extra stopwords are included from file "BAGO1.txt"
    f=open("BAGO1.txt","r")
    stp1=f.read().split('\n')
    f.close()
    f=open("SmartStoplist.txt","r")
    stp2=f.read().split('\n')
    f.close()
    stop_words.extend(stp2)
    stop_words.extend(stp1)

    #This function removes the stopwords from the input parameter "texts" of form [["HI ..."]]
    def remove_stopwords(texts):
        return [word for word in texts if word not in stop_words]
    
    #From the user input of the topics to be discussed the stopwords are removed
    keywords=remove_stopwords(keywords[0])
    for i in range(len(keywords)):
        keywords[i]=keywords[i].lower()
    """The file "conversation.txt" contains the conversation with each dialogues in one line, the conversation
    is merged into one para and each word is converted into lowercase""" 
    f=open(conv_file,"r")
    data=f.read()
    data_words = re.sub('\s+', ' ', data)
    data_words=data_words.split(" ")
    f.close()

    for i in range(len(data_words)):
        data_words[i]=data_words[i].lower()

    #varibles flag, prev_flag and intial are used in various loops to check if the keyword is present in the conversation
    #The variable flag stores how many topics entered by the user are actually in the conversation
    #wordnet.synets cimmand gets the synonyms of a given word
    #The variable not_discussed stores the topics or keywords that did not occur atleast once in the conversation
        
    flag=0
    prev_flag=0
    initial=0
    not_discussed=[]
    for i in keywords:
        initial=flag
        for syn in wordnet.synsets(i):
            prev_flag=flag
            for j in syn.lemmas(): 
                if j.name() in data_words:
                    flag+=1
                    break
            if prev_flag!=flag:
                break
        if initial==flag:
            not_discussed.append(i)

    """
    #The productivity of the conversation is defined as the percentage of the topics in the topics to be discussed that have actually been discussed in the conversation
    print("The productivity of the conversation is:"+str(round((flag/len(keywords[0]))*100,2))+"%")
    print("The following topics have not been raised in the conversation:")

    #The below line must be changed to get bigrams or trigrams as output instead of single word keywords
    #To get bigrams instead of single words use print_biigrams()
    #To get trigrams instead of single words use print_trigrams()
    print(not_discussed)
    """
    to_return="The productivity of the conversation is:"+str(100-round((len(not_discussed)/len(keywords[0]))*100,2))+"%. "+"\nThe topics to be discussed input is:"+inp
    if len(not_discussed)!=0:
        to_return=to_return+"\n. The following topics have not been raised in the conversation:"
        to_return=to_return+str(not_discussed)
    
    def print_trigrams():
        for i in not_discussed:
            for j in trigrams:
                if i in j:
                    flag=0
                    for k in j.split(" "):
                        if k in keywords or k in data_words:
                            flag+=1
                    if flag>=2:
                        print(j)
        return 0

    def print_bigrams():
        for i in not_discussed:
            for j in trigrams:
                if i in j:
                    flag=0
                    for k in j.split(" "):
                        if k in keywords or k in data_words:
                            flag+=1
                    if flag>=2:
                        print(j)
        return 0
    return to_return
