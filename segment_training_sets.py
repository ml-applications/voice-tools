#!/usr/bin/env python3

import os
import re
import shutil
import sys

HOLD_FOR_TEST  = 0.2

src_voice_dir = './resampled/brandon'
dst_voice_dir = './resampled/trump'

src_training_dir = './ready/brandon/training'
src_testing_dir = './ready/brandon/test'

dst_training_dir = './ready/trump/training'
dst_testing_dir = './ready/trump/test'

# TODO: Output dirs originate by convention
# TODO: Check none of the directories is the same

NAMING_SCHEME = re.compile(r'(?P<name>[0-9A-Za-z]+)_(?P<date>\d{4}_\d{2}_\d{2})-(?P<sample>\d{3})-?(?P<variant>\d{3})?\.wav')

SKIP_SETS = set([
    '2018_02_15', # These sound 'acted' and fake.
])

def check_directories_not_same(dir_input, dir_output):
    if not os.path.exists(dir_input):
        sys.exit('Error: Input directory does not exist: {}'.format(dir_input))
    if not os.path.exists(dir_output):
        sys.exit('Error: Output directory does not exist: {}'.format(dir_output))
    abs_a = os.path.abspath(dir_input)
    abs_b = os.path.abspath(dir_output)
    if abs_a == abs_b:
        sys.exit('Error: Paths are the same: {}'.format(abs_a))

def count_wavs_in_directory(directory):
    num_wavs = 0
    for _i, name in enumerate(os.listdir(directory)):
        filename = os.path.join(directory, name)
        if os.path.isfile(filename) and name.endswith(".wav"):
            num_wavs += 1
    return num_wavs

def find_filename_to_duplicate(source_filename):
    """
    In the event I was too lazy to create *-002.wav, etc. files, find a file to copy.
    """
    matches = NAMING_SCHEME.match(source_filename)
    if not matches:
        return
    name = matches.group('name')
    date = matches.group('date')
    sample = matches.group('sample')
    variant = matches.group('variant')
    return {
        'from': '{}_{}-{}-001.wav'.format(name, date, sample),
        'to': '{}_{}-{}-{}.wav'.format(name, date, sample, variant),
    }

def check_same_files_between_dirs(dir_a, dir_b):
    def do_check(dir_a, dir_b):
        for i, name in enumerate(sorted(os.listdir(dir_a))):
            check_filename = os.path.join(dir_b, name)
            if not os.path.exists(check_filename):
                print('File {} exists in dir {}, but file does not exist in dir {}'.format(name, dir_a, dir_b))
    do_check(dir_a, dir_b)
    do_check(dir_b, dir_a)

def should_skip(source_filename):
    matches = NAMING_SCHEME.match(source_filename)
    if not matches:
        return True
    if matches['date'] in SKIP_SETS:
        return True
    return False

# === Plan & Mutation Bits ===

num_src_wavs = count_wavs_in_directory(src_voice_dir)
num_dst_wavs = count_wavs_in_directory(dst_voice_dir)

print('{} source speaker wavs, {} destination speaker wavs'.format(num_src_wavs, num_dst_wavs))

prelim_num_test = int(num_src_wavs * HOLD_FOR_TEST)

print('Original num total: {}'.format(num_src_wavs))
print('Prelim num for training: {}'.format(num_src_wavs - prelim_num_test))
print('Prelim num for test: {}'.format(prelim_num_test))

actual_num_src_wavs = 0
skipped_wavs = 0

for i, name in enumerate(sorted(os.listdir(src_voice_dir))):
    if should_skip(name):
        skipped_wavs += 1
    else:
        actual_num_src_wavs += 1

actual_num_test = int(actual_num_src_wavs * HOLD_FOR_TEST)
actual_withold_for_test = actual_num_src_wavs // actual_num_test

print('Skipped wavs: {}'.format(skipped_wavs))
print('Actual num total: {}'.format(actual_num_src_wavs))
print('Actual num for training: {}'.format(actual_num_src_wavs - actual_num_test))
print('Actual num for test: {}'.format(actual_num_test))

duplicated_count = 0

for i, name in enumerate(sorted(os.listdir(src_voice_dir))):
    # We treat source as authoratative, even though destination is the original speaker.
    # There may be extra 'source' samples.
    full_src_path = os.path.join(src_voice_dir, name)
    full_dst_path = os.path.join(dst_voice_dir, name)

    if should_skip(name):
        continue

    duplicate_plan = None
    if not os.path.exists(full_dst_path):
        # In the event I was too lazy to create *-002.wav, etc. files, lazily do so here.
        duplicate_plan = find_filename_to_duplicate(name)
        if not duplicate_plan:
            print('Cannot find duplicate for {}'.format(full_dst_path))
            continue
        else:
            duplicated_count += 1

    if i % actual_withold_for_test == 0:
        shutil.copy(full_src_path, src_testing_dir)
        if not duplicate_plan:
            shutil.copy(full_dst_path, dst_testing_dir)
        else:
            from_ = os.path.join(dst_voice_dir, duplicate_plan['from'])
            to = os.path.join(dst_testing_dir, duplicate_plan['to'])
            shutil.copy(from_, to)
    else:
        shutil.copy(full_src_path, src_training_dir)
        if not duplicate_plan:
            shutil.copy(full_dst_path, dst_training_dir)
        else:
            from_ = os.path.join(dst_voice_dir, duplicate_plan['from'])
            to = os.path.join(dst_training_dir, duplicate_plan['to'])
            shutil.copy(from_, to)

# === Validation Step ===

print('Duplicated Destination Speaker Count: {}'.format(duplicated_count))

check_same_files_between_dirs(src_training_dir, dst_training_dir)
check_same_files_between_dirs(src_testing_dir, dst_testing_dir)

