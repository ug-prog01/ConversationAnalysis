#AUTHOR: UTKARSH MISHRA, NIPUN HEDAOO
# Import dependencies

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import *
import wave

"""This function plots the spectrogram of the given audio file i.e. plots amplitude of the audio
file w.r.t. time to show the variation of amplitude as a function of time.
"""
def show_wave(speech):

    # Plotting Spectrogram of given audio

    spf = wave.open(speech, 'r')
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')

    f = spf.getframerate()
    fig=plt.figure()
    fig.add_subplot(2,1,1)
    plt.plot(sound_info)
    fig.suptitle('Wave form and Spetrogram of audio file of the conversation')

    fig.add_subplot(2,1,2)
    spectrogram = specgram(sound_info, Fs = f, scale_by_freq=True, sides = 'default')

    Modulation_file = 'Modulation.png'

    fig.savefig(Modulation_file)
    spf.close()
    plt.close(fig)
    plt.cla()


"""Reads the JSON string per sentence and identifies the speaker of every sentence and calculates the
required statistics for the entire conversation and plots the same using bar plots. Also it stores the
transcripted file with speaker tags and without speaker tags in 'conv_with_tags.txt' and 'conversation.txt'
respectively after extracting the speaker labels and transcripts and arranging them as spoken.
"""
def analysis_of_json(json_file):

    # Initialize objects

    transcripts = []
    speaker_labels = []
    transcript_file = 'conv_with_tags.txt'
    conversation_file = 'conversation.txt'
    # json_file = 'JSON_DATA.json'
    speakers = {}
    speaker_conf = {}
    conf_avg = {}


    #Read data from the local json file

    with open(json_file) as json_file:
        json_data = json.load(json_file)


    # Convert interior lists of dictionaries into dictionaries to access elements using keys

    for olo in json_data:
        newDict={}
        if('results' in olo.keys()):
            for item in olo['results']:
                newDict.update(item)
            olo['results']=newDict
            transcripts.append(olo['results'])
        elif('speaker_labels' in olo.keys()):
            for item in olo['speaker_labels']:
                newDict.update(item)
            olo['speaker_labels']=newDict
            speaker_labels.append(olo['speaker_labels'])


    # Only access Final transcripts and not interim results

    final_transcripts = []
    for i in range(len(transcripts)):
        if(transcripts[i]['final'] == True):
            final_transcripts.append(transcripts[i])


    # Access Speaker Labels i.e. Speaker Diarization and store the final transcript locally
    print("\nThe transcript of the conversation is:")
    t_file1=open(transcript_file, 'w')
    t_file2=open(conversation_file, 'w')
    for i in range(len(speaker_labels) - 1):
        print('Speaker'+str(speaker_labels[i]['speaker'])+':'+final_transcripts[i]['alternatives'][0]['transcript']+' ; From : '+str(final_transcripts[i]['alternatives'][0]['timestamps'][0][1])+' ; To : '+str(speaker_labels[i]['to']))
        'Speaker'+str(speaker_labels[i]['speaker'])+' : '+final_transcripts[i]['alternatives'][0]['transcript']+'\n'
        t_file1.write(str(str(speaker_labels[i]['speaker'])+':'+final_transcripts[i]['alternatives'][0]['transcript']+'\n'))
        t_file2.write(final_transcripts[i]['alternatives'][0]['transcript']+'\n')
    t_file1.close()
    t_file2.close()


    # Calculate total time for individual speaker using python dictionaries

    for i in range(len(speaker_labels) - 1):
        if('Speaker'+str(speaker_labels[i]['speaker']) not in speakers.keys()):
            speakers['Speaker'+str(speaker_labels[i]['speaker'])] = str(float(((speaker_labels[i]['to'])-final_transcripts[i]['alternatives'][0]['timestamps'][0][1])))
        else:
            existing = float(speakers['Speaker'+str(speaker_labels[i]['speaker'])])
            current = float(((speaker_labels[i]['to'])-final_transcripts[i]['alternatives'][0]['timestamps'][0][1]))
            updated = existing + current
            speakers['Speaker'+str(speaker_labels[i]['speaker'])] = updated


    # Calculate avg confidence per speaker    

    for i in speakers.keys():
        speaker_conf[str(i)] = []

    for i in range(len(final_transcripts)):
        speaker_conf['Speaker'+str(speaker_labels[i]['speaker'])].append(float(final_transcripts[i]['alternatives'][0]['confidence']))

    for i in  speaker_conf.keys():
        conf_avg[str(i)] = sum(speaker_conf[i])/len(speaker_conf[i])


    # Plot the total time and average confidences

    talk_time = []
    for i in speakers.keys():
        talk_time.append(float(speakers[i]))

    speaker = []
    for i in conf_avg.keys():
        speaker.append(float(conf_avg[i]))

    Conf_file = 'Conf3.png'
    Time_file = 'Time3.png'

    y_pos = np.arange(len(talk_time))
    plt.bar(y_pos, talk_time, width = 0.65)
    plt.xticks(y_pos, speakers.keys())
    plt.xlabel('Speakers')
    plt.ylabel('Total Talk Time(in s)')
    plt.title('Talk time of Speakers')
    plt.savefig('static/results/'+Time_file)
    plt.close()
    plt.cla()

    y_pos = np.arange(len(speaker))
    plt.bar(y_pos, speaker, width = 0.55)
    plt.xticks(y_pos, conf_avg.keys())
    plt.xlabel('Speakers')
    plt.ylabel('Confidence')
    plt.title('Confidence of Speakers')
    plt.savefig('static/results/'+Conf_file)
    plt.close()
    plt.cla()
    # show_wave(au)

    return [Conf_file, Time_file]