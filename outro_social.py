import subprocess, glob

video_file = [f for f in glob.glob("in/*") if f.lower().endswith((".mp4", ".mov"))][0]

subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-loop", "1", "-t", "5", "-f", "lavfi", "-i", "color=black:s=1920x1080",
    "-loop", "1", "-t", "5", "-i", "logo_soc/insta.png",
    "-loop", "1", "-t", "5", "-i", "logo_soc/tiktok.png",
    "-loop", "1", "-t", "5", "-i", "logo_soc/facebook.png",
    "-loop", "1", "-t", "5", "-i", "logo_soc/youtube.png",
    "-filter_complex",
    "[0:v]format=yuv420p,split[main][fade];"
    "[fade][1:v]overlay=shortest=1:enable='gte(t,main_t-5)'[dark];"

    "[dark]drawtext=fontfile=fonts/OpenSans-Bold.ttf:text='FOLLOW US':"
    "fontcolor=white:fontsize=80:x=(w-text_w)/2:y=200:"
    "enable='between(t,main_t-5,main_t-2)':alpha='if(lt(t,main_t-4), (t-(main_t-5))/1, 1)'[t1];"

    "[t1]drawtext=fontfile=fonts/OpenSans-Bold.ttf:"
    "text='We\\'re sharing the full journey. Don\\'t miss out!':"
    "fontcolor=white:fontsize=40:x=(w-text_w)/2:y=300:"
    "enable='between(t,main_t-4,main_t)':alpha='if(lt(t,main_t-3),(t-(main_t-4))/1,1)'[t2];"

    "[t2][2:v]overlay=x=550:y='if(lt(t,main_t-3),(H+100)-(t-(main_t-3))*400, H/2)':enable='between(t,main_t-3,main_t)'[s1];"
    "[s1][3:v]overlay=x=750:y='if(lt(t,main_t-3.2),(H+100)-(t-(main_t-3.2))*400, H/2)':enable='between(t,main_t-3.2,main_t)'[s2];"
    "[s2][4:v]overlay=x=950:y='if(lt(t,main_t-3.4),(H+100)-(t-(main_t-3.4))*400, H/2)':enable='between(t,main_t-3.4,main_t)'[s3];"
    "[s3][5:v]overlay=x=1150:y='if(lt(t,main_t-3.6),(H+100)-(t-(main_t-3.6))*400, H/2)':enable='between(t,main_t-3.6,main_t)'",
    
    "-c:a", "copy",
    "-shortest",
    "out_social.mp4"
])
