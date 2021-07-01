# https://medium.com/slanglabs/how-to-build-python-transcriber-using-mozilla-deepspeech-5485b8d234cf
# https://medium.com/slanglabs/automatic-speech-recognition-in-python-programs-a64851ad29b3

import deepspeech
import numpy as np
import os
import pyaudio
import time

# DeepSpeech parameters
MODEL_FILE_PATH = "./deepspeech-0.9.3-models.pbmm"
BEAM_WIDTH = 500
LM_ALPHA = 0.75
LM_BETA = 1.85

# Make DeepSpeech Model
model = deepspeech.Model(MODEL_FILE_PATH)
model.setScorerAlphaBeta(alpha=LM_ALPHA, beta=LM_BETA)


# PyAudio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Feed audio to deepspeech in a callback to PyAudio

#
# try:
#     while stream.is_active():
#         time.sleep(0.1)
# except KeyboardInterrupt:
#     # PyAudio
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
#     print("Finished recording.")
#     # DeepSpeech
#     text = context.finishStream(context)
#     print("Final text = {}".format(text))


class AudioChannel:
    def __init__(self):
        # Create a Streaming session
        self.context = model.createStream()
        # Encapsulate DeepSpeech audio feeding into a callback for PyAudio
        self.text_so_far = ""

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=self.return_audio,
        )
        self.data_raw = []
        self.stream.start_stream()
        self.text_so_far = ''

    def return_audio(self, in_data, frame_count, time_info, status):
        self.data_raw.append(in_data)
        return (in_data, pyaudio.paContinue)

    def recognize_audio(self, in_data):
        data16 = np.frombuffer(in_data, dtype=np.int16)
        self.context.feedAudioContent(data16)
        text = self.context.intermediateDecode()
        if text != self.text_so_far:
            print("Interim text = {}".format(text))
            self.text_so_far = text
        return (in_data, pyaudio.paContinue)
