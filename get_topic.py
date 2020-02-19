# AUTHOR: KARTHIK PEDDI
"""In order to use this topic_modelling program independently , the following files are necessary - "conversation.txt"
which contains the transcript of the conversation without any speaker tags with each dialogue in a single line. The results
of the topic modelling are written into the file "LDA_Visualization.html" and an extra file named "clean.txt" is created for
further processing if required which contains the conversation transcript without the stopwords"""

import re
import numpy as np
import pandas as pd

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS

def topic_modelling(conv_file):
    to_return = []
    #This line reads the conversation transcript without speaker tags and stores it in data variable
    file = open(conv_file, "r") 
    conv=file.read()
    file.close()
    data = [re.sub('\s+', ' ', conv)]

    #This function tokenizes a given sentence
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    #"SmartStoplist.txt" is a file containing some extra stopwords
    
    f=open("SmartStoplist.txt","r")
    stp2=f.read().split('\n')
    f.close()

    #The below lines include the english stopwords along with some extra stopwords in variable stop_words
    stop_words = stopwords.words('english')
    stop_words.extend(stp2)
    stop_words.extend(["hi","hello","bye","cheerio",'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])
    stop_words.extend(['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he','her', 'here','hers', 'herself', 'him', 'himself', 'his', 'how','i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other','our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she',"she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll",'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there','these', 'they','this', 'those', 'through', 'to', 'too', 'under', 'until', 'up','ve', 'very', 'was', 'wasn', "wasn't", 'we','were', 'weren', "weren't", 'what','when','where','which', 'while', 'who','whom', 'why', 'will','with', 'won', "won't",'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'])

    #This sentence tokenizes the data variable and stores in data_words
    data_words = list(sent_to_words(data))

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    #This function removes the stopwords from the input parameter "texts" of form [["HI ..."]]
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    #This function makes the bigrams from input parameter "texts" of form [["HI ..."]]
    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    #This function makes the trigrams from input parameter "texts" of form [["HI ..."]]
    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    #This function performs lemmatization given parameter "texts" of form [["HI ..."]]
    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """https://spacy.io/api/annotation"""
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    #data_words_nostops stores the data words after removing the stopwords
    data_words_nostops = remove_stopwords(data_words)

    #The below line stores the conversation transacript without any stopwords in the file "clean.txt"
    f=open("clean.txt","w")
    f.write(" ".join(data_words_nostops[0]))
    f.close()
    
    #For topic modelling some extra stopwords are included from file "BAGO1.txt"
    f=open("BAGO1.txt","r")
    stp1=f.read().split('\n')
    f.close()
    stop_words.extend(stp1)
    data_words_nostops = remove_stopwords(data_words)
    
    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    num=4
    
    #The below line creates an LDA model for topic modelling
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
    doc_lda = lda_model[corpus]
    fig=plt.figure()
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
    for t in range(lda_model.num_topics):
        a=fig.add_subplot(2,2,t+1)
        a.imshow(WordCloud(stopwords=STOPWORDS,background_color="white",
                             width=2500,height=2000,colormap='tab10',color_func=lambda *args, **kwargs: cols[t],prefer_horizontal=1.0).fit_words(dict(lda_model.show_topic(t, 200))))
        a.axis("off")
        a.title.set_text("Topic #" + str(t))
    fig.suptitle("Topic Wordcloud")
    topic_file = 'static/results/topic_word_cloud.png'
    to_return.append('topic_word_cloud.png')
    fig.savefig(topic_file,dpi=1200)
    plt.close(fig)
    plt.cla()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word);

    #The following line stores the results of topic modelling in a file named "LDA_Visualization.html"
    modelling_file = 'static/results/LDA_Visualization.html'
    pyLDAvis.save_html(vis, modelling_file)
    to_return.append('LDA_Visualization.html')

    return to_return