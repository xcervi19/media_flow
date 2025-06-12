import subprocess, glob

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-framerate", "6", "-i", "chameleon/smile%02d.png",
    "-i", "logo/logo.png",
    "-filter_complex",
    # animace Leona loopnuta 36x, pak konec
    "[1:v]fps=6,loop=35:6:0,scale=300:-1,format=rgba,setpts=PTS-STARTPTS[anim];"
    # logo s fade-in/out
    "[2:v]format=rgba,scale=300:-1,"
    "fade=t=in:st=3:d=0.3:alpha=1,"
    "fade=t=out:st=5:d=0.3:alpha=1[logo];"
    # overlay Leon: vpravo nahoře, 4s–10s, neprotahuje video
    "[0:v][anim]overlay=W-w-30:30:enable='between(t,4,10)':shortest=1[v1];"
    # overlay logo: nahoře doprostřed
    "[v1][logo]overlay=(W-w)/2:80:enable='between(t,3,5.3)'",
    "-c:a", "copy",
    "out.mp4"
])
