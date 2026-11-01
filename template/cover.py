"""Cover image (1080x1920 JPG) for the grid: best face frame + dark gradient + 3-line headline.
Text sits inside the centre 3:4 area so the profile grid crop never cuts it.

usage: python3 cover.py FRAME_SECONDS "LINE ONE" "LINE TWO (yellow)" "LINE THREE" [PILL] [EMOJI]
reads joined3.mkv (the graded cut), writes cover.jpg
"""
import subprocess, sys
from PIL import Image, ImageDraw
from graphics import text_layer, pill, emoji_layer, scaled_center, YELLOW

t = sys.argv[1]; l1, l2, l3 = sys.argv[2:5]
tag = sys.argv[5] if len(sys.argv) > 5 else None
emo = sys.argv[6] if len(sys.argv) > 6 else "😳"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", "joined3.mkv", "-frames:v", "1", "cover_face.png"], check=True)
c = Image.open("cover_face.png").convert("RGBA")
g = Image.new("RGBA", c.size); d = ImageDraw.Draw(g)
for y in range(1920):
    d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(210 * min(1, max(0, (y - 850) / 500)))))
c.alpha_composite(g)
if tag: scaled_center(pill(tag, 70, YELLOW), 1, 540, 1030, c)
scaled_center(text_layer(l1, 120), 1, 540, 1190, c)
scaled_center(text_layer(l2, 120, fill=YELLOW), 1, 540, 1330, c)
scaled_center(text_layer(l3, 120), 1, 540, 1470, c)
scaled_center(emoji_layer(emo, 160), 1, 180, 420, c)
c.convert("RGB").save("cover.jpg", quality=92)
print("cover.jpg")
