# https://medium.com/slanglabs/how-to-build-python-transcriber-using-mozilla-deepspeech-5485b8d234cf
# https://medium.com/slanglabs/automatic-speech-recognition-in-python-programs-a64851ad29b3

import deepspeech
import numpy as np
import os
import pyaudio
import time

# DeepSpeech parameters
MODEL_FILE_PATH = './deepspeech-0.9.3-models.pbmm'
BEAM_WIDTH = 500
LM_ALPHA = 0.75
LM_BETA = 1.85

# Make DeepSpeech Model
model = deepspeech.Model(MODEL_FILE_PATH)

# Create a Streaming session
context = model.createStream()
model.setScorerAlphaBeta(alpha=LM_ALPHA,beta=LM_BETA)
# Encapsulate DeepSpeech audio feeding into a callback for PyAudio
text_so_far = ''
def process_audio(in_data, frame_count, time_info, status):
    global text_so_far
    data16 = np.frombuffer(in_data, dtype=np.int16)
    context.feedAudioContent(data16)
    text = context.intermediateDecode()
    if text != text_so_far:
        print('Interim text = {}'.format(text))
        text_so_far = text
    return (in_data, pyaudio.paContinue)

# PyAudio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Feed audio to deepspeech in a callback to PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
    stream_callback=process_audio
)

print('Please start speaking, when done press Ctrl-C ...')
stream.start_stream()

try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    # PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print('Finished recording.')
    # DeepSpeech
    text = context.finishStream()
    print('Final text = {}'.format(text))
