from utils.audio import Audio, Melody
from utils.clip import Clip
from utils.dtw import Dtw
from utils.video import Video

def video__init__(self, video1, video2):
    Clip(video1, "wav1.wav")
    Clip(video2, "wav2.wav")
    x1, sr = Audio("wav1.wav")
    x2, sr = Audio("wav2.wav")
    x1_chroma = Melody(x1, sr)
    x2_chroma = Melody(x2, sr)
    start_point, end_point = Dtw(x1_chroma, x2_chroma)
    new_clip = Video(start_point, end_point)
    