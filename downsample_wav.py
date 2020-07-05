#!/usr/bin/env python3

import argparse
import librosa
import numpy as np
import os
import scipy
import shutil
import sys
import time

"""
Testing LJS Resample
--------------------

+ (python) bt@halide:~/dev/voice-tools$ aplay test_input.wav
Playing WAVE 'test_input.wav'
    : Signed 16 bit Little Endian, Rate 22050 Hz, Mono

+ (python) bt@halide:~/dev/voice-tools$ aplay test_output.wav
Playing WAVE 'test_output.wav'
    : Float 32 bit Little Endian, Rate 16000 Hz, Mono


Signed 16 bit --> Float 32 bit

WaveRNN
-------

aplay model_outputs/mel-northandsouth_52_f000076.wav
Playing WAVE 'model_outputs/mel-northandsouth_52_f000076.wav'
    : Float 32 bit Little Endian, Rate 16000 Hz, Mono

aplay model_outputs/mel-LJ001-0109.npy_orig.wav
Playing WAVE 'model_outputs/mel-LJ001-0109.npy_orig.wav'
    : Float 32 bit Little Endian, Rate 22050 Hz, Mono

Everything in ML is Float 32 bit?

"""

OUTPUT_RATE = 22050

def check_directories(dir_input, dir_output):
    if not os.path.exists(dir_input):
        sys.exit('Error: Input directory does not exist: {}'.format(dir_input))
    if not os.path.exists(dir_output):
        sys.exit('Error: Output directory does not exist: {}'.format(dir_output))
    abs_a = os.path.abspath(dir_input)
    abs_b = os.path.abspath(dir_output)
    if abs_a == abs_b:
        sys.exit('Error: Paths are the same: {}'.format(abs_a))

def resample_file(input_filename, output_filename, sample_rate):
    mono = True # librosa converts signal to mono by default, so I'm just surfacing this
    audio, existing_rate = librosa.load(input_filename, sr=sample_rate, mono=mono)

    #if existing_rate == sample_rate:
    #  print(' - File {} already at sample rate of {}'.format(input_file, sample_rate))
    #  if not os.path.exists(output_filename):
    #    # Skip copy if we've already done it.
    #    print(' - Copying {} to {}'.format(input_file, output_file))
    #    shutil.copy(input_filename, output_filename)
    #  return

    # librosa can't write int16
    #librosa.output.write_wav(output_filename, audio, sr=sample_rate)

    # Scale audio to the range of 16 bit PCM
    # https://stackoverflow.com/a/52757235
    #print(' - Downsampling {} to {}'.format(existing_rate, sample_rate))
    audio /= 1.414 # Scale to [-1.0, 1.0]
    audio *= 32767 # Scale to int16
    audio = audio.astype(np.int16)
    scipy.io.wavfile.write(output_filename, sample_rate, audio)

def downsample_wav_files(input_dir, output_dir, output_sample_rate):
    check_directories(input_dir, output_dir)

    for i, name in enumerate(os.listdir(input_dir)):
        if i % 100 == 0:
          time.sleep(0.1) # So we can interrupt
        input_filename = os.path.join(input_dir, name)

        if not os.path.isfile(input_filename) \
                or not name.endswith(".wav"):
            continue

        output_filename = os.path.join(output_dir, name)

        print('Processing {}: {}'.format(i, name))
        resample_file(input_filename, output_filename, output_sample_rate)


def parse_args():
  parser = argparse.ArgumentParser('Split audio into ingestible chunks')
  parser.add_argument('--input_directory', type=str, required=True)
  parser.add_argument('--output_directory', type=str, required=True)
  return parser.parse_args()

args = parse_args()

print('Input directory: {}'.format(args.input_directory))
print('Output directory: {}'.format(args.output_directory))

downsample_wav_files(args.input_directory, args.output_directory, OUTPUT_RATE)

print('Done downsampling')

