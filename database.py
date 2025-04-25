"""
Create a database containing the hashcodes of the songs stored
in the specified folder (.wav files only).
The database is saved as a pickle file as a list of dictionaries.
Each dictionary has two keys 'song' and 'hashcodes', corresponding
to the name of the song and to the hashcodes used as signature for
the matching algorithm.
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
from algorithm import *


# ----------------------------------------------
# Run the script
# ----------------------------------------------
if __name__ == "__main__":
    folder = "./samples/"

    # 1: Load the audio files
    import os

    audiofiles = os.listdir(folder)
    audiofiles = [item for item in audiofiles if item[-4:] == ".wav"]

    # 2: Set the parameters of the encoder
    nperseg = 128
    noverlap = 32
    min_distance = 50
    time_window = 1.0
    freq_window = 1500
    encoder = Encoding(
        timelapse=nperseg,
        overlap=noverlap,
        time_window=time_window,
        freq_window=freq_window,
    )

    # 3: Construct the database
    database = []
    for audiofile in audiofiles:
        fs, s = read(folder + "/" + audiofile)
        print("Song: " + audiofile[:-4])
        print("Sampling frequency: " + str(fs))
        encoder.process(fs, s)
        database.append({"song": audiofile[:-4], "hashcodes": encoder.hashes})

    # 4: Save the database
    with open("songs.pickle", "wb") as handle:
        pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)
        