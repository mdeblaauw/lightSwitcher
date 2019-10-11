import pyaudio

class Microphone():
    def __init__(self, device_index=0, sample_rate=None, chunk_size=1024):
        self.audio = pyaudio.PyAudio()
        assert self.audio.get_device_count() >= 0, 'no sources detected'

        self.device_index = device_index

        if sample_rate is None:
            device_info = self.audio.get_device_info_by_index(self.device_index)
            sample_rate = int(device_info["defaultSampleRate"])

        self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
        self.SAMPLE_RATE = sample_rate
        self.CHUNK = chunk_size

    def __enter__(self):
        try:
            self.stream = Microphone.MicrophoneStream(
                self.audio.open(
                    input_device_index=self.device_index, channels=1, format=self.format,
                    rate=self.SAMPLE_RATE, frames_per_buffer=self.CHUNK, input=True,
                )
            )
        except Exception:
            self.audio.terminate()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.stream.close()
        finally:
            self.stream = None
            self.audio.terminate()

    class MicrophoneStream(object):
        def __init__(self, pyaudio_stream):
            self.pyaudio_stream = pyaudio_stream

        def read(self, size):
            return self.pyaudio_stream.read(size, exception_on_overflow=False)

        def close(self):
            try:
                # sometimes, if the stream isn't stopped, closing the stream throws an exception
                if not self.pyaudio_stream.is_stopped():
                    self.pyaudio_stream.stop_stream()
            finally:
                self.pyaudio_stream.close()