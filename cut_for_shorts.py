import subprocess
import glob
import json

def get_video_resolution(path):
    result = subprocess.run([
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", path
    ], capture_output=True, text=True)

    streams = json.loads(result.stdout)["streams"]
    video_stream = next(s for s in streams if s["codec_type"] == "video")
    return int(video_stream["width"]), int(video_stream["height"])

video_file = glob.glob("in/*.[mM][oO][vVpP4]*")[0]
width, height = get_video_resolution(video_file)

if width > height:
    crop_w = int(height * 9 / 16)
    x_offset = (width - crop_w) // 2
    filter_str = f"crop={crop_w}:{height}:{x_offset}:0,scale=1080:1920"
else:
    filter_str = "scale=1080:1920"

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-vf", filter_str,
    "-c:a", "copy",
    "shorts_output.mp4"
])
