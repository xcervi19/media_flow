import subprocess, glob

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-loop", "1", "-t", "5", "-i", "logo/logo.png",  # <- důležité omezení délky
    "-filter_complex",
    "[1:v]format=rgba,"
    "scale=iw*(0.7+0.3*(t-2)/1):ih*(0.7+0.3*(t-2)/1):eval=frame,"
    "fade=t=in:st=2:d=1:alpha=1,"
    "fade=t=out:st=4.5:d=0.5:alpha=1[logo];"
    "[0:v][logo]overlay=(W-w)/2:80:enable='between(t,2,5)'",
    "-c:a", "copy",
    "out_with_logo.mp4"
])
