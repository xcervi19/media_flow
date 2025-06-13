
import subprocess, glob
import ffmpeg

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]
duration = float(ffmpeg.probe(video_file)["format"]["duration"])
start = round(duration - 5, 2)

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-filter_complex",
    f"""
    drawtext=fontfile=fonts/OpenSans-Bold.ttf:
    text='FOLLOW US':
    fontcolor=white:fontsize=120:
    x=(w-text_w)/2:
    y='if(lt(t,{start+1}),(h*-0.2 + (h*0.4)*(t-{start})/1.2),h*0.2)':
    enable='gte(t,{start})',

    drawtext=fontfile=fonts/OpenSans-Regular.ttf:
    text='Join our creative':
    fontcolor=white:fontsize=48:
    x='if(lt(t,{start+1.5}),-tw,(w-text_w)/2)':
    y=h*0.45:
    enable='between(t,{start+1.5},{start+4})',

    drawtext=fontfile=fonts/OpenSans-Regular.ttf:
    text='development journey':
    fontcolor=white:fontsize=48:
    x='if(lt(t,{start+1.8}),-tw,(w-text_w)/2)':
    y=h*0.53:
    enable='between(t,{start+1.8},{start+4.3})',

    drawtext=fontfile=fonts/OpenSans-Regular.ttf:
    text='from zero to launch.':
    fontcolor=white:fontsize=48:
    x='if(lt(t,{start+2.1}),-tw,(w-text_w)/2)':
    y=h*0.61:
    enable='between(t,{start+2.1},{start+4.6})'
    """.replace('\n', ''),
    "-c:a", "copy",
    "-shortest",
    "out_text_mobile.mp4"
])
