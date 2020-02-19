# AUTHOR: KARTHIK PEDDI
"""This code uses plotly and vaderSentiment modules to get the positivity scores of each dialogue in the conversation
and plot them in a line plot for comparison of positivity of different speakers, the result is stored
in positivity_scores_comparison.html"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt

"""
print("Enter the number of speakers in the conversation")
speaker_count=int(input())
"""

def plot_positivity_scores(speaker_count, conv_tag_file):
    plot_file = 'positivity_comparison.png'
    file = open(conv_tag_file, "r") 
    conv=file.readlines()
    dialogues=[[] for i in range(speaker_count)]
    for i in conv:
        dialogues[int(i[0])-1].append(i[3:-1])
    analyser = SentimentIntensityAnalyzer()
    scores=[[] for i in range(speaker_count)]
    maximum=0
    for i in dialogues:
        if len(i)>maximum:
            maximum=len(i)
    for i in range(len(dialogues)):
        for j in dialogues[i]:
            sentiment_dict = analyser.polarity_scores(j)
            scores[i].append(sentiment_dict['pos'])
    scores=np.array(scores)
    data=[]
    for i in range(speaker_count):
        trace=go.Scatter(x=np.arange(1,maximum,1),
                         y=scores[i],
                         mode='lines+markers',
                         name="Speaker "+str(i+1))
        data.append(trace)
    layout = go.Layout(
    title=go.layout.Title(
        text='Positivity scores comparison of various speakers',
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Dialogues Count',
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Positivity scores (0-1)',
        )
    ))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='positivity_comparison.html',auto_open=False)
    fig=plt.figure()
    for i in range(speaker_count):
        plt.plot(np.arange(1,len(scores[i])+1,1),scores[i],label="Speaker "+str(i+1))
    fig.suptitle('Positivity scores comparison of various speakers')
    plt.xlabel('Dialogues Count')
    plt.ylabel('Positivity scores (0-1)')
    plt.legend()
    fig.savefig('static/results/'+plot_file,dpi=1200)
    plt.close(fig)
    plt.cla()
    return plot_file

  
