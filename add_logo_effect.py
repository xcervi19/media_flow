import subprocess, glob

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-loop", "1", "-t", "5", "-i", "logo/logo.png",
    "-filter_complex",
    "[1:v]format=rgba,"
    "scale=iw*(if(between(t\\,2\\,3)\\,0.1+0.4*(t-2)\\,0.5)):"
    "ih*(if(between(t\\,2\\,3)\\,0.1+0.4*(t-2)\\,0.5)):eval=frame,"
    "fade=t=in:st=2:d=1:alpha=1,"
    "fade=t=out:st=4.5:d=0.5:alpha=1[logo];"
    "[0:v][logo]overlay=x=(W-w)/2:y=H/2:enable='between(t,2,5)'",
    "-c:a", "copy",
    "out_with_logo.mp4"
])
