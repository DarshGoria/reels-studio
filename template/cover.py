"""Cover image (1080x1920 JPG) for the grid: best face frame + gradient + 3-line headline.
Text stays inside the centre 3:4 area (y 240-1680) so the profile-grid crop never cuts it.

usage: python3 cover.py SECONDS "LINE ONE" "LINE TWO (accent)" "LINE THREE" [--tag TEXT] [--emoji 😳]
                        [--accent FFE500] [--place bottom|top] [--out cover.jpg]
  --place top    puts the headline in the empty space above the head (use when the face sits low in frame)
reads joined3.mkv (the graded cut)
"""
import argparse, subprocess
from PIL import Image, ImageDraw
from graphics import text_layer, pill, emoji_layer, scaled_center

ap = argparse.ArgumentParser()
ap.add_argument("t"); ap.add_argument("l1"); ap.add_argument("l2"); ap.add_argument("l3")
ap.add_argument("--tag"); ap.add_argument("--emoji", default="😳"); ap.add_argument("--accent", default="FFE500")
ap.add_argument("--place", default="bottom", choices=["bottom", "top"]); ap.add_argument("--out", default="cover.jpg")
a = ap.parse_args()
ACC = tuple(int(a.accent[i:i + 2], 16) for i in (0, 2, 4))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", a.t, "-i", "joined3.mkv", "-frames:v", "1", "cover_face.png"], check=True)
c = Image.open("cover_face.png").convert("RGBA")
g = Image.new("RGBA", c.size); d = ImageDraw.Draw(g)
for y in range(1920):
    k = max(0, (y - 850) / 500) if a.place == "bottom" else max(0, (960 - y) / 420)
    d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(215 * min(1, k))))
c.alpha_composite(g)
y0 = 1030 if a.place == "bottom" else 300
lum = 0.299 * ACC[0] + 0.587 * ACC[1] + 0.114 * ACC[2]
if a.tag: scaled_center(pill(a.tag, 64, ACC, fg=(0, 0, 0) if lum > 140 else (255, 255, 255)), 1, 540, y0, c)
for i, (txt, col) in enumerate(((a.l1, (255, 255, 255)), (a.l2, ACC), (a.l3, (255, 255, 255)))):
    scaled_center(text_layer(txt, 118, fill=col), 1, 540, y0 + 160 + i * 138, c)
scaled_center(emoji_layer(a.emoji, 150), 1, 930 if a.place == "top" else 180, 1000 if a.place == "top" else 420, c)
c.convert("RGB").save(a.out, quality=92)
print(a.out)
