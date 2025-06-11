import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip, AudioFileClip

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] > max_width:
            lines.append(line.strip())
            line = word + " "
        else:
            line = test_line

    if line:
        lines.append(line.strip())

    return lines


# Nastavení složek
ASSETS_DIR = "assets"
OUTPUT_DIR = "output"
BACKGROUND_IMG = None
AUDIO_FILE = None

# Najdi první image a audio soubor v assets
for f in os.listdir(ASSETS_DIR):
    if f.lower().endswith((".jpg", ".jpeg", ".png")) and BACKGROUND_IMG is None:
        BACKGROUND_IMG = os.path.join(ASSETS_DIR, f)

# Ověř
if not BACKGROUND_IMG:
    raise FileNotFoundError("Chybí background image nebo audio v assets složce.")

# Načti background a zjisti parametry
bg_cv = cv2.imread(BACKGROUND_IMG)
h, w, _ = bg_cv.shape

# Detekuj průměrnou barvu pozadí
mean_color = cv2.mean(bg_cv)[:3]
luminance = (0.299 * mean_color[2] + 0.587 * mean_color[1] + 0.114 * mean_color[0])
text_color = (255, 255, 255) if luminance < 128 else (0, 0, 0)

# Texty pro animaci
texts = [
    "Let's remake!",
    "The popular game!",
    "Make IOS native"
]

# Font
font_path = os.path.join("fonts", "LIntel-Regular.otf")
font = ImageFont.truetype(font_path, int(h / 10))


# Parametry animace
frames = []
fps = 30
frames_per_text = 45
# Vytvoření frames s animací (fade-in + scale-in)
for text in texts:
    # Předpočítej layout pro max scale (==1.0)
    max_font_size = int((h / 10) * 1.0)
    base_font = ImageFont.truetype(font_path, max_font_size)
    draw_dummy = ImageDraw.Draw(Image.new("RGB", (w, h)))
    lines = wrap_text(text, base_font, int(0.9 * w), draw_dummy)
    base_line_height = base_font.getbbox("Hg")[3] - base_font.getbbox("Hg")[1]

    for i in range(frames_per_text):
        bg_rgb = cv2.cvtColor(bg_cv, cv2.COLOR_BGR2RGB)
        bg_pil = Image.fromarray(bg_rgb).convert("RGBA")

        progress = i / frames_per_text
        opacity = int(255 * progress)
        scale = 0.7 + 0.3 * progress

        temp_font = ImageFont.truetype(font_path, int(max_font_size * scale))
        txt_layer = Image.new("RGBA", bg_pil.size, (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_layer)

        line_height = temp_font.getbbox("Hg")[3] - temp_font.getbbox("Hg")[1]
        total_height = len(lines) * line_height
        start_y = int(h * 0.25 - total_height // 2)

        for j, line in enumerate(lines):
            bbox = txt_draw.textbbox((0, 0), line, font=temp_font)
            line_width = bbox[2] - bbox[0]
            x = (w - line_width) // 2
            y = start_y + j * line_height
            txt_draw.text((x, y), line, font=temp_font, fill=text_color + (opacity,))

        combined = Image.alpha_composite(bg_pil, txt_layer)
        frames.append(np.array(combined.convert("RGB")))



# Vytvoř video klip
clip = ImageSequenceClip(frames, fps=fps)

# Výstup
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, "ad_video.mp4")
clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
