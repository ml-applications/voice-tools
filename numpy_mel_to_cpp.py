#!/usr/bin/env python3

"""
The C++ vocoder in WaveRNN-Pytorch [1] can be built as a
python extension or standalone binary. When used as the latter,
it expects raw mel files to follow a simple format. We convert
numpy matrices to that format here.

    struct Header{
        int nRows, nCols;
    } header;

    fread( &header, sizeof( Header ), 1, fd);

    Matrixf mel( header.nRows, header.nCols );
    fread(mel.data(), sizeof(float), header.nRows*header.nCols, fd);

[1] https://github.com/geneing/WaveRNN-Pytorch
"""

import struct
import numpy as np

def numpy_to_raw_mel(input_file, output_file):
    mel = np.load(input_file).T
    (rows, cols) = mel.shape

    print("Rows: {}, Cols: {}".format(rows, cols))

    buf = []
    buf.append(struct.pack('<i', rows))
    buf.append(struct.pack('<i', cols))

    for i in range(rows):
        for j in range(cols):
            data = mel[i][j]
            buf.append(struct.pack('<f', data))

    with open(output_file, 'wb') as f:
        for b in buf:
            f.write(b)

input_file = '/home/bt/dev/2nd/Tacotron-2/training_data/mels/mel-LJ001-0109.npy'

numpy_to_raw_mel(input_file, 'output.cppmel')

