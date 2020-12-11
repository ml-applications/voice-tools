#!/usr/bin/env python3
"""
Rename the wav files in a directory to contain a prefix.

Eg, to rename with the "foo_" prefix,

  d7c60bc7ec91b381cb798baa66259887728833792c79b3de3aafde0da22a2381.wav  ->  foo_d7c60bc7ec91b381cb798baa66259887728833792c79b3de3aafde0da22a2381.wav
  d8dacf4e73b263c30b0c7e1bef1153d2762e60a816498c1ecf61bb24abad6afc.wav  ->  foo_d8dacf4e73b263c30b0c7e1bef1153d2762e60a816498c1ecf61bb24abad6afc.wav
  e033d28a9eecf9d9b725ed74b8720647c21a00608e884cc46578f60481469295.wav  ->  foo_e033d28a9eecf9d9b725ed74b8720647c21a00608e884cc46578f60481469295.wav
  e2f4b4828c1c831c62dad6190bd8404b9ea92512235a0797b83453dfa8a1f19c.wav  ->  foo_e2f4b4828c1c831c62dad6190bd8404b9ea92512235a0797b83453dfa8a1f19c.wav

"""

import argparse
import os
import time

def rename_wav_files(input_dir, prefix):
    for i, name in enumerate(os.listdir(input_dir)):
        if i % 100 == 0:
          time.sleep(0.1) # So we can interrupt

        old_filepath = os.path.join(input_dir, name)

        if not os.path.isfile(old_filepath) \
                or not name.endswith(".wav"):
            continue

        if name.startswith(prefix):
            continue # We're already done. Don't double prefix.

        print('Processing {}: {}'.format(i, name))

        new_name = f"{prefix}{name}"

        new_filepath = os.path.join(input_dir, new_name)

        if os.path.exists(new_filepath):
            print(f'A file with that name already exists: {new_name}')
            continue

        #print(f'{old_filepath} -> {new_filepath}')
        print(f'{name} -> {new_name}')
        os.rename(old_filepath, new_filepath)

def parse_args():
  parser = argparse.ArgumentParser('Rename all the wav files to include a prefix')
  parser.add_argument('--input_directory', type=str, required=True)
  parser.add_argument('--prefix', type=str, required=True)
  return parser.parse_args()

args = parse_args()

print('Input directory: {}'.format(args.input_directory))
print('Prefix : {}'.format(args.prefix))

rename_wav_files(args.input_directory, args.prefix)

print('Done renaming')
