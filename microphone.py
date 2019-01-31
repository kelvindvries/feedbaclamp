import pyaudio
import numpy
import spl_lib as spl
from scipy.signal import lfilter
import connect_database
import RPi.GPIO as GPIO

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

            red_limit = 50
            leds = [18, 11, 13, 15, 16]

            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(leds, GPIO.OUT)

            if new_decibel >= red_limit - 40:
                GPIO.output(leds[0], True)
                print("Onder limiet")
            else: GPIO.output(leds[0], False)

            if new_decibel >= red_limit - 30:
                GPIO.output(leds[1], True)
                print("onder 20 db")
            else: GPIO.output(leds[1], False)

            if new_decibel >= red_limit - 20:
                print ('onder 30db')
                GPIO.output(leds[2], True)
            else: GPIO.output(leds[2], False)

            if new_decibel >= red_limit - 10:
                print ('onder 40 db')
                GPIO.output(leds[3], True)
            else: GPIO.output(leds[3], False)

            if new_decibel > red_limit:
                GPIO.output(leds[4], True)
                print("Red")
            else: GPIO.output(leds[4], False)

            # print('A-weighted: {:+.2f} dB'.format(new_decibel)) and end db to database
            if new_decibel > red_limit:
                print (new_decibel)
                connect_database.insert_feedbacklamp(new_decibel, connect_database.get_date(),
                                                     connect_database.get_time())

            GPIO.cleanup()

    stream.stop_stream()
    stream.close()
    pa.terminate()


if __name__ == ("__main__"):
    # This starts the listen function
    mic()
