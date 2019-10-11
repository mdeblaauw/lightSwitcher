import time
import math
import os
import collections
import audioop

from .snowboy.snowboydetect import SnowboyDetect

class SnowboyApp():
    def __init__(self, model, audioGain=1.0, sensitivity="0.6", applyFrontend=True):
        TOP_DIR = os.path.dirname(os.path.abspath(__file__))
        RESOURCE_FILE = os.path.join(TOP_DIR, "snowboy/resources/common.res")
        model_str = ",".join([os.path.join("functions/snowboy/resources/models/", model)])

        self.detector = SnowboyDetect(RESOURCE_FILE.encode(), model_str=model_str.encode())

        self.detector.SetAudioGain(audioGain)
        self.detector.SetSensitivity(",".join([sensitivity]).encode())
        self.detector.ApplyFrontend(applyFrontend)

    def snowboy_hot_word(self,source):
        #assert isinstance(source, Microphone), "Source must be a Microphone source"

        snowboy_sample_rate = self.detector.SampleRate()
        seconds_per_buffer = float(source.CHUNK)/source.SAMPLE_RATE
        resampling_state = None
        
        five_seconds_buffer_count = int(math.ceil(2/seconds_per_buffer))
        half_second_buffer_count = int(math.ceil(0.5/seconds_per_buffer))
        
        frames = collections.deque(maxlen=five_seconds_buffer_count)
        resampled_frames = collections.deque(maxlen=half_second_buffer_count)
        
        check_interval = 0.05
        last_check = time.time()
        while True:
            #elapsed_time += seconds_per_buffer
            
            buffer = source.stream.read(source.CHUNK)
            frames.append(buffer)
            
            resampled_buffer, resampling_state = audioop.ratecv(buffer, source.SAMPLE_WIDTH, 1, source.SAMPLE_RATE, snowboy_sample_rate, resampling_state)
            resampled_frames.append(resampled_buffer)
            
            if time.time() - last_check > check_interval:
                snowboy_result = self.detector.RunDetection(b"".join(resampled_frames))
                if snowboy_result > 0:
                    print("hot word detected")
                    break;
                resampled_frames.clear()
                last_check = time.time()
                
        return b"".join(frames)