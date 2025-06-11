import os
from moviepy import *

SCENES_DIR = "scenes"
MUSIC_PATH = "music/global_music.mp3"
OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_video.mp4")

scene_clips = []
ref_width, ref_height = None, None

for folder in sorted(os.listdir(SCENES_DIR)):
    folder_path = os.path.join(SCENES_DIR, folder)
    if not os.path.isdir(folder_path):
        continue
    for file in os.listdir(folder_path):
        if file.endswith(".mp4"):
            clip_path = os.path.join(folder_path, file)
            clip = VideoFileClip(clip_path)

            if not scene_clips:
                ref_width, ref_height = clip.w, clip.h
                print(ref_width, ref_height)
            # else:
            #     if clip.w < ref_width or clip.h < ref_height:
            #         scale_factor = max(ref_width / clip.w, ref_height / clip.h)
            #         clip = clip.resized(newsize=(ref_width, ref_height))

            scene_clips.append(clip)

if not scene_clips:
    raise RuntimeError("Nebyl nalezen žádný .mp4 soubor ve složce 'scenes/'.")

final_clip = concatenate_videoclips(scene_clips, method="compose")

if os.path.exists(MUSIC_PATH):
    music = AudioFileClip(MUSIC_PATH).with_duration(final_clip.duration)
    final_clip = final_clip.with_audio(music)

os.makedirs(OUTPUT_DIR, exist_ok=True)
final_clip.write_videofile(OUTPUT_PATH, codec="libx264", audio_codec="aac")
