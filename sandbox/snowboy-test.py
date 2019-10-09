import pyaudio

import io
import wave
import audioop
import collections
import math
import sys
import os

snowboy_location = '/Users/mdeblaauw/Desktop/lightSwitcher/snowboy_model/'
snowboy_model = '/Users/mdeblaauw/Desktop/lightSwitcher/snowboy_model/resources/models/jarvis.pmdl'

sys.path.append(snowboy_location)
import snowboydetect
sys.path.pop()

detector = snowboydetect.SnowboyDetect(
    resource_filename=os.path.join(snowboy_location, "resources", "common.res").encode(),
    model_str=",".join(snowboy_model).encode()
)