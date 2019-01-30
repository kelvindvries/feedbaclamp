import pyaudio
import numpy
import spl_lib as spl
from scipy.signal import lfilter
import connect_database

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


def mic(error_count=0):
    # This listens to incoming sound, processes the sound, returns db and sends it to the database.
    print("Listening")
    while True:
        try:
            # read() returns string. You need to decode it into an array later.
            block = stream.read(CHUNK)
        except IOError as e:
            error_count += 1
            print(" (%d) Error recording: %s" % (error_count, e))
        else:
            # Int16 is a numpy data type which is Integer (-32768 to 32767)
            # If you put Int8 or Int32, the result numbers will be ridiculous
            decoded_block = numpy.fromstring(block, 'Int16')
            # This is where you apply A-weighted filter
            y = lfilter(NUMERATOR, DENOMINATOR, decoded_block)
            new_decibel = 20 * numpy.log10(spl.rms_flat(y))
            # print('A-weighted: {:+.2f} dB'.format(new_decibel))
            if new_decibel > 50:
                print (new_decibel)
                connect_database.insert_feedbacklamp(new_decibel, connect_database.get_date(),
                                                     connect_database.get_time())

    stream.stop_stream()
    stream.close()
    pa.terminate()


if __name__ == ("__main__"):
    # This starts the listen function
    mic()
