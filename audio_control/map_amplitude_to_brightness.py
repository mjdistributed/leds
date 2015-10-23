#!/usr/bin/python

# open a microphone in pyAudio and listen for taps

import pyaudio
import struct
import math
import serial
import time

# DELTA_THRESHOLD = 0.02
RATIO_THRESHOLD = 1.1
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
# RATE = 44100  
RATE = 22050
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0            
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120 
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

NUM_SAMPLES_TO_AVERAGE = 2000

MIN_BRIGHTNESS = 1
MAX_BRIGHTNESS = 20

port = '/dev/cu.usbmodemfa131'  # usb port left-bottom (away from screen)
ser = serial.Serial(port, 9600)

# port = '/dev/cu.usbmodemfd121' # usb port left-top (toward screen)

mid_brightness = (MAX_BRIGHTNESS + MIN_BRIGHTNESS) / 2

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class Listener(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0
        self.total_amplitude = 0
        self.average_amplitude = 0
        self.num_samples = 0
        self.brightness = mid_brightness

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def get_brightness(self, amplitude):
        brightness = self.brightness
        if amplitude / self.average_amplitude > RATIO_THRESHOLD:
            # noisy block            
            brightness = mid_brightness + int(mid_brightness * (1 - self.average_amplitude / amplitude))
        elif self.average_amplitude / amplitude > RATIO_THRESHOLD:
            brightness = mid_brightness - int(mid_brightness * (1 - amplitude / self.average_amplitude))
        return brightness

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            # dammit. 
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        self.total_amplitude += amplitude
        self.num_samples += 1
        self.average_amplitude = self.total_amplitude / self.num_samples
        if(self.num_samples > NUM_SAMPLES_TO_AVERAGE):
            self.num_samples = 0
            self.total_amplitude = self.average_amplitude

        self.brightness = self.get_brightness(amplitude)
        ser.write(str(self.brightness) + "\n")

if __name__ == "__main__":
    tt = Listener()

    while(True):
        tt.listen()