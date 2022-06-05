from os import environ, path
import pyaudio
from pocketsphinx import get_model_path
from timeit import default_timer as timer

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = get_model_path()

config = Decoder.default_config()
config.set_string('-logfn','nul')

config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))


decoder = Decoder(config)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
while True:
    start = timer()
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                print ('Result:', decoder.hyp().hypstr)
                print(format(timer() - start, '.2f') + ' sec')
                decoder.start_utt()
    else:
        break
decoder.end_utt()