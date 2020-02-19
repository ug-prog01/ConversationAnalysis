# AUTHOR: UTKARSH MISHRA
# Import dependencies

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import os
import json

def conv_files(json_file):
    transcripts = []
    speaker_labels = []
    transcript_file = 'static/results/conv_with_tags5.txt'
    conversation_file = 'static/results/conversation5.txt'
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
        # print('Speaker'+str(speaker_labels[i]['speaker'])+':'+final_transcripts[i]['alternatives'][0]['transcript'])
        str(speaker_labels[i]['speaker'])+' : '+final_transcripts[i]['alternatives'][0]['transcript']+'\n'
        t_file1.write(str(str(speaker_labels[i]['speaker'])+':'+final_transcripts[i]['alternatives'][0]['transcript']+'\n'))
        t_file2.write(final_transcripts[i]['alternatives'][0]['transcript']+'\n')
    t_file1.close()
    t_file2.close()
    return transcript_file





#a-audio file name
def transcription(a):
    # Initialize objects

    filename = 'static/results/JSON_DATA.json'
    audiofile = a


    # Initialize credentials

    speech_to_text = SpeechToTextV1(
        iam_apikey='iY6UdFrcCv7ld3elSJbvBsw_ZxbcAyiVlCi4o1Q4dM3T',
        url='https://gateway-lon.watsonplatform.net/speech-to-text/api'
    )


    """Callback class used by the recoginze_using_sockets function after receiving json response per sentence
    """
    
    class MyRecognizeCallback(RecognizeCallback):
        def __init__(self):
            RecognizeCallback.__init__(self)

        def on_connected(self):
            return

        def on_listening(self):
            return


        """Save the response JSON string in a local file named 'tran1.json' and appending ',' after every response 
        to treat the response as a list for easier access from the file"""
        
        def on_data(self, data):
            with open(filename, 'a+') as outfile:
                json.dump(data, outfile, indent=2)
            with open(filename, 'a+') as outfile:
                outfile.write(',')

        def on_hypothesis(self, hypothesis):
            return
            
        def on_error(self, error):
            print('Error received: {}'.format(error))
            print(error)

        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))

        def on_close(self):
            with open(filename,'a+') as filehandle:
                filehandle.seek(filehandle.tell()-1, os.SEEK_SET)
                filehandle.truncate()
                filehandle.write(']')

    myRecognizeCallback = MyRecognizeCallback()


    """Sends the audio file(in .wav format) through web sockets and gets the response json per sentence and stores
    them locally in a file 'JSON_DATA.json'.
    """

    with open(filename,'w') as handle:
        handle.write('[')

    with open(join(dirname(__file__), './.', audiofile), 'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(audio=audio_source,
                                                 content_type='audio/wav',
                                                 recognize_callback=myRecognizeCallback,
                                                 model='en-US_NarrowbandModel',
                                                 inactivity_timeout=10,
                                                 speaker_labels=True,
                                                 interim_results=True)

    return_file = conv_files(filename)

    return return_file, filename