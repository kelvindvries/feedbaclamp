import pyaudio
import numpy
import spl_lib as spl
from scipy.signal import lfilter

CHUNKS = [4096, 9600]  # Use what you need
CHUNK = CHUNKS[1]
FORMAT = pyaudio.paInt16  # 16 bit
CHANNEL = 1  # 1 means mono. If stereo, put 2
RATES = [44300, 48000]  # Mics have different refresh rates
RATE = RATES[1]

NUMERATOR, DENOMINATOR = spl.A_weighting(RATE)
'''
Listen to mic
'''
pa = pyaudio.PyAudio()

stream = pa.open(format=FORMAT,
                 channels=CHANNEL,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)


def is_meaningful(old, new):
    return abs(old - new) > 3


def listen(old=0, error_count=0, min_decibel=50, max_decibel=0):
    print("Listening")
    while True:
        try:
            ## read() returns string. You need to decode it into an array later.
            block = stream.read(CHUNK)
        except IOError as e:
            error_count += 1
            print(" (%d) Error recording: %s" % (error_count, e))
        else:
            ## Int16 is a numpy data type which is Integer (-32768 to 32767)
            ## If you put Int8 or Int32, the result numbers will be ridiculous
            decoded_block = numpy.fromstring(block, 'Int16')
            ## This is where you apply A-weighted filter
            y = lfilter(NUMERATOR, DENOMINATOR, decoded_block)
            new_decibel = 20 * numpy.log10(spl.rms_flat(y))
            if is_meaningful(old, new_decibel):
                old = new_decibel
                print('A-weighted: {:+.2f} dB'.format(new_decibel))
                max_decibel = max_decibel

    stream.stop_stream()
    stream.close()
    pa.terminate()

listen()