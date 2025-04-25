"""
Algorithm implementation
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
from scipy.signal import spectrogram
from skimage.feature import peak_local_max
import soundfile as sf
from scipy.signal import stft, find_peaks

# ----------------------------------------------------------------------------
# Create a fingerprint for an audio file based on a set of hashes
# ----------------------------------------------------------------------------


class Encoding:

    """
    Class implementing the procedure for creating a fingerprint 
    for the audio files

    The fingerprint is created through the following steps
    - compute the spectrogram of the audio signal
    - extract local maxima of the spectrogram
    - create hashes using these maxima

    """

    def __init__(self, timelapse, time_window, freq_window, overlap):

      self.timelapse = timelapse
      self.time_window = time_window
      self.freq_window = freq_window
      self.overlap = overlap

      """
        Class constructor

        To Do
        -----

        Initialize in the constructor all the parameters required for
        creating the signature of the audio files. These parameters include for
        instance:
        - the window selected for computing the spectrogram
        - the size of the temporal window 
        - the size of the overlap between subsequent windows
        - etc.

        All these parameters should be kept as attributes of the class.
        """
      
    def process(self, fs, s):
      """

      To Do
      -----

      This function takes as input a sampled signal s and the sampling
      frequency fs and returns the fingerprint (the hashcodes) of the signal.
      The fingerprint is created through the following steps
      - spectrogram computation
      - local maxima extraction
      - hashes creation

      Implement all these operations in this function. Keep as attributes of
      the class the spectrogram, the range of frequencies, the anchors, the 
      list of hashes, etc.

      Each hash can conveniently be represented by a Python dictionary 
      containing the time associated to its anchor (key: "t") and a numpy 
      array with the difference in time between the anchor and the target, 
      the frequency of the anchor and the frequency of the target 
      (key: "hash")

      Parameters
      ----------

      fs: int
         sampling frequency [Hz]
      s: numpy array
         sampled signal
      """

      self.fs = fs
      self.s = s

      # Spectrogram computation
      freq, times, coefs = stft(s, fs, nperseg=self.timelapse, noverlap=self.overlap)
      spectrogram = np.abs(coefs)
      self.spectrogram = spectrogram
      

      # Local maxima extraction
      anchors = []
      for i in range(spectrogram.shape[1]):
         col = spectrogram[:, i]
         peaks, _ = find_peaks(col, distance=self.freq_window // 2)
         for p in peaks:
               anchors.append((times[i], freq[p]))
      anchors = np.array(anchors)
      self.anchors = anchors

      # Hashes creation
      H=[]
      N_MAX=10
      self.anchors
      peaks_sorted = sorted(peaks, key = lambda x:x[0])[:]
      for i in range(len(peaks_sorted)) :
         t_anchors,f_anchors = peaks_sorted[i]
         j = 1
         while j<=10 and i+j < len(peaks) : 
            ti,tj = peaks_sorted[i][0],peaks_sorted[j][0]
            if tj-ti >= self.overlap:
               t_target,f_target = peaks_sorted[i+j]
               delta_t = t_target-t_anchors
               h={"t":t_anchors, "hash": np.array([delta_t,f_anchors,f_target])}
               j+=1
               H.append(h)
      self.hashes = H



      





    def display_spectrogram(self,display_anchors):

        """
        Display the spectrogram of the audio signal

        Parameters
        ----------
        display_anchors: boolean
           when set equal to True, the anchors are displayed on the
           spectrogram
        """


        plt.pcolormesh(self.t, self.f/1e3, self.S, shading='gouraud')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [kHz]')
        if(display_anchors):
            plt.scatter(self.anchors[:, 0], self.anchors[:, 1]/1e3)
        plt.show()



# ----------------------------------------------------------------------------
# Compares two set of hashes in order to determine if two audio files match
# ----------------------------------------------------------------------------

class Matching:

    """
    Compare the hashes from two audio files to determine if these
    files match

    Attributes
    ----------

    hashes1: list of dictionaries
       hashes extracted as fingerprints for the first audiofile. Each hash 
       is represented by a dictionary containing the time associated to
       its anchor (key: "t") and a numpy array with the difference in time
       between the anchor and the target, the frequency of the anchor and
       the frequency of the target (key: "hash")

    hashes2: list of dictionaries
       hashes extracted as fingerprint for the second audiofile. Each hash 
       is represented by a dictionary containing the time associated to
       its anchor (key: "t") and a numpy array with the difference in time
       between the anchor and the target, the frequency of the anchor and
       the frequency of the target (key: "hash")

    matching: numpy array
       absolute times of the hashes that match together

    offset: numpy array
       time offsets between the matches
    """

    def __init__(self, hashes1, hashes2, offsets):

        """
        Compare the hashes from two audio files to determine if these
        files match

        Parameters
        ----------

        hashes1: list of dictionaries
           hashes extracted as fingerprint for the first audiofile. Each hash 
           is represented by a dictionary containing the time associated to
           its anchor (key: "t") and a numpy array with the difference in time
           between the anchor and the target, the frequency of the anchor and
           the frequency of the target

        hashes2: list of dictionaries
           hashes extracted as fingerprint for the second audiofile. Each hash 
           is represented by a dictionary containing the time associated to
           its anchor (key: "t") and a numpy array with the difference in time
           between the anchor and the target, the frequency of the anchor and
           the frequency of the target
          
        """


        self.hashes1 = hashes1
        self.hashes2 = hashes2

        times = np.array([item['t'] for item in self.hashes1])
        hashcodes = np.array([item['hash'] for item in self.hashes1])

        # Establish matches
        self.matching = []
        for hc in self.hashes2:
             t = hc['t']
             h = hc['hash'][np.newaxis, :]
             dist = np.sum(np.abs(hashcodes - h), axis=1)
             mask = (dist < 1e-6)
             if (mask != 0).any():
                 self.matching.append(np.array([times[mask][0], t]))
        self.matching = np.array(self.matching)

        # TODO: complete the implementation of the class by
        # 1. creating an array "offset" containing the time offsets of the 
        #    hashcodes that match
        # 2. implementing a criterion to decide whether or not both extracts
        #    match
       
             
    def display_scatterplot(self):

        """
        Display through a scatterplot the times associated to the hashes
        that match
        """
    
        plt.scatter(self.matching[:, 0], self.matching[:, 1])
        plt.show()


    def display_histogram(self):

        """
        Display the offset histogram
        """
        L = []
        for i in range(len(self.hashes1)) :
           offset = self.hashes1[i]["hash"][0] - self.hashes2[i]["hash"][0]
           L.append(offset)
        self.offsets = L
        plt.hist(self.offsets, bins=100, density=True)
        plt.xlabel('Offset (s)')
        plt.show()


