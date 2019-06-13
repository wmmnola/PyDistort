import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import sys
import getopt
import scipy.fftpack as fft
import scipy.signal as sig
import scipy.stats as norm
import scipy.signal as sig
import math

def dist(s, H, G):
    f = np.linspace(0, 1000, len(s))
    H_seq = [H(f),H(f)]
    inv_fft = np.real(fft.ifft(H_seq))
    final = sig.convolve(s, inv_fft, method='auto')
    return G * final


def get_name(file):
    file.split("/")
    return file[::-1]

def break_audio(sig):
    lst = []
    for x in range(0, len(sig)-256, 256):
        lst.append(sig[x-256:x])
    return lst
def help():
    print("py_distort.py [options] <input file>")
    print("Options")
    print("-h displays this dialog")
    print("-p apply polynomial distortion")
    print("-c apply cubic distortion")
    print("-g apply a gaussian distortion \n -e apply exponential distortion")

def find_wav(file,output, H):
    print(file)
    try:
        sig, fs = sf.read(file)
        signals = np.array_split(sig, 1000)
        f = np.asanyarray([0,0])
        distored_signals_977 = []
        disroted_signals_976 = []
        for s in signals:
            print(s.shape)
            if(s.shape == (976,2)):
                distored_signals_977.append(dist(s, H, 100))
            else:
                disroted_signals_976.append(dist(s, H, 100))

        f1 = np.hstack(distored_signals_977)
        f2 = np.hstack(disroted_signals_976)
        np.concatenate(f1, f2)
        #distorted_signal = dist(sig, H, 10000)
        #print(distorted_signal)
        sf.write(output, f1, fs, subtype='FLOAT')
    ## TODO: make this an actual File not Found Exception
    except FileNotFoundError:
        print("Error:%s not found in directory" % file)
        sys.exit(0)

arguements = sys.argv[1::]

try:
    opts, args = getopt.getopt(arguements,"heg",["ifile=", "ofile="])
    input = args[0]
    out = args[1]

    for opt in opts:
        if("-h" in opt):
            help()
        if("-e" in opt):
            k = 2
            h = lambda s: np.exp(-k *s)
            find_wav(input, out, h)
        if("-g" in opt):
            h = lambda s: norm.norm.pdf(s, 2.5, 1000)
            find_wav(input, out, h)


except getopt.GetoptError:
    print("Incorrect Syntax. Correct usage is py_distort.py [options] <input file>")
    print("Use -h for a list of options")

#sig, fs = sf.read("sample.wav")
#sf.write('sample_distorted.wav', distortion, fs, subtype='FLOAT')
