#!/usr/bin/env python
# Modified from code by Yu-Jie Lin

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import struct
import wave
import pylab as pl


# nFFT = 512
nFFT = 1024
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
# RATE = 44100
RATE = 22050
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

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

  # Read n*nFFT frames from stream, n > 0
  # N = max(stream.get_read_available() / nFFT, 1) * nFFT
  # data = stream.read(N)
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
        pl.plot(x_f, Y)
        pl.xlabel("Frequency(Hz)")
        pl.ylabel("Power(dB)")
        pl.show()
        print("power in low interval: " + str(get_avg_power_in_range(100, x_f, Y)))
      except IOError, e:
        print("Error recording: %s"%e)
  except KeyboardInterrupt:
    print("received KeyboardInterrupt. Cleaning up and exiting")
    stream.stop_stream()
    stream.close()
    p.terminate()
    return


if __name__ == '__main__':
  main()
  
