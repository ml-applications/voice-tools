#!/usr/bin/env python3

"""
This is meant to partition VCTK for multi-speaker Melgan training.
Some speakers have fewer samples (172 minimum) wheras others have more (503 maximum).
"""

import os
import pathlib
import random
import shutil
import sys

OUTPUT_DIRECTORY = './output_vctk_melgan'

def main(vctk_directory, training_directory, validation_directory):
    wav_directory = os.path.join(vctk_directory, 'wav48')
    print(wav_directory)

    total_training_samples = 0
    total_validation_samples = 0

    for entry in os.listdir(wav_directory):
        directory = os.path.join(wav_directory, entry)
        if not os.path.isdir(directory):
            continue

        print('Partitioning VCTK speaker: {}'.format(entry))

        wav_files = get_directory_wav_files(directory)

        total_samples = len(wav_files)
        validation_samples = int(total_samples * 0.15)
        training_samples = total_samples - validation_samples

        total_training_samples += training_samples
        total_validation_samples += validation_samples

        validation_wav_files = random.sample(wav_files, validation_samples)
        training_wav_files = [wav_file for wav_file in wav_files if wav_file not in validation_wav_files]

        copy_files(validation_wav_files, validation_directory)
        copy_files(training_wav_files, training_directory)

    print('total training files:', total_training_samples)
    print('total validation files:', total_validation_samples)


def get_directory_wav_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.wav')]


def copy_files(file_list, destination_directory):
    for file in file_list:
        shutil.copy(file, destination_directory)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Must supply directory of vctk data set')

    if not os.path.isdir(OUTPUT_DIRECTORY):
        raise Exception('Output directory does not exist: {}'.format(OUTPUT_DIRECTORY))

    training_dir = os.path.join(OUTPUT_DIRECTORY, 'training')
    validation_dir = os.path.join(OUTPUT_DIRECTORY, 'validation')

    pathlib.Path(training_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(validation_dir).mkdir(parents=True, exist_ok=True)

    main(sys.argv[1], training_dir, validation_dir)
