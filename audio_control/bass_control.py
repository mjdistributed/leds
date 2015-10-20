#!/usr/bin/python

# open a microphone in pyAudio and listen for taps

import pyaudio
import struct
import math
import serial
import pylab as pl
import numpy as np

# DELTA_THRESHOLD = 0.02
RATIO_THRESHOLD = 1.1
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0            
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120 
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

NUM_SAMPLES_TO_AVERAGE = 1000

# port = '/dev/cu.usbmodemfa131'  # usb port left-bottom (away from screen)
# ser = serial.Serial(port, 9600)
# port = '/dev/cu.usbmodemfd121' # usb port left-top (toward screen)


def plot_test(block):
    count = len(block)/2
    format = "%dh"%(count)
    print("format: " + format)
    data = np.array(list(struct.unpack(format, block)))
    time = np.arange(len(data))*1.0/RATE
    pl.plot(time, data)
    pl.show()

def frequency_analysis(block):
    count = len(block)/2
    format = "%dh"%(count)
    print("format: " + format)
    data = np.array(list(struct.unpack(format, block)))
    data_Left = data[::2]
    data_Right = data[1::2]
    power = 20*np.log10(np.abs(np.fft.rfft(data_Left[:2048])))
    frequency = np.linspace(0, RATE/2.0, len(power))
    pl.plot(frequency, power)
    pl.xlabel("Frequency(Hz)")
    pl.ylabel("Power(dB)")
    pl.show()

def get_power_for_frequency(block, low_freq, high_freq):
    count = len(block)/2
    format = "%dh"%(count)
    data = np.array(list(struct.unpack(format, block)))
    data_Left = data[::2]
    data_Right = data[1::2]
    power = 20*np.log10(np.abs(np.fft.rfft(data_Left)))
    frequency = np.linspace(0, RATE/2.0, len(power))
    # print(len(power))
    # print(len(frequency))
    total_power = 0
    count = 0
    for i in range(0, len(frequency)):
        if(frequency[i] >= low_freq and frequency[i] <= high_freq):
            # print("here: " + str(frequency[i]))
            total_power += power[i]
            count += 1
        elif(frequency[i] > high_freq):
            break
    return (total_power * 1.0 / count)

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    print("format: " + format)
    shorts = struct.unpack( format, block )

    # print("shorts: " + str(shorts))
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

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            # dammit. 
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return
        # amplitude = get_rms( block )

        frequency_analysis(block)
        amplitude = get_power_for_frequency(block, 430, 450)
        return
        # print("found amplitude: " + str(amplitude))

        self.total_amplitude += amplitude
        self.num_samples += 1
        self.average_amplitude = self.total_amplitude / self.num_samples
        if(self.num_samples > NUM_SAMPLES_TO_AVERAGE):
            self.num_samples = 0
            self.total_amplitude = self.average_amplitude
        print("average amplitude: " + str(self.average_amplitude))

        print("amplitude: " + str(amplitude))
        # print("threshold: " + str(self.threshold))

        # if amplitude / self.average_amplitude > RATIO_THRESHOLD: #DELTA_THRESHOLD:
            # noisy block
            # ser.write("20" + "\n")    
        
        # else:            
            # quiet block.
            # ser.write("0" + "\n")

if __name__ == "__main__":
    tt = Listener()

    while(True):
        tt.listen()