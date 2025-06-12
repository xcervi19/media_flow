import subprocess
import glob

video_file = glob.glob("in/*")
video_file = [f for f in video_file if f.lower().endswith(('.mp4', '.mov'))][0]

subprocess.run([
    "ffmpeg",
    "-y",
    "-i", video_file,
    "-framerate", "6",
    "-i", "chameleon/smile%02d.png",
    "-filter_complex",
    "[1:v]format=rgba[anim];[0:v][anim]overlay=10:H-h-10:eof_action=pass",
    "-c:a", "copy",
    "out.mp4"
])

