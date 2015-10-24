#!/usr/bin/python

### Control the LED strip via serial communication
# for use with serial_control.ino and serial_individual_brightness_control.ino

import pyaudio
import struct
import math
import serial
import time







#!/usr/bin/env python
# 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import struct
import wave
import pylab as pl


### Audio Sampling Constants
# nFFT = 512
nFFT = 1024
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
# RATE = 44100
RATE = 22050
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

### LED Serial Communication Constants
NUM_LEDS = 200
port = '/dev/cu.usbmodemfa131'  # usb port left-bottom (away from screen)
# port = '/dev/cu.usbmodemfd121' # usb port left-top (toward screen)
ser = serial.Serial(port, 9600)

MAX_BRIGHTNESS = 20


def normalize(collection, MAX_VALUE):
  """ Normalizes all items in collection to be in [0, MAX_VALUE] """
  """ assumes collection is linearly distributed """

  # print("collection: " + str(collection))
  max_amplitude = max(collection)
  min_amplitude = min(collection)
  # print("max: " + str(max_amplitude))
  new_collection = list()
  for i in range(len(collection)):
    item = (collection[i] - min_amplitude) / (max_amplitude - min_amplitude)
    # print("item: " + str(item))
    new_collection.append(item)
  # print("new collection: " + str(new_collection))
  # exit(-1)
  normalized = map(lambda x: (x - min_amplitude) / (max_amplitude - min_amplitude), collection)
  # exit(-1)
  print("\nnormalized: " + str(normalized))
  return map(lambda x: int(x * MAX_VALUE), normalized)

def write_leds_brightness(amplitudes):
  """ Map amplitudes to brightness for each LED. """
  """ For use with serial_individual_brightness_control.ino """

  # compress amplitudes to be NUM_LEDS wide
  buckets = [0] * NUM_LEDS
  print("num buckets: " + str(len(buckets)))
  print("num amplitudes: " + str(len(amplitudes)))
  # exit()
  freqs_per_bucket = int(math.ceil(len(amplitudes) * 1.0 / NUM_LEDS))
  print(amplitudes)
  for i in range(len(amplitudes)):
    # truncate to find current bucket
    bucket_index = i / freqs_per_bucket
    # print("bucket index: " + str(bucket_index))
    # print(amplitudes[i])
    buckets[bucket_index] = amplitudes[i]
  buckets = normalize(buckets, MAX_BRIGHTNESS)
  # print("normalized: " + str(buckets))
  print("\n\nwriting: " + str(buckets))
  # exit()
  # write instructions to microcontroler
  for i in range(NUM_LEDS):
    ser.write(str(buckets[i]))
    print("acknowledgement: " + str(ser.readline()))

def write_leds_color():
  """ For use with serial_control.ino """
  for i in range(NUM_LEDS):
      # TODO: speed up by writing bytes: ie ser.write(bytes)
      ser.write("255,00,00")
      print("acknowledgement: " + str(ser.readline()))
  # print("end")
  exit()

def get_avg_power_in_range(high, freqs, Y):
  """ [0 - high) """
  frequencies_per_index = RATE * 1.0 / nFFT # number of frequencies in each X 'bucket'
  high_index = int(high / frequencies_per_index) # 0-based
  # the real "zero" is in the middle
  start_index = len(Y) / 2 - high_index
  end_index = len(Y) / 2 + high_index
  total_power = 0
  for i in range(start_index, end_index):
    print("frequency: " + str(freqs[i]))
    print("power: " + str(Y[i]))
    total_power += Y[i]
  return total_power / (end_index - start_index)



# X goes from -XXXX to +XXXX
def get_power(stream, MAX_y):
  """ Modified from code by Yu-Jie Lin """

  data = stream.read(INPUT_FRAMES_PER_BLOCK)

  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (INPUT_FRAMES_PER_BLOCK * CHANNELS), data)) / MAX_y
  y_L = y[::2]
  y_R = y[1::2]

  Y_L = np.fft.fft(y_L, nFFT)
  Y_R = np.fft.fft(y_R, nFFT)

  # Sewing FFT of two channels together, DC part uses right channel's
  Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))

  return Y


def main():
  """ Modified from code by Yu-Jie Lin """
  p = pyaudio.PyAudio()

  # Frequency range
  x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

  # Used for normalizing signal. If use paFloat32, then it's already -1..1.
  # Because of saving wave, paInt16 will be easier.
  MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)
  
  try:
    while(True):
      try:
        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=BUF_SIZE)
        Y = get_power(stream, MAX_y)
        # pl.plot(x_f, Y)
        # pl.xlabel("Frequency(Hz)")
        # pl.ylabel("Power(dB)")
        # pl.show()
        print("Y: " + str(Y[:50]))
        print("Y end: " + str(Y[len(Y) - 50:-1]))
        write_leds_brightness(Y)

        # print("power in low interval: " + str(get_avg_power_in_range(100, x_f, Y)))
      except IOError, e:
        print("Error recording: %s"%e)
  except KeyboardInterrupt:
    print("received KeyboardInterrupt. Cleaning up and exiting")
    stream.stop_stream()
    stream.close()
    p.terminate()
    return


if __name__ == '__main__':
    # clear anything in the buffer
    ser.flushInput()
    ser.flushOutput()   

    # Arduino resets when new serial connection is opened, so wait
    # for this process to complete
    time.sleep(3)

    # while(True):
    #     write_leds()
    
    main()
  
