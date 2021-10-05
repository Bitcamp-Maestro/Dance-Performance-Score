from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, clips_array
from numpy.core.fromnumeric import size

clip1 = VideoFileClip("sample_data/BTS-Dynamite1-1.mp4")
clip2 = VideoFileClip("sample_data/BTS-Dynamite1-3.mp4")
clip1 = clip1.resize(0.50)
clip2 = clip2.resize(0.50)

final_clip = clips_array([[clip1, clip2]])

final_clip.write_videofile("test.mp4")