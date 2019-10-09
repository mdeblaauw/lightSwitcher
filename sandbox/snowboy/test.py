import snowboydetect
import os

TOP_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCE_FILE = os.path.join(TOP_DIR, "resources/common.res")

model_str = ",".join(["resources/models/snowboy.umdl"])

print('hi')
detector = snowboydetect.SnowboyDetect(
            resource_filename=RESOURCE_FILE.encode(), model_str=model_str.encode())

print('bla')
detector.SetAudioGain(1.0)
detector.SetSensitivity(",".join(["0.4"]).encode())