import subprocess, glob
import ffmpeg

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]
duration = float(ffmpeg.probe(video_file)["format"]["duration"])
start = round(duration - 5, 2)

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-vf", f"fade=t=out:st={start}:d=5:alpha=0",
    "-c:a", "copy",
    "out_darkened.mp4"
])
