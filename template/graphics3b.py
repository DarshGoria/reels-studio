# reels-studio template — PER-REEL: floating-card versions of the same panels.
"""v3.2 floating cards (full-screen face). Cards sit over the chest area, face stays clear."""
import math
from PIL import Image, ImageDraw, ImageFilter
import graphics3 as g
from graphics3 import (font, YELLOW, clamp, out_back, out_cubic, scaled_center, text_layer, pill, emoji_layer,
                       flag_us, flag_cn, TILE_T, PA0, QWEN_T, PB0, CAL_T, PC0, DIFF_T, CTRY_T, word_time,
                       PA_DUR, PB_DUR, PC_DUR, P_US, P_CN, icon, encode)

CW, CH = 1080, 760          # canvas; overlaid at y=760 -> card centred around y~1140
CARD_W = 960

def glass(h, w=CARD_W):
    """frosted dark card with soft shadow and thin yellow rim"""
    im = Image.new("RGBA", (w + 60, h + 60))
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((30, 42, w + 30, h + 42), radius=46, fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((30, 30, w + 30, h + 30), radius=46, fill=(14, 16, 34, 222), outline=(255, 229, 0, 255), width=4)
    return im

def card_frame(t, dur, draw, h):
    c = Image.new("RGBA", (CW, CH))
    card = glass(h); draw(card, t)
    k_in, k_out = out_back(t / 0.32), out_cubic((dur - t) / 0.22)
    k = min(k_in, k_out)
    bob = 6 * math.sin(t * 2.4)
    scaled_center(card, 0.6 + 0.4 * k if k > 0 else 0, CW / 2, CH / 2 + bob, c, alpha=clamp(min(t / 0.15, (dur - t) / 0.22)))
    return c

# ---- card A: features row + Qwen reveal
def mini_tile(label, kind, col):
    w, h = 205, 190
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), radius=30, fill=(34, 36, 56, 255), outline=col, width=3)
    d.rounded_rectangle((w / 2 - 42, 22, w / 2 + 42, 106), radius=22, fill=col)
    im.alpha_composite(icon(kind, 100).resize((60, 60)), (int(w / 2 - 30), 34))
    d.ellipse((w - 46, 12, w - 14, 44), fill=(52, 199, 89)); d.line((w - 38, 28, w - 32, 34, w - 21, 21), fill="white", width=4)
    d.text((w / 2, 148), label, font=font(30), fill="white", anchor="mm")
    return im
MT = [mini_tile("Siri", "siri", (120, 80, 255)), mini_tile("Writing", "write", (255, 140, 40)),
      mini_tile("Visual AI", "eye", (40, 170, 255)), mini_tile("Cleanup", "spark", (255, 60, 140))]
HA = text_layer("APPLE INTELLIGENCE", 50, pad=10); CN = pill("CHINA", 30, YELLOW)
def brain():
    p = pill("RUNS ON ALIBABA'S QWEN", 42, YELLOW); e = emoji_layer("🧠", 60)
    im = Image.new("RGBA", (p.width + 74, max(p.height, 66))); im.alpha_composite(p, (0, (im.height - p.height) // 2))
    im.alpha_composite(e, (p.width + 10, (im.height - e.height) // 2)); return im
BR = brain()
HA_H = 420
def draw_a(card, t):
    cx = card.width / 2
    scaled_center(HA, out_back(t / 0.3), cx - 70, 95, card)
    scaled_center(CN, out_back((t - 0.1) / 0.3), cx + 300, 95, card)
    for i, (tl, tt) in enumerate(zip(MT, TILE_T)):
        scaled_center(tl, out_back((t - (tt - PA0)) / 0.3), 30 + 125 + i * 237, 235, card)
    k = out_back((t - (QWEN_T - PA0)) / 0.35)
    if k > 0:
        scaled_center(BR, k * (1 + 0.03 * math.sin(t * 8)), cx, 415, card)
def card_a(t, dur): return card_frame(t, dur, draw_a, HA_H + 50)

# ---- card B: iOS 27.3 + calendar
IOS = text_layer("iOS 27.3", 130, glow=(80, 160, 255), pad=20)
UPD = pill("SOFTWARE UPDATE", 34, (255, 255, 255))
CAL = g.CAL.resize((240, 270), Image.LANCZOS)
WHO = pill("iPHONE USERS IN CHINA", 38, YELLOW)
def draw_b(card, t):
    scaled_center(UPD, out_back(t / 0.3), 300, 100, card)
    scaled_center(IOS, 0.5 + 0.5 * out_back((t - 0.05) / 0.4), 330, 215, card)
    kc = out_back((t - (CAL_T - PB0)) / 0.4)
    if kc > 0:
        cal = CAL.rotate(-10 * (1 - clamp(kc)) + 2 * math.sin(t * 3), expand=True, resample=Image.BICUBIC)
        scaled_center(cal, kc, 800, 190, card)
    scaled_center(WHO, out_back((t - (word_time("iPHONE")[0] - PB0)) / 0.3), card.width / 2, 365, card)
def card_b(t, dur): return card_frame(t, dur, draw_b, 400)

# ---- card C: same iPhone, 2 AIs
SAME = text_layer("SAME iPHONE", 70, pad=10); DIFF = pill("2 DIFFERENT AIs", 40, YELLOW)
PUS = P_US.resize((150, int(150 * P_US.height / P_US.width))); PCN = P_CN.resize((150, int(150 * P_CN.height / P_CN.width)))
FU, FC = flag_us(120), flag_cn(120)
VS = text_layer("VS", 70, fill=YELLOW, pad=10)
def draw_c(card, t):
    cx = card.width / 2
    scaled_center(SAME, out_back(t / 0.3), cx, 95, card)
    kl, kr = out_cubic((t - 0.2) / 0.4), out_cubic((t - 0.4) / 0.4)
    if kl > 0: scaled_center(PUS, 1, 170 - 400 * (1 - kl), 320, card, alpha=clamp(kl * 2))
    if kr > 0: scaled_center(PCN, 1, card.width - 170 + 400 * (1 - kr), 320, card, alpha=clamp(kr * 2))
    kf = out_back((t - (CTRY_T - PC0)) / 0.3)
    scaled_center(FU, kf, cx - 150, 270, card); scaled_center(FC, kf, cx + 150, 270, card)
    kd = out_back((t - (DIFF_T - PC0)) / 0.3)
    scaled_center(DIFF, kd, cx, 400, card)
    scaled_center(VS, out_back((t - 0.7) / 0.3) * (1 - 0.0 * kd), cx, 270 if kd <= 0 else 270, card)
def card_c(t, dur): return card_frame(t, dur, draw_c, 460)

JOBS = {"ca": (card_a, PA_DUR, (CW, CH)), "cb": (card_b, PB_DUR, (CW, CH)), "cc": (card_c, PC_DUR, (CW, CH))}

if __name__ == "__main__":
    import sys
    if "--preview" in sys.argv:
        fr = [card_a(PA_DUR - 0.5, PA_DUR), card_a(2.5, PA_DUR), card_b(PB_DUR - 0.4, PB_DUR), card_c(PC_DUR - 0.4, PC_DUR)]
        sh = Image.new("RGB", (540 * 2, 380 * 2), (90, 90, 90))
        for i, f in enumerate(fr):
            b = Image.new("RGBA", f.size, (120, 60, 60, 255)); b.alpha_composite(f)
            sh.paste(b.resize((540, 380)).convert("RGB"), ((i % 2) * 540, (i // 2) * 380))
        sh.save("gfx3b_preview.png")
    else:
        for k in JOBS:
            fn, dur, size = JOBS[k]; encode(k, fn, dur, size)
