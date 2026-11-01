# reels-studio template — Generic helpers (easing, text, pills, phone mockup, flags, orb, calendar, emoji) + v2 elements reused by v3.
"""Original animated graphics for the Apple x Alibaba reel.
Renders RGBA animations to .mov (png codec, alpha) in anims/."""
import math, os, subprocess, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
os.makedirs("anims", exist_ok=True)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
def font(sz, bold=True): return ImageFont.truetype(FB if bold else FM, sz)

YELLOW = (255, 229, 0)
# ---------- easing
def clamp(x, a=0, b=1): return max(a, min(b, x))
def out_back(x, s=1.70158):
    x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def out_cubic(x): x = clamp(x); return 1 - (1 - x) ** 3
def in_cubic(x): x = clamp(x); return x ** 3

def encode(name, frames_fn, dur, size):
    n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
                          "-s", f"{size[0]}x{size[1]}", "-r", str(FPS), "-i", "-",
                          "-c:v", "png", "-pix_fmt", "rgba", f"anims/{name}.mov"], stdin=subprocess.PIPE)
    for i in range(n):
        im = frames_fn(i / FPS, dur)
        p.stdin.write(im.convert("RGBA").tobytes())
    p.stdin.close(); p.wait()
    print("rendered", name, n, "frames")

def scaled_center(layer, scale, cx, cy, canvas, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    w, h = layer.size
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    l = layer.resize((nw, nh), Image.LANCZOS)
    if alpha < 1:
        a = l.getchannel("A").point(lambda v: int(v * alpha)); l.putalpha(a)
    canvas.alpha_composite(l, (int(cx - nw / 2), int(cy - nh / 2)))

def text_layer(txt, sz, fill=(255, 255, 255), glow=None, bold=True, pad=40):
    f = font(sz, bold)
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    d.text((pad - bb[0], pad - bb[1]), txt, font=f, fill=fill)
    if glow:
        g = Image.new("RGBA", (w, h)); ImageDraw.Draw(g).text((pad - bb[0], pad - bb[1]), txt, font=f, fill=glow)
        g = g.filter(ImageFilter.GaussianBlur(18))
        g.alpha_composite(im); im = g
    return im

def emoji_layer(ch, px):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((px, int(px * im.height / im.width)), Image.LANCZOS)

# ---------- shared pieces
def bg_gradient(c1=(8, 10, 24), c2=(40, 14, 70)):
    g = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(g)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3)) + (255,))
    # soft spotlight
    spot = Image.new("RGBA", (W, H)); ImageDraw.Draw(spot).ellipse((140, 420, 940, 1220), fill=(120, 80, 255, 70))
    g.alpha_composite(spot.filter(ImageFilter.GaussianBlur(160)))
    return g

random.seed(7)
PARTS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(2, 5), random.uniform(10, 40)) for _ in range(45)]
def particles(canvas, t):
    d = ImageDraw.Draw(canvas)
    for x, y, r, sp in PARTS:
        yy = (y - t * sp * 3) % H
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 60))

def orb(size, cols):
    """generic glowing AI orb (original design)"""
    im = Image.new("RGBA", (size, size))
    s = size
    for i, (c, ox, oy) in enumerate(zip(cols, (0.38, 0.62, 0.5), (0.42, 0.45, 0.62))):
        b = Image.new("RGBA", (s, s))
        ImageDraw.Draw(b).ellipse((s * (ox - 0.28), s * (oy - 0.28), s * (ox + 0.28), s * (oy + 0.28)), fill=c + (230,))
        im.alpha_composite(b.filter(ImageFilter.GaussianBlur(s * 0.045)))
    mask = Image.new("L", (s, s)); ImageDraw.Draw(mask).ellipse((s * .1, s * .1, s * .9, s * .9), fill=255)
    core = Image.new("RGBA", (s, s)); core.paste(im, (0, 0), mask)
    glow = core.filter(ImageFilter.GaussianBlur(s * 0.08))
    glow.alpha_composite(core)
    hl = Image.new("RGBA", (s, s)); ImageDraw.Draw(hl).ellipse((s * .3, s * .2, s * .55, s * .38), fill=(255, 255, 255, 110))
    glow.alpha_composite(hl.filter(ImageFilter.GaussianBlur(s * .04)))
    return glow

def phone(w=520, screen=(14, 14, 22)):
    h = int(w * 2.05)
    im = Image.new("RGBA", (w + 40, h + 40))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, w + 20, h + 20), radius=int(w * .16), fill=(60, 62, 70), outline=(150, 152, 160), width=5)
    d.rounded_rectangle((34, 34, w + 6, h + 6), radius=int(w * .14), fill=screen)
    d.rounded_rectangle((w / 2 - 55 + 20, 56, w / 2 + 55 + 20, 92), radius=18, fill=(0, 0, 0))
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((20, 40, w + 20, h + 40), radius=int(w * .16), fill=(0, 0, 0, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(25)); sh.alpha_composite(im)
    return sh

def flag_us(w):
    h = int(w * 0.6); im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    for i in range(13): d.rectangle((0, i * h / 13, w, (i + 1) * h / 13), fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle((0, 0, w * 0.4, h * 7 / 13), fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            x, y = w * 0.4 * (c + 0.5) / 6, h * 7 / 13 * (r + 0.5) / 5
            d.ellipse((x - 3, y - 3, x + 3, y + 3), fill="white")
    return rounded(im, 14)

def star(d, cx, cy, r, rot=0, fill=(255, 222, 0)):
    pts = []
    for i in range(10):
        a = rot + math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(a), cy - rr * math.sin(a)))
    d.polygon(pts, fill=fill)

def flag_cn(w):
    h = int(w * 2 / 3); im = Image.new("RGBA", (w, h), (238, 28, 37, 255)); d = ImageDraw.Draw(im)
    u = h / 20
    star(d, 5 * u, 5 * u, 3 * u)
    for (x, y) in [(10, 2), (12, 4), (12, 7), (10, 9)]:
        star(d, x * u, y * u, u, rot=math.atan2(5 - y, x - 5) - math.pi / 2)
    return rounded(im, 14)

def rounded(im, r):
    m = Image.new("L", im.size); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width, im.height), radius=r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m); return out

def pill(txt, sz, bg, fg=(0, 0, 0), padx=34, pady=18):
    f = font(sz); bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + padx * 2, bb[3] - bb[1] + pady * 2
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), radius=h // 2, fill=bg)
    d.text((padx - bb[0], pady - bb[1]), txt, font=f, fill=fg)
    return im

def cut_alpha(t, dur, fin=0.18, fout=0.15):
    return clamp(t / fin) * clamp((dur - t) / fout)

BG = bg_gradient()
BG2 = bg_gradient((10, 8, 20), (90, 12, 20))

# ================= C1: QWEN title card (full screen)
QW = text_layer("QWEN", 250, glow=(150, 100, 255))
LBL = pill("ALIBABA'S AI MODEL", 54, YELLOW)
NODES = [(random.uniform(80, W - 80), random.uniform(350, 1350)) for _ in range(16)]
def c1(t, dur):
    c = BG.copy(); particles(c, t)
    d = ImageDraw.Draw(c)
    k = out_cubic(t / 0.8)
    for i, (x, y) in enumerate(NODES):  # neural-net lines
        x2, y2 = x + 25 * math.sin(t * 2 + i), y + 25 * math.cos(t * 1.7 + i)
        for j in range(i + 1, len(NODES)):
            xx, yy = NODES[j]
            if math.hypot(xx - x, yy - y) < 330:
                d.line((x2, y2, xx, yy), fill=(140, 120, 255, int(70 * k)), width=2)
        d.ellipse((x2 - 7, y2 - 7, x2 + 7, y2 + 7), fill=(190, 170, 255, int(200 * k)))
    scaled_center(QW, 0.4 + 0.6 * out_back(t / 0.45) + 0.03 * t, W / 2, 860, c)
    scaled_center(LBL, out_back((t - 0.25) / 0.35), W / 2, 1120, c)
    c.putalpha(c.getchannel("A").point(lambda v: int(v * cut_alpha(t, dur))))
    return c

# ================= C2: phone with features appearing
FEATS = ["Siri", "Writing Tools", "Visual Intelligence", "Photo Cleanup"]
FEAT_T = [0.15, 0.82, 1.99, 3.19]  # relative to cutaway start (o 10.45)
PH = phone(560)
HDR = text_layer("Apple Intelligence", 46)
HDR2 = text_layer("CHINA EDITION", 30, fill=(255, 210, 0))
QB = pill("POWERED BY QWEN", 44, YELLOW)
def feat_row(txt):
    im = Image.new("RGBA", (470, 96)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 470, 96), radius=26, fill=(40, 42, 58, 255))
    d.ellipse((22, 24, 70, 72), fill=(52, 199, 89)); d.line((34, 49, 44, 59, 60, 38), fill="white", width=6)
    d.text((90, 48), txt, font=font(36), fill="white", anchor="lm")
    return im
ROWS = [feat_row(f) for f in FEATS]
def c2(t, dur):
    c = BG.copy(); particles(c, t)
    py = 900 + 900 * (1 - out_cubic(t / 0.45))
    tilt = 0
    ph = PH.copy()
    ph.alpha_composite(HDR, (ph.width // 2 - HDR.width // 2, 120))
    ph.alpha_composite(HDR2, (ph.width // 2 - HDR2.width // 2, 185))
    o = orb(150, [(255, 60, 160), (60, 140, 255), (255, 170, 40)])
    ph.alpha_composite(o, (ph.width // 2 - 75, 260))
    for i, (r, ft) in enumerate(zip(ROWS, FEAT_T)):
        k = out_back((t - ft) / 0.3)
        if k > 0.01:
            rr = r.resize((max(1, int(r.width * k)), max(1, int(r.height * k))))
            ph.alpha_composite(rr, (ph.width // 2 - rr.width // 2, 450 + i * 120 + (96 - rr.height) // 2))
    scaled_center(ph, 1.0, W / 2, py, c)
    scaled_center(QB, out_back((t - 3.6) / 0.35), W / 2, 1530, c)
    c.putalpha(c.getchannel("A").point(lambda v: int(v * cut_alpha(t, dur))))
    return c

# ================= C3: calendar + iOS 27.3
def calendar():
    w, h = 460, 500
    im = Image.new("RGBA", (w + 40, h + 40)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, w + 20, h + 20), radius=50, fill=(250, 250, 252))
    d.rounded_rectangle((20, 20, w + 20, 170), radius=50, fill=(235, 60, 60)); d.rectangle((20, 120, w + 20, 170), fill=(235, 60, 60))
    d.text((w / 2 + 20, 95), "DECEMBER", font=font(62), fill="white", anchor="mm")
    d.text((w / 2 + 20, 345), "2026", font=font(150), fill=(30, 30, 40), anchor="mm")
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((20, 40, w + 20, h + 40), radius=50, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(25)); sh.alpha_composite(im); return sh
CAL = calendar()
IOS = text_layer("iOS 27.3", 190, glow=(80, 160, 255))
UPD = pill("SOFTWARE UPDATE", 46, (255, 255, 255))
def c3(t, dur):
    c = BG.copy(); particles(c, t)
    scaled_center(UPD, out_back((t - 0.05) / 0.3), W / 2, 470, c)
    scaled_center(IOS, 0.5 + 0.5 * out_back(t / 0.4), W / 2, 680, c)
    k = out_back((t - 0.35) / 0.4)
    cal = CAL.rotate(-8 * (1 - clamp((t - 0.35) / 0.4)) + 2 * math.sin(t * 3), expand=True, resample=Image.BICUBIC)
    scaled_center(cal, k, W / 2, 1100, c)
    c.putalpha(c.getchannel("A").point(lambda v: int(v * cut_alpha(t, dur))))
    return c

# ================= C4: same iPhone, two different AIs
SAME = text_layer("SAME iPHONE", 110)
DIFF = pill("2 DIFFERENT AIs", 60, YELLOW)
def mini_phone(cols, label):
    p = phone(330)
    o = orb(200, cols); p.alpha_composite(o, (p.width // 2 - 100, 230))
    tl = text_layer(label, 40, pad=10); p.alpha_composite(tl, (p.width // 2 - tl.width // 2, 470))
    return p
P_US = mini_phone([(60, 140, 255), (160, 80, 255), (60, 220, 255)], "AI #1")
P_CN = mini_phone([(255, 120, 30), (255, 50, 70), (255, 200, 40)], "AI #2")
F_US, F_CN = flag_us(220), flag_cn(220)
VS = text_layer("VS", 90, fill=YELLOW)
def c4(t, dur):
    c = BG.copy(); particles(c, t)
    scaled_center(SAME, out_back(t / 0.35), W / 2, 380, c)
    scaled_center(DIFF, out_back((t - 0.2) / 0.35), W / 2, 530, c)
    kl = out_cubic((t - 0.3) / 0.45); kr = out_cubic((t - 0.55) / 0.45)
    fl = 8 * math.sin(t * 2.2)
    if kl > 0:
        scaled_center(P_US, 1, 290 - 700 * (1 - kl), 1080 + fl, c)
        scaled_center(F_US, out_back((t - 0.8) / 0.3), 290, 680, c)
    if kr > 0:
        scaled_center(P_CN, 1, 790 + 700 * (1 - kr), 1080 - fl, c)
        scaled_center(F_CN, out_back((t - 1.05) / 0.3), 790, 680, c)
    scaled_center(VS, out_back((t - 1.2) / 0.3), W / 2, 1080, c)
    c.putalpha(c.getchannel("A").point(lambda v: int(v * cut_alpha(t, dur))))
    return c

# ================= stickers (small, alpha)
SW = 420
def sticker_anim(layer, t, dur, wobble=3):
    c = Image.new("RGBA", (SW, SW))
    k = out_back(t / 0.35) * clamp((dur - t) / 0.2)
    rot = wobble * math.sin(t * 4)
    l = layer.rotate(rot, expand=True, resample=Image.BICUBIC)
    scaled_center(l, k, SW / 2, SW / 2 + 6 * math.sin(t * 3), c)
    return c

ORB_S = orb(300, [(255, 60, 160), (60, 140, 255), (255, 170, 40)])
def s1(t, dur):  # AI orb
    c = Image.new("RGBA", (SW, SW))
    k = out_back(t / 0.35) * clamp((dur - t) / 0.2)
    scaled_center(ORB_S, k * (1 + 0.05 * math.sin(t * 6)), SW / 2, SW / 2 - 30, c)
    lab = pill("AI", 44, (255, 255, 255)); scaled_center(lab, k, SW / 2, SW / 2 + 140, c)
    return c

def flag_sticker():
    f = flag_cn(300); im = Image.new("RGBA", (340, 300)); im.alpha_composite(f, (20, 20))
    lab = pill("CHINA", 40, YELLOW); im.alpha_composite(lab, (170 - lab.width // 2, 200)); return im
FS = flag_sticker()
def s2(t, dur): return sticker_anim(FS, t, dur)

def chip():
    s = 280; im = Image.new("RGBA", (s + 40, s + 40)); d = ImageDraw.Draw(im)
    for i in range(6):
        p = 60 + i * 40
        for (a, b, c_, e) in [(p, 0, p + 14, 50), (p, s - 10, p + 14, s + 40), (0, p, 50, p + 14), (s - 10, p, s + 40, p + 14)]:
            d.rectangle((a, b, c_, e), fill=(200, 170, 80))
    d.rounded_rectangle((40, 40, s, s), radius=30, fill=(30, 30, 40), outline=(255, 200, 60), width=6)
    d.text(((s + 40) / 2, (s + 40) / 2 - 20), "AI", font=font(110), fill=(255, 200, 60), anchor="mm")
    d.text(((s + 40) / 2, (s + 40) / 2 + 65), "QWEN", font=font(36), fill="white", anchor="mm")
    g = im.filter(ImageFilter.GaussianBlur(14)); g.alpha_composite(im); return g
CHIP = chip()
def s3(t, dur): return sticker_anim(CHIP, t, dur, wobble=4)

BELL = emoji_layer("🔔", 230)
def s4(t, dur):
    c = Image.new("RGBA", (SW, SW))
    k = out_back(t / 0.35)
    rot = 18 * math.sin(t * 16) * max(0, 1 - ((t % 1.2) / 0.6))
    l = BELL.rotate(rot, expand=True, resample=Image.BICUBIC)
    scaled_center(l, k, SW / 2, SW / 2, c)
    return c

if __name__ == "__main__":
    import sys
    jobs = {
        "c1": (c1, 4.90 - 2.95, (W, H)), "c2": (c2, 14.85 - 10.45, (W, H)),
        "c3": (c3, 22.35 - 19.70, (W, H)), "c4": (c4, 29.85 - 25.00, (W, H)),
        "s1": (s1, 2.85 - 1.00, (SW, SW)), "s2": (s2, 9.65 - 8.20, (SW, SW)),
        "s3": (s3, 17.05 - 14.95, (SW, SW)), "s4": (s4, 34.56 - 31.10, (SW, SW)),
    }
    for k in (sys.argv[1:] or jobs):
        fn, dur, size = jobs[k]; encode(k, fn, dur, size)
