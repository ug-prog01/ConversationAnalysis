# AUTHOR: KARTHIK PEDDI
"""The following program to be used independently needs an input file named
"clean.txt" which contains the transcript of a conversation or the document to
be classified as positive and negative words for word cloud visualization. The
document data should not contain any stopwords, for removing stopwords please
refer "get_topic.py" file"""

from collections import defaultdict as dd
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt1
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def draw_word_clouds():
    return_list = []
    #The following line reads "clean.txt" file to get the conversation or paragraph without stopwords
    f=open("clean.txt","r")
    data=[f.read()]
    f.close()
    plt1.cla()
    """The following line creates a dictionary which stores only integers as values
    and is used to store the integer representing how many times a word occurs in positive
    context and how many times in a negative context, every time the word occurs in
    a positive context the value of the word with that key is oncreased by +1 else if
    word occurs in negative context the value is decreased by '-1'
    """
    word_positivity=dd(int)
    
    #The following line creates a Sentiment Analyzer Object which gives the positivity and negativity scores of a sentence
    analyser = SentimentIntensityAnalyzer()

    """The following loop takes a sentence and if sentence is found out
    to be positive by sentiment analyzer, the values of the corresponding keys of
    all the words in the sentence are increased by +1 , if negative decreased by -1
    """
    for sentence in data:
        sentiment_dict = analyser.polarity_scores(sentence)
        if sentiment_dict['compound'] >= 0.05 : 
            for i in sentence.split(" "):
                word_positivity[i]+=1            
        elif sentiment_dict['compound'] <= - 0.05 :
            for i in sentence.split(" "):
                word_positivity[i]-=1 

    """The following function takes the input parameters list of words,
    color of graph and the string which represents whether the word cloud is positive
    or negative and then draws the wordcloud and stores positive word cloud in
    'positive_word_cloud.png' adn negative word cloud in 'negative_word_cloud.png'
    if they exist"""

    def wordcloud_draw(data, color,string):
        words = ' '.join(data)
        wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color=color,
                      width=2500,
                      height=2000
                     ).generate(words)
        plt1.cla()
        plt1.figure(1,figsize=(13, 13))
        plt1.imshow(wordcloud)
        plt1.axis('off')
        plt1.title(string,loc="center",fontsize= 30)
        if string=="Positive Word Cloud":
            plt1.savefig('static/results/positive_word_cloud.png',dpi=1200)
            return_list.append('positive_word_cloud.png')
        else:
            plt1.savefig('static/results/negative_word_cloud.png',dpi=1200)
            return_list.append('negative_word_cloud.png')
        plt1.cla()

    """The below lines take the positivity scores calculated earlier and then divide
    words as positive and negative and store them in lists "pos" and "neg" respectively
    """
    pos=[]
    neg=[]
    for i in word_positivity.keys():
        if word_positivity[i]>0:
            pos.append(i)
        elif word_positivity[i]<0:
            neg.append(i)
    #The below conditions make sure that word clouds are made only if atleast 3 positive or negative words exist
    if len(pos)>2:
        wordcloud_draw(pos,'white','Positive Word Cloud')
    if len(neg)>2:
        wordcloud_draw(neg,'black','Negative Word Cloud')
    return return_list