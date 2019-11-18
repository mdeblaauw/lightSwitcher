import wave

import boto3
import functions

bot_name = 'lightSwitchBot'
bot_alias = '$LATEST'
user_id = '123456789'
content_type = 'audio/l16; rate=16000; channels=1'

rc = functions.Recogniser()
sb = functions.SnowboyApp("computer.umdl")

def pipeline():
    with functions.Microphone(device_index=2) as source:
        rc.adjust_for_ambient_noise(source, duration=1)
        audio = rc.listen(source, sb)
    try:
        response = rc.lex_recognise(audio,bot_name,bot_alias,user_id,content_type)
        print('You said: ' + response['inputTranscript'] + '\n')
        print(response['message'])
        print('Intent classified as ' + response['intentName'])
        command = response['intentName']
    except Exception as e:
        print(e)
        command = pipeline()

    return(command)

def assistant(command):
    print('execute commands')

while True:
    assistant(pipeline())
