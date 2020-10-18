from PIL import Image, ImageDraw

def render_histogram(wav, filename='histograms/output.png', row_index=None, col_index=None):
    dimensions = wav.shape
    print('>>> Tensor Image input size: {}'.format(dimensions))

    wav_signal = None
    rows = -1
    cols = -1
    if row_index is not None and col_index is not None:
        rows = dimensions[row_index]
        cols = dimensions[col_index]
        wav_signal = wav
    else:
        # Remove 1-sized dimensions
        wav_signal = wav.squeeze()
        rows = wav_signal.shape[0]
        cols = wav_signal.shape[1]

    print('>>> Generating image (rows: {} cols: {})'.format(rows, cols))
    image = Image.new('RGB', (rows, cols))
    pixels = image.load()

    minimum = wav_signal[0,0]
    maximum = wav_signal[0,0]

    for x in range(0, rows):
        for y in range(0, cols):
            if wav_signal[x,y] > maximum:
                maximum = wav_signal[x,y]
            if wav_signal[x,y] < minimum:
                minimum = wav_signal[x,y]

    print('Minimum: ' + str(minimum))
    print('Maximum: ' + str(maximum))

    if maximum == minimum:
        maximum = 1 # nb: to prevent division by zero below

    for x in range(0, rows):
        for y in range(0, cols):
            v = wav_signal[x,y]
            scaled = int((v - minimum) / (maximum - minimum) * 255)
            pixels[x, y] = (scaled, scaled, scaled)

    # Image Show only works on local X server:
    #image.show()
    image.save(filename)

