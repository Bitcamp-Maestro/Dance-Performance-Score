import numpy as np
import librosa
import librosa.core
import librosa.display

from audio import audio, melody


# Load Audio Recordings 
# First, we loaded audio from the professional dancer which is target video 

def Dtw(x1_chroma,x2_chroma):
    """
    Computes Dynamic Time Wariping DTW) of two sequences.

    """
    hop_size = 2205

    D, wp = librosa.sequence.dtw(x1_chroma, x2_chroma, subseq=True)
    wp_s = np.asarray(wp) * hop_size / sorted
    start_point = wp_s[:, 0][-1]
    end_point = wp_s[:, 0][0] - start_point
    return start_point, end_point
