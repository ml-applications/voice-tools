#!/usr/bin/env python3

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

#input_dir_1 = '/home/bt/dev/audio-samples/conversion/trump/brandon_src/'
#input_dir_2 = '/home/bt/dev/audio-samples/conversion/trump/trump_dst/'
#output_dir_1 = './resampled/brandon'
#output_dir_2 = './resampled/trump'

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


model = sys.argv[1]

if model == 'melgan':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_for_melgan_learning/training_original',
                      '/home/bt/dev/voicecurator/ready_for_melgan_learning/training',
                      OUTPUT_RATE)

  downsample_wav_files('/home/bt/dev/voicecurator/ready_for_melgan_learning/validation_original',
                      '/home/bt/dev/voicecurator/ready_for_melgan_learning/validation',
                      OUTPUT_RATE)

elif model == 'glow_tts':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_for_transfer_learning/wav_original',
                      '/home/bt/dev/voicecurator/ready_for_transfer_learning/wav',
                      OUTPUT_RATE)
elif model == 'melgan':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_for_melgan_learning/original/training',
                      '/home/bt/dev/voicecurator/ready_for_melgan_learning/training',
                      OUTPUT_RATE)
  downsample_wav_files('/home/bt/dev/voicecurator/ready_for_melgan_learning/original/validation',
                      '/home/bt/dev/voicecurator/ready_for_melgan_learning/validation',
                      OUTPUT_RATE)
elif model == 'reagan':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_reagan/wav_original',
                      '/home/bt/dev/voicecurator/ready_reagan/wav',
                      OUTPUT_RATE)
elif model == 'oliver':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_oliver/wav_original',
                      '/home/bt/dev/voicecurator/ready_oliver/wav',
                      OUTPUT_RATE)
elif model == 'queen':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_queen/wav_original',
                      '/home/bt/dev/voicecurator/ready_queen/wav',
                      OUTPUT_RATE)
elif model == 'mario':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_mario/wav_original',
                      '/home/bt/dev/voicecurator/ready_mario/wav',
                      OUTPUT_RATE)
elif model == 'billgates':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_billgates/wav_original',
                      '/home/bt/dev/voicecurator/ready_billgates/wav',
                      OUTPUT_RATE)
elif model == 'zuckerberg':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_zuckerberg/wav_original',
                      '/home/bt/dev/voicecurator/ready_zuckerberg/wav',
                      OUTPUT_RATE)
elif model == 'bush':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_bush/wav_original',
                      '/home/bt/dev/voicecurator/ready_bush/wav',
                      OUTPUT_RATE)
elif model == 'danny-devito':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_danny-devito/wav_original',
                      '/home/bt/dev/voicecurator/ready_danny-devito/wav',
                      OUTPUT_RATE)
elif model == 'christopher-lee':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_christopher-lee/wav_original',
                      '/home/bt/dev/voicecurator/ready_christopher-lee/wav',
                      OUTPUT_RATE)
elif model == 'barack-obama':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_barack-obama/wav_original',
                      '/home/bt/dev/voicecurator/ready_barack-obama/wav',
                      OUTPUT_RATE)
elif model == 'betty-white':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_betty-white/wav_original',
                      '/home/bt/dev/voicecurator/ready_betty-white/wav',
                      OUTPUT_RATE)
elif model == 'dr-phil-mcgraw':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_dr-phil-mcgraw/wav_original',
                      '/home/bt/dev/voicecurator/ready_dr-phil-mcgraw/wav',
                      OUTPUT_RATE)
elif model == 'fred-rogers':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_fred-rogers/wav_original',
                      '/home/bt/dev/voicecurator/ready_fred-rogers/wav',
                      OUTPUT_RATE)
elif model == 'bill-clinton':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_bill-clinton/wav_original',
                      '/home/bt/dev/voicecurator/ready_bill-clinton/wav',
                      OUTPUT_RATE)
elif model == 'gilbert-gottfried':
  downsample_wav_files('/home/bt/dev/voicecurator/ready_gilbert-gottfried/wav_original',
                      '/home/bt/dev/voicecurator/ready_gilbert-gottfried/wav',
                      OUTPUT_RATE)
else:
  raise Exception('Wrong model specified: {}.'.format(model))


print('Done downsampling for model {}'.format(model))

