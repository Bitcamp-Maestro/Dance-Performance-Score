from utils.audio import Audio, Melody
from utils.clip import Clip
from utils.dtw import Dtw
from utils.mix_video import mix_video

def video__init__(user_video, target_video, output):
    Clip(user_video, "sample_data/audio/wav1.wav")
    Clip(target_video, "sample_data/audio/wav2.wav")
    
    x1, sr = Audio("sample_data/audio/wav1.wav")
    x2, sr = Audio("sample_data/audio/wav2.wav")
    
    x1_chroma = Melody(x1, sr)
    x2_chroma = Melody(x2, sr)
    
    time = Dtw(x1_chroma, x2_chroma, sorted=sr)

    print("start time : ", time["start"])
    print("end time : ", time["end"])

    mix_video(user_video=user_video, target_video=target_video, time=time, output=output)

if __name__ == '__main__':
    video__init__(
        user_video="sample_data/sample.mp4",
        target_video="sample_data/BTS-Dynamite1-3.mp4",
        output="result"
    )