import os
import cv2
import numpy as np
import ffmpeg
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "assets"
LOGO_DIR = "logo"
CHAMELEON_DIR = "chameleon"
OUTPUT_DIR = "output"
FONT_PATH = os.path.join("fonts", "LIntel-Regular.otf")
VIDEO_FILE = None
VIDEO_DIR = "in"

for f in os.listdir(VIDEO_DIR):
    if f.lower().endswith((".mp4", ".mov")):
        VIDEO_FILE = os.path.join(VIDEO_DIR, f)
        break

if not VIDEO_FILE:
    raise FileNotFoundError("Ve složce 'in' nebylo nalezeno žádné video.")

video_streams = [s for s in ffmpeg.probe(VIDEO_FILE)["streams"] if s["codec_type"] == "video"]
if not video_streams:
    raise ValueError("No video stream found in the file.")
video_info = video_streams[0]

w = int(video_info['width'])
h = int(video_info['height'])
fps = eval(video_info['r_frame_rate'])

audio_file = next((os.path.join(ASSETS_DIR, f) for f in os.listdir(ASSETS_DIR) if f.lower().endswith((".mp3", ".wav"))), None)
if not audio_file:
    raise FileNotFoundError("No audio file found in assets.")

logo_file = next((os.path.join(LOGO_DIR, f) for f in os.listdir(LOGO_DIR) if f.lower().endswith((".png", ".jpg"))), None)

font_size = int(h / 15)
font = ImageFont.truetype(FONT_PATH, font_size)
img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
text = "FOLLOW TechArt Society\nWe going to share developing journey."
tw, th = draw.textbbox((0, 0), text, font=font)[2:]
draw.text(((w - tw) / 2, (h - th) / 2), text, font=font, fill=(255, 255, 255, 255))
text_overlay_path = os.path.join(OUTPUT_DIR, "final_text.png")
os.makedirs(OUTPUT_DIR, exist_ok=True)
img.save(text_overlay_path)

chameleon_frames = [os.path.join(CHAMELEON_DIR, f) for f in sorted(os.listdir(CHAMELEON_DIR)) if f.endswith((".png", ".jpg"))]
chameleon_input = f"concat:{'|'.join(chameleon_frames)}"

output_path = os.path.join(OUTPUT_DIR, "processed_video.mp4")

ffmpeg_cmd = (
    ffmpeg
    .input(VIDEO_FILE)
    .output('tmp_video.mp4', an=None)
    .run_async(overwrite_output=True)
)
ffmpeg_cmd.communicate()

input_video = ffmpeg.input('tmp_video.mp4')
overlay_logo = f"overlay=(main_w-overlay_w)/2:0:enable='between(t,8,{999})" if logo_file else None
overlay_chameleon = f"overlay=W-w:H-h:enable='between(t,3,6)'" if chameleon_frames else None
fade_text = f"fade=t=in:st=14:d=1,fade=t=out:st=duration-1:d=1"

filter_complex = []
if logo_file:
    filter_complex.append(f"[0:v][1:v]{overlay_logo}[v1]")
if chameleon_frames:
    filter_complex.append(f"[v1][2:v]{overlay_chameleon}[v2]")
filter_complex.append(f"[v2][3:v]overlay=0:0:enable='between(t,14,20)',{fade_text}[v]" if chameleon_frames and logo_file else f"[0:v][1:v]overlay=0:0:enable='between(t,14,20)',{fade_text}[v]")

inputs = {'0': 'tmp_video.mp4'}
idx = 1
if logo_file:
    inputs[str(idx)] = logo_file
    idx += 1
if chameleon_frames:
    inputs[str(idx)] = chameleon_frames[0]
    idx += 1
inputs[str(idx)] = text_overlay_path

input_args = [ffmpeg.input(inputs[k]) for k in sorted(inputs.keys())]
output_args = ffmpeg.output(
    *input_args,
    output_path,
    **{
        'c:v': 'libx264',
        'c:a': 'aac',
        'vf': ','.join(filter_complex),
        'shortest': None
    }
)

ffmpeg.run(output_args, overwrite_output=True)

final_output = os.path.join(OUTPUT_DIR, "final_output.mp4")
ffmpeg.input(output_path).output(
    final_output,
    **{
        'i': audio_file,
        'c:v': 'copy',
        'c:a': 'aac',
        'shortest': None
    }
).run(overwrite_output=True)

