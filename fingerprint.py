"""
Author: Eva Fineberg 
Queen Mary University of London 
Music Informatics 2021
"""

import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import hashlib

from db import Database
from skimage.feature import peak_local_max
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure

# Default Fs - everything is 22050
DEFAULT_FS=22050

# Default fft size for 22050Hz
NFFT=2048

# Min amplitude to be considered a peak
MIN_AMPLITUDE=10

# Number of coordinates around an amplitude peak 
# in the spectrogram
NEIGHBOURHOOD=20

# Plot flag
plot = False

# Number of bits to throw away from the front of the SHA1 hash in the
# fingerprint calculation. 
FINGERPRINT_CUTOFF = 20

# Degree to which a fingerprint can be
# Associated with its neighbors
FAN_VALUE = 15

# plot flag
plot=False

# How close and far can finger prints be in
# order to be a pair of peaks in a finger print
MIN_TIME_DELTA = 0
MAX_TIME_DELTA = 200

# Code referenced from Lab 10 jupytre notebook on QMPlus
def get_spectrogram(data, sr):
    spec = np.abs(librosa.stft(data, n_fft=NFFT,window='hann',hop_length=int(NFFT/4)))
    if plot:
        plt.figure(figsize=(10, 5))
        librosa.display.specshow(librosa.amplitude_to_db(spec,ref=np.max),y_axis='linear', x_axis='time',cmap='gray_r',sr=sr)
    return spec

# Code referenced from Lab 10 jupytre notebook on QMPlus
def get_peak_coords(spectrogram):
    coordinates = peak_local_max(np.log(spectrogram), min_distance=10,threshold_rel=0.05,indices = False)
    if plot:
        plt.figure(figsize=(10, 5))
        plt.imshow(coordinates,cmap=plt.cm.gray_r,origin='lower')
    return coordinates

# peak_picks uses a 2D array algorithm
# code referenced from: 
# https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
def pick_peaks(spec):
    structure = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(structure, NEIGHBOURHOOD)

    local_max = maximum_filter(spec, footprint=neighborhood)==spec
    background = (spec == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    detected_peaks = local_max ^ eroded_background
    
    # extract the amplitudes with the 2d mask and flatten
    amplitudes = spec[detected_peaks].flatten()
    # take the time frequency pairs
    freq, t = np.where(detected_peaks)
    
    # discard all peaks with an amplitude lower than the cutoff
    unfiltered_peaks = zip(t, freq, amplitudes)
    filtered_peaks = [x for x in unfiltered_peaks if x[2] > MIN_AMPLITUDE]
    
    # extract time and frequency indicies
    time = [x[0] for x in filtered_peaks]
    frequency = [x[1] for x in filtered_peaks]

    #  plot if set
    if plot:
        _, axis = plt.subplots()
        axis.imshow(spec)
        axis.scatter(time, frequency)
        axis.set_xlabel('Time')
        axis.set_ylabel('Frequency')
        plt.gca().invert_yaxis()
        plt.show(block=True)
    
    # return iterable in list form
    return list(zip(time, frequency))

def get_hashes(peaks):
    # return a list of hashes based on the peaks
    hashes = []
    
    # Loop through the peaks and the neighboring considered cells
    for i in range(len(peaks)):
        for j in range(1, FAN_VALUE):
            if (i + j) < len(peaks):
                # Get values at times (within range)
                time_1 = peaks[i][0]
                time_2 = peaks[i + j][0]
                # Get values at frequencies (within range)
                freq1 = peaks[i][1]
                freq2 = peaks[i + j][1]
                # Take the difference in times
                time_delta = time_2 - time_1

                # Check if that difference is within the rangee that it can still be considered a peak
                if time_delta >= MIN_TIME_DELTA and time_delta <= MAX_TIME_DELTA:
                    hash = hashlib.sha1(str(str(freq1) + str(freq2) + str(time_delta)).encode('utf-8'))

                    hashes.append((hash.hexdigest()[0:FINGERPRINT_CUTOFF], t1))

    return hashes


# process_audio finds and computes the 
# hashes of the constellation peaks
# :param path is the path to the audio
# :param sr is the sample rate
def process_audio(path, sr):
    y, sr = librosa.load(path, sr=sr)
    # Compute and plot STFT spectrogram
    stft_spectrogram = get_spectrogram(y, sr)
    
    # Detect peaks from STFT spectrogram and plot constellation map
    if plot:
        peak_coords = get_peak_coords(stft_spectrogram)
    # Find peaks with 2-d approach
    peaks = pick_peaks(stft_spectrogram)
    hashes = get_hashes(peaks)
    return hashes

# Takes two data paths and reads from one to produce 
# fingerprints of audio in the second
# :param db_path is the path to the database recordings
# :param fp_path is the path to where the fingerprints
# will be stored
def fingerprintBuilder(db_path, fp_path):

    # Get all files in the recordings database
    r_files = [x for x in os.listdir(db_path) if x.endswith('.wav')]

    # Initialise the DB
    db = Database(fp_path)

    # Loop through recorded files and store their fingerprints
    for file in r_files:
        print("Fingerprinting {0}...".format(file))
        hashes = process_audio(os.path.join(db_path, file), sr=DEFAULT_FS)
        db.store(file, hashes)
