#!/usr/bin/env python3

import subprocess
import os

INPUT_DIRECTORY = './wavs_original/'
OUTPUT_DIRECTORY = './wavs/'

# original, original, output
command_template = 'sox {} temp/noise.wav synth whitenoise vol 0.001 && sox {} temp/transformed.wav pitch 700  reverb 2 && sox -m temp/transformed.wav temp/noise.wav {}'

for i, name in enumerate(sorted(os.listdir(INPUT_DIRECTORY))):
  input_file = os.path.join(INPUT_DIRECTORY, name)
  output_file = os.path.join(OUTPUT_DIRECTORY, name)
  command = command_template.format(input_file, input_file, output_file)
  subprocess.call(command, shell=True)
