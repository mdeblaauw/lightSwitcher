import wave

from functions.source import Microphone
from functions.listen_pipeline import Recogniser
from functions.snowboy_app import SnowboyApp

rc = Recogniser()
sb = SnowboyApp("computer.umdl")
#print(dir(kl))
with Microphone() as source:
    rc.adjust_for_ambient_noise(source, duration=1)
    audio = rc.listen(source, sb)
    print('bla')

#record audio
#wv = audio.get_wav_data()
#with open('bla.wav', 'wb') as output:
#    output.write(wv)