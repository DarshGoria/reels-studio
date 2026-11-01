# reels-studio template — PER-REEL: hook headline (HK_TXT*), panels A/B/C content + trigger words, poll text. Helpers are generic.
"""v3 graphics: hook flash + loop tail, split-screen top panels, poll CTA."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
from graphics import (W, H, FPS, font, YELLOW, clamp, out_back, out_cubic, scaled_center, text_layer,
                      emoji_layer, bg_gradient, particles, orb, phone, flag_us, flag_cn, pill, rounded,
                      c1, s1, s2, s4, calendar)
from timeline import word_time, SPEECH_END, TOTAL, LOOP_TAIL

os.makedirs("anims3", exist_ok=True)
PW, PH = 1080, 960  # top panel

def encode(name, fn, dur, size):
    n = int(round(dur * FPS))
    tmp = f"anims3/{name}.tmp.mov"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{size[0]}x{size[1]}",
                          "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(fn(i / FPS, dur).convert("RGBA").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f"anims3/{name}.mov")
    print("rendered", name, n)

PBG = bg_gradient()
PBG = PBG.crop((0, 300, PW, 300 + PH))

def panel_frame(t, dur, draw):
    """top-half panel that slides down in and back up out; yellow divider at the bottom edge"""
    c = PBG.copy(); particles(c, t); draw(c, t)
    d = ImageDraw.Draw(c); d.rectangle((0, PH - 8, PW, PH), fill=YELLOW)
    full = Image.new("RGBA", (W, H))
    k_in, k_out = out_cubic(t / 0.25), out_cubic((dur - t) / 0.22)
    y = int(-PH * (1 - min(k_in, k_out)))
    full.alpha_composite(c, (0, y))
    return full

# ---------- hook flash / loop tail composition
HK_TXT = text_layer("APPLE DID", 135); HK_TXT2 = text_layer("WHAT?!", 170, fill=YELLOW)
HK_EMO = emoji_layer("😳", 170)
P_US = phone(300); P_CN = phone(300)
for p, cols in ((P_US, [(60, 140, 255), (160, 80, 255), (60, 220, 255)]), (P_CN, [(255, 120, 30), (255, 50, 70), (255, 200, 40)])):
    o = orb(190, cols); p.alpha_composite(o, (p.width // 2 - 95, 220))
F_US, F_CN = flag_us(200), flag_cn(200)
VS = text_layer("VS", 90, fill=YELLOW)
def hook_comp(t=0):
    c = bg_gradient(); particles(c, t)
    scaled_center(HK_TXT, 1, W / 2, 380, c)
    scaled_center(HK_TXT2, 1, W / 2 - 95, 560, c)
    scaled_center(HK_EMO, 1, W / 2 + 345, 560, c)
    scaled_center(F_US, 1, 300, 880, c); scaled_center(F_CN, 1, 780, 880, c)
    scaled_center(P_US, 1, 300, 1280, c); scaled_center(P_CN, 1, 780, 1280, c)
    scaled_center(VS, 1, W / 2, 1280, c)
    return c
HOOK = hook_comp()
def zoomed(img, z):
    w, h = int(W * z), int(H * z)
    big = img.resize((w, h), Image.LANCZOS)
    return big.crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))
def hook_flash(t, dur):
    c = zoomed(HOOK, 1.12 - 0.12 * out_cubic(t / dur))
    if t > dur - 0.12:  # quick white flash into the face shot
        a = (t - (dur - 0.12)) / 0.12
        c = Image.blend(c, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.6 * a)
        c.putalpha(int(255 * (1 - a * 0.9)))
    return c
def loop_tail(t, dur):  # ends on exactly the hook's first frame -> seamless replay
    c = zoomed(HOOK, 1.0 + 0.12 * out_cubic(t / dur))
    c.putalpha(int(255 * clamp(t / 0.12)))
    return c

# ---------- panel A: Apple Intelligence features (2x2 tiles)
def icon(kind, s=110):
    im = Image.new("RGBA", (s, s)); d = ImageDraw.Draw(im)
    if kind == "siri":
        for i, hh in enumerate((30, 60, 90, 60, 30)):
            x = 15 + i * 20; d.rounded_rectangle((x, s / 2 - hh / 2, x + 12, s / 2 + hh / 2), radius=6, fill=(255, 255, 255))
    elif kind == "write":
        d.polygon([(25, 85), (30, 65), (75, 20), (90, 35), (45, 80)], fill="white"); d.line((20, 95, 90, 95), fill="white", width=5)
    elif kind == "eye":
        d.ellipse((10, 30, 100, 80), outline="white", width=7); d.ellipse((40, 40, 70, 70), fill="white")
    else:  # sparkle cleanup
        for cx, cy, r in ((50, 55, 34), (85, 25, 14), (85, 85, 10)):
            d.polygon([(cx, cy - r), (cx + r * .28, cy - r * .28), (cx + r, cy), (cx + r * .28, cy + r * .28),
                       (cx, cy + r), (cx - r * .28, cy + r * .28), (cx - r, cy), (cx - r * .28, cy - r * .28)], fill="white")
    return im
def tile(label, kind, col):
    w, h = 450, 230
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), radius=36, fill=(30, 32, 48, 245), outline=col, width=4)
    d.rounded_rectangle((28, 28, 128, 128), radius=26, fill=col)
    ic = icon(kind, 100).resize((70, 70)); im.alpha_composite(ic, (43, 43))
    d.ellipse((w - 80, 30, w - 30, 80), fill=(52, 199, 89)); d.line((w - 67, 55, w - 58, 64, w - 42, 45), fill="white", width=6)
    d.text((30, 185), label, font=font(40), fill="white", anchor="lm")
    return im
TILES = [tile("Siri", "siri", (120, 80, 255)), tile("Writing Tools", "write", (255, 140, 40)),
         tile("Visual Intelligence", "eye", (40, 170, 255)), tile("Photo Cleanup", "spark", (255, 60, 140))]
PA0 = word_time("SIRI", 2)[0] - 0.12
TILE_T = [word_time("SIRI", 2)[0], word_time("WRITING")[0], word_time("VISUAL")[0], word_time("PHOTO")[0]]
QWEN_T = word_time("ALIBABA'S", 2)[0]
HDRA = text_layer("APPLE INTELLIGENCE", 64); CHN = pill("CHINA EDITION", 36, YELLOW)
BRAIN = pill("RUNS ON QWEN  🧠", 46, YELLOW)
BRAIN = Image.new("RGBA", (1, 1))
def brain_pill():
    p = pill("RUNS ON ALIBABA'S QWEN", 44, YELLOW)
    e = emoji_layer("🧠", 64)
    im = Image.new("RGBA", (p.width + 80, max(p.height, 70))); im.alpha_composite(p, (0, (im.height - p.height) // 2))
    im.alpha_composite(e, (p.width + 12, (im.height - e.height) // 2)); return im
BRAIN = brain_pill()
def draw_a(c, t):
    scaled_center(HDRA, out_back(t / 0.3), PW / 2, 120, c)
    scaled_center(CHN, out_back((t - 0.1) / 0.3), PW / 2, 205, c)
    for i, (tl, tt) in enumerate(zip(TILES, TILE_T)):
        k = out_back((t - (tt - PA0)) / 0.3)
        x = 290 if i % 2 == 0 else 790; y = 400 + (i // 2) * 255
        scaled_center(tl, k, x, y, c)
    k = out_back((t - (QWEN_T - PA0)) / 0.35)
    if k > 0:
        dim = Image.new("RGBA", (PW, PH), (0, 0, 0, int(120 * clamp(k)))); c.alpha_composite(dim)
        scaled_center(BRAIN, k * (1 + 0.03 * math.sin(t * 8)), PW / 2, 520, c)
PA_DUR = word_time("BRAIN")[1] + 0.25 - PA0
def panel_a(t, dur): return panel_frame(t, dur, draw_a)

# ---------- panel B: iOS 27.3 + December
PB0 = word_time("iOS")[0] - 0.15
CAL_T = word_time("DECEMBER")[0]
IOS = text_layer("iOS 27.3", 140, glow=(80, 160, 255)); UPD = pill("SOFTWARE UPDATE", 40, (255, 255, 255))
CAL = calendar().resize((330, 370), Image.LANCZOS)
def draw_b(c, t):
    scaled_center(UPD, out_back(t / 0.3), PW / 2, 150, c)
    k = out_back((t - 0.1) / 0.4)
    kc = out_back((t - (CAL_T - PB0)) / 0.4)
    x = PW / 2 - 210 * clamp(kc)  # iOS text slides left when calendar arrives
    scaled_center(IOS, 0.5 + 0.5 * k, x, 470, c)
    if kc > 0:
        cal = CAL.rotate(-10 * (1 - clamp(kc)) + 2 * math.sin(t * 3), expand=True, resample=Image.BICUBIC)
        scaled_center(cal, kc, 855, 480, c)
    # chip strip: who gets it
    k2 = out_back((t - (word_time("iPHONE")[0] - PB0)) / 0.3)
    scaled_center(pill("iPHONE USERS IN CHINA", 42, YELLOW), k2, PW / 2, 790, c)
PB_DUR = min(word_time("CHINA", 2)[1] + 0.25, word_time("SO")[0] - 0.12 + 0.1) - PB0
def panel_b(t, dur): return panel_frame(t, dur, draw_b)

# ---------- panel C: same iPhone, 2 different AIs
PC0 = word_time("SO")[0] - 0.12
SAME = text_layer("SAME iPHONE", 100); DIFF = pill("2 DIFFERENT AIs", 54, YELLOW)
DIFF_T, CTRY_T = word_time("DIFFERENT")[0], word_time("COUNTRY")[0]
PUS, PCN = P_US.resize((200, int(200 * P_US.height / P_US.width))), P_CN.resize((200, int(200 * P_CN.height / P_CN.width)))
FU, FC = flag_us(170), flag_cn(170)
def draw_c(c, t):
    scaled_center(SAME, out_back(t / 0.3), PW / 2, 110, c)
    kl, kr = out_cubic((t - 0.25) / 0.4), out_cubic((t - 0.45) / 0.4)
    fl = 8 * math.sin(t * 2.2)
    if kl > 0: scaled_center(PUS, 1, 260 - 600 * (1 - kl), 620 + fl, c)
    if kr > 0: scaled_center(PCN, 1, 820 + 600 * (1 - kr), 620 - fl, c)
    scaled_center(DIFF, out_back((t - (DIFF_T - PC0)) / 0.3), PW / 2, 225, c)
    kf = out_back((t - (CTRY_T - PC0)) / 0.3)
    scaled_center(FU, kf * 0.8, 260, 340, c); scaled_center(FC, kf * 0.8, 820, 340, c)
    scaled_center(VS, out_back((t - 0.8) / 0.3), PW / 2, 620, c)
PC_DUR = word_time("IN", 3)[1] + 0.2 - PC0
def panel_c(t, dur): return panel_frame(t, dur, draw_c)

# ---------- poll CTA sticker (Instagram-poll look, original)
POLL_T0 = word_time("WOULD")[0] - 0.05
POLL_DUR = word_time("FOLLOW")[0] - POLL_T0
def poll_card():
    w, h = 760, 330
    im = Image.new("RGBA", (w + 40, h + 40)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, w + 20, h + 20), radius=40, fill=(255, 255, 255))
    d.text((w / 2 + 20, 90), "WOULD YOU TRUST IT?", font=font(50), fill=(20, 20, 30), anchor="mm")
    for i, (lab, col) in enumerate((("YES", (52, 199, 89)), ("NO", (255, 69, 58)))):
        x0 = 50 + i * 370
        d.rounded_rectangle((x0, 160, x0 + 330, 300), radius=30, fill=col)
        d.text((x0 + 165, 230), lab, font=font(64), fill="white", anchor="mm")
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((20, 34, w + 20, h + 34), radius=40, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(20)); sh.alpha_composite(im); return sh
POLL = poll_card()
HAND = emoji_layer("👇", 120)
def poll(t, dur):
    c = Image.new("RGBA", (840, 520))
    k = out_back(t / 0.35) * clamp((dur - t) / 0.2)
    scaled_center(POLL.rotate(-3 + 1.5 * math.sin(t * 3), expand=True, resample=Image.BICUBIC), k, 420, 200, c)
    scaled_center(HAND, k, 420, 430 + 15 * math.sin(t * 7), c)
    return c

JOBS = {
    "hook": (hook_flash, 0.45, (W, H)),
    "tail": (loop_tail, LOOP_TAIL, (W, H)),
    "c1": (c1, word_time("QWEN")[1] + 0.12 - (word_time("ALIBABA'S")[0] - 0.08), (W, H)),
    "pa": (panel_a, PA_DUR, (W, H)), "pb": (panel_b, PB_DUR, (W, H)), "pc": (panel_c, PC_DUR, (W, H)),
    "s1": (s1, word_time("ALIBABA'S")[0] - 0.1 - (word_time("CHINESE")[0] - 0.05), (420, 420)),
    "s2": (s2, PA0 - (word_time("CHINA")[0] - 0.08), (420, 420)),
    "s4": (s4, SPEECH_END - (word_time("FOLLOW")[0] - 0.05), (420, 420)),
    "poll": (poll, POLL_DUR, (840, 520)),
}
STARTS = {"hook": 0, "tail": SPEECH_END, "c1": word_time("ALIBABA'S")[0] - 0.08, "pa": PA0, "pb": PB0, "pc": PC0,
          "s1": word_time("CHINESE")[0] - 0.05, "s2": word_time("CHINA")[0] - 0.08,
          "s4": word_time("FOLLOW")[0] - 0.05, "poll": POLL_T0}

if __name__ == "__main__":
    import json
    json.dump({k: [STARTS[k], JOBS[k][1]] for k in JOBS}, open("anims3/times.json", "w"), indent=1)
    if "--preview" in sys.argv:
        fr = [hook_flash(0, .45), panel_frame(PA_DUR - 0.4, PA_DUR, draw_a), panel_frame(2.0, PA_DUR, draw_a),
              panel_frame(PB_DUR - 0.4, PB_DUR, draw_b), panel_frame(PC_DUR - 0.4, PC_DUR, draw_c)]
        sh = Image.new("RGB", (270 * 6, 480), "white")
        for i, f in enumerate(fr):
            b = Image.new("RGBA", f.size, (90, 90, 90, 255)); b.alpha_composite(f); sh.paste(b.resize((270, 480)).convert("RGB"), (i * 270, 0))
        p = poll(1, 2); b = Image.new("RGBA", p.size, (90, 90, 90, 255)); b.alpha_composite(p); sh.paste(b.resize((270, 167)).convert("RGB"), (5 * 270, 0))
        sh.save("gfx3_preview.png")
    else:
        for k in (sys.argv[1:] or JOBS): encode(k, *JOBS[k])
