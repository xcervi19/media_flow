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
    y='if(lt(t,{start+1.2}), h*-0.5 + (h*0.7)*(1 - exp(-(t-{start})*3)), h*0.2)':
    enable='gte(t,{start})',

    drawtext=fontfile=fonts/OpenSans-Regular.ttf:
    text='Join our creative':
    fontcolor=white:fontsize=60:
    x='if(lt(t,{start+1.5}),-tw*1.2,(w-text_w)/2)':
    y=h*0.3:
    enable='gte(t,{start+1.5})',

    drawtext=fontfile=fonts/OpenSans-Regular.ttf:
    text='development journey':
    fontcolor=white:fontsize=60:
    x='if(lt(t,{start+1.8}),-tw*1.2,(w-text_w)/2)':
    y=h*0.35:
    enable='gte(t,{start+1.8})',

    drawtext=fontfile=fonts/OpenSans-Regular.ttf:
    text='from zero to launch.':
    fontcolor=white:fontsize=60:
    x='if(lt(t,{start+2.1}),-tw*1.2,(w-text_w)/2)':
    y=h*0.40:
    enable='gte(t,{start+2.1})',

    drawtext=fontfile=fonts/OpenSans-Bold.ttf:
    text='techart_society':
    fontcolor=#8ecae6:fontsize=50:
    x=(w-text_w)/2:
    y=h*0.45:
    enable='gte(t,{start+2.4})'
    """.replace('\n', ''),
    "-c:a", "copy",
    "-shortest",
    "out_text_mobile.mp4"
])
