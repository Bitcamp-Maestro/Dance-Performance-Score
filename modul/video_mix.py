from mmcv import video
from moviepy.editor import VideoFileClip, clips_array, vfx, CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def Video_Mix(video1,video2):
    #1920X1080
    clip1 = VideoFileClip(video1)
    clip1.set_position("left")
    clip2 = VideoFileClip(video2)
    clip2.set_position("right")
    final_clip = clips_array([[clip1, clip2]])
    final_clip.resize(width=1920,height=1080).write_videofile("final_clips.mp4")

    return final_clip
if __name__ == "__main__":
    Video_Mix("sample_data/BTS-Dynamite/1/BTS-Dynamite1-1.mp4", "sample_data/BTS-Dynamite/1/BTS-Dynamite1-3.mp4")