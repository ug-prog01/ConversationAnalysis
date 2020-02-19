"""
AUTHOR: KARTHIK PEDDI, UTKARSH MISRHA, NIPUN HEDAOO

The following project does the following given an audio file, number of speakers
in the audio file and the topics that had to be discussed in the audio file:

A)Get the transcript of the conversation in the audio file and store the conversation
without speaker tags with one dialogue in each line in "conversation.txt" and with tags
in "conv_with_tags.txt".

B)Do topic modelling on the conversation and store the results in 'LDA_Visualization.html'.

C)Draw and store the positive and negative word cloud of the words used in the converesation
in the files "positive_word_cloud.png" and "negative_word_cloud.png" respectively
if they exist.

D)Calculate the productivity of the conversation based on the topics that had to be discussed
entered by the user and print which topics havent occured in the conversation
atleast once.

E)Plot a line plot representing the positivity of each speaker in the conversation
based on the positivity of each of their dialogues.

F)Send a mail to each and every one who participated in the conversation, by taking
the sender's email id and passwords and the recipients email ids, the mail contains
all the above visualizations along with transcript.
"""
import transcription as ts
import analysis as sd
import action_items as ac
import get_topic as gp
import word_cloud as wc
import productivity as prod
import line_plot as lp
import send_mail as sm
import getpass


"""Getting the required inputs from the operator
"""

print("Enter the audio file path with extension:")
speech_file=input()
 
print("Enter the number of speakers in the audio file:")
speaker_count=int(input())

print("Please enter what had to be discussed in the audio file to compute productivity:\n(Please make sure to enter atleast 15 words:)")
inp=input()
while len(inp)<15:
    print("The input should contain atleast 15 words, please enter again:")
    inp=input()

print("Enter the mail id of the sender whose account is used to send mail to speakers in the conversation:")
username = input()
password = getpass.getpass(prompt="Enter the password of the sender account:")

print("Enter the mail ids of the people who took part in the conversation, seperated by a space:")
email_list = input().split(" ")

"""This function performs speaker diarization and stores the output in a 'JSON_DATA.json' file
"""
ts.transcription(speech_file)

"""The following funtion performs analysis of the audio file and stores the transcript
with tags in 'conv_with_tags.txt' and without tags in 'conversation.txt'.
It also performs analysis like talk time comparison, confidence comparison and
analysis of modulation of the audio file. The outputs are stored in 'Time.png', 'Conf.png' and
'Modulation.png' respectively.
"""
sd.analysis_of_json(speech_file)

"""This function performs the extraction of action items from the transcript provided by the previous
function i.e. analysis_of_json. It stores the result in a key value format in a file called 'action.txt'.
It contains the person responsible for a given task as the key and the task itself as the corresponding value.
"""
ac.filter()

"""This function reads the "conversation.txt" file and performs topic modelling
to get the topics discussed in the conversation and stores the result in
"LDA_Visualization.html" file"""
gp.topic_modelling()

"""This function takes the words in the conversation without the stopwords
stored in the file "clean.txt" and then draws a positive and negative word clouds if
atleast 3 positive or negative words exist respectively and store them in the file
"positive_word_cloud.png" and "negative_word_cloud.png" respectively"""
wc.draw_word_clouds()

"""The following function take the topics to be discussed in the converation as the input
from the user and gets the productivity of the conversation calculated by percentage of topics
actually discussed and also prints out the topics which have not occured in the
conversation"""
to_add_in_mail=prod.get_productivity(inp)

"""The uses plotly and vaderSentiment modules to get the positivity scores of each dialogue in the conversation
and plot them in a line plot for comparison of positivity of different speakers, the result is stored
in positivity_scores_comparison.html"""
lp.plot_positivity_scores(speaker_count)

"""The following function takes the sender email and password which is used to send
emails to speakers participated in the conversation who's email ids are also taken
as input from the user. All the insights gathered from the above analysis are sent
in the mail"""
sm.send_email(username,password,email_list,to_add_in_mail)