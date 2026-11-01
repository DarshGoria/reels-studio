# reels-studio template — PER-REEL: title() texts and the sentence-start break words.
"""Word-by-word karaoke captions + titles (ASS)."""
import json
from timeline import OW, SPEECH_END, TOTAL

T = json.load(open("anims3/times.json"))
SPLITS = [(T["pa"][0], T["pa"][0] + T["pa"][1]), (T["pb"][0], T["pc"][0] + T["pc"][1])]
import sys
NOSPLIT = "--nosplit" in sys.argv
def in_split(t): return (not NOSPLIT) and any(a + 0.1 < t < b - 0.1 for a, b in SPLITS)

def ts(x):
    x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"

# chunk words: max 3 words / 15 chars, break on pauses > 0.3s
chunks, cur = [], []
for i, w in enumerate(OW):
    if cur and (w[0] in ("WOULD", "COMMENT", "FOLLOW", "SO", "IT", "THAT", "ALIBABA'S", "IS", "ALL", "FOR") or len(cur) == 3 or len(" ".join(x[0] for x in cur + [w])) > 15 or w[1] - cur[-1][2] > 0.3):
        chunks.append(cur); cur = []
    cur.append(w)
chunks.append(cur)

ev = []
for ci, ch in enumerate(chunks):
    start = max(ch[0][1], 0.45)
    nxt = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else SPEECH_END
    end = min(nxt, ch[-1][2] + 0.35)
    pos = r"{\an5\pos(540,900)}" if in_split((start + end) / 2) else ""
    for wi, (w, s, e) in enumerate(ch):
        ws = start if wi == 0 else s
        we = ch[wi + 1][1] if wi + 1 < len(ch) else end
        if we <= ws: continue
        parts = []
        for k, (x, _, _) in enumerate(ch):
            if k == wi:
                parts.append(r"{\c&H00E5FF&\fscx112\fscy112}" + x + r"{\c&HFFFFFF&\fscx100\fscy100}")
            else:
                parts.append(x)
        pop = r"{\fscx90\fscy90\t(0,80,\fscx100\fscy100)}" if wi == 0 else ""
        ev.append((2, ws, we, "Cap", pos + pop + " ".join(parts)))

def title(s, e, txt, style="Title"):
    ev.append((1, s, e, style, r"{\fscx70\fscy70\t(0,120,\fscx100\fscy100)}" + txt))
title(0.45, T["c1"][0], "APPLE × ALIBABA?!")
title(T["c1"][0] + T["c1"][1], T["pa"][0], "QWEN = ALIBABA'S AI", "Title2")
title(T["pa"][0] + T["pa"][1], T["pb"][0], "ROLLING OUT SOON", "Title2")
title(T["s4"][0], SPEECH_END, "FOLLOW FOR DAILY AI", "Title2")

ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,98,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,9,4,2,40,40,400,1
Style: Title,Poppins,92,&H00000000,&H00000000,&H0000E5FF,&H0000E5FF,-1,0,0,0,100,100,0,0,3,18,0,8,60,60,250,1
Style: Title2,Poppins,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,3,18,0,8,60,60,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for layer, s, e, st, txt in sorted(ev, key=lambda x: x[1]):
    ass += f"Dialogue: {layer},{ts(s)},{ts(e)},{st},,0,0,0,,{txt}\n"
open("overlay3b.ass" if NOSPLIT else "overlay3.ass", "w").write(ass)
json.dump(SPLITS, open("splits.json", "w"))
print(len(chunks), "caption chunks;", "splits", SPLITS)
