import subprocess, glob
import ffmpeg

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]
duration = float(ffmpeg.probe(video_file)["format"]["duration"])
start = round(duration - 5, 2)

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-loop", "1", "-t", "5", "-i", "logo_soc/insta.png",
    "-loop", "1", "-t", "5", "-i", "logo_soc/tiktok.png",
    "-loop", "1", "-t", "5", "-i", "logo_soc/facebook.png",
    "-loop", "1", "-t", "5", "-i", "logo_soc/youtube.png",
    "-filter_complex",
    f"""
    [1:v]scale=100:-1[insta];
    [2:v]scale=100:-1[tiktok];
    [3:v]scale=100:-1[facebook];
    [4:v]scale=100:-1[youtube];
    [0:v]format=yuv420p[base];
    [base][insta]overlay=x=500:y='if(lt(t,{start+1}),(H+100)-(t-{start+1})*400,H/2)':enable='between(t,{start+1},{duration})'[s1];
    [s1][tiktok]overlay=x=650:y='if(lt(t,{start+1.3}),(H+100)-(t-{start+1.3})*400,H/2)':enable='between(t,{start+1.3},{duration})'[s2];
    [s2][facebook]overlay=x=800:y='if(lt(t,{start+1.6}),(H+100)-(t-{start+1.6})*400,H/2)':enable='between(t,{start+1.6},{duration})'[s3];
    [s3][youtube]overlay=x=950:y='if(lt(t,{start+1.9}),(H+100)-(t-{start+1.9})*400,H/2)':enable='between(t,{start+1.9},{duration})'
    """,
    "-c:a", "copy",
    "-shortest",
    "out_social_icons_scaled.mp4"
])
