import subprocess, glob
import ffmpeg

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]
duration = float(ffmpeg.probe(video_file)["format"]["duration"])
start = round(duration - 5, 2)

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-vf",
    f"drawtext=fontfile=fonts/OpenSans-Bold.ttf:text='FOLLOW US':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=100:"
    f"enable='between(t,{start},{start+3})':alpha='if(lt(t,{start+1}),(t-{start})/1,1)',"
    f"drawtext=fontfile=fonts/OpenSans-Regular.ttf:"
    f"text='We’re documenting the entire creative journey. Join us.':fontcolor=white:fontsize=40:"
    f"x=(w-text_w)/2:y=200:enable='between(t,{start+1},{duration})':alpha='if(lt(t,{start+2}),(t-{start+1})/1,1)'",
    "-c:a", "copy",
    "-shortest",
    "out_text.mp4"
])
