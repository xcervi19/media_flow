import subprocess, glob

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-framerate", "6", "-i", "chameleon/smile%02d.png",
    "-filter_complex",
    "[1:v]fps=6,loop=35:6:0,scale=300:-1,format=rgba,setpts=PTS-STARTPTS[anim];"
    "[0:v][anim]overlay=W-w-30:30:enable='between(t,4,10)':shortest=1",
    "-c:a", "copy",
    "out.mp4"
])
