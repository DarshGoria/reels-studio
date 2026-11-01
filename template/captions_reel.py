"""Word-by-word karaoke captions (ASS) for any reel.
usage: captions_reel.py --accent 39FF88 [--split 2.36,15.29 ...] [--margin 400] [--seam-y 900] [-o captions.ass]
Active word = accent colour at 112%, chunk pops in from 90%. Chunks: <=3 words / <=15 chars, break on pauses > 0.3 s
and before sentence-start words (taken from the punctuation in edit/raw.words.json). Inside a --split window the
captions sit on the seam (y = --seam-y) instead of the bottom."""
import argparse, json
from timeline import OW, SPEECH_END, SRC_WORDS

ap = argparse.ArgumentParser()
ap.add_argument("--accent", default="FFE500"); ap.add_argument("--split", action="append", default=[])
ap.add_argument("--margin", type=int, default=400); ap.add_argument("--seam-y", type=int, default=900)
ap.add_argument("--start", type=float, default=0.45, help="no captions before this (hook flash)")
ap.add_argument("-o", default="captions.ass")
a = ap.parse_args()
r, g, b = a.accent[0:2], a.accent[2:4], a.accent[4:6]
ACC = f"&H{b}{g}{r}&"                      # ASS colours are BGR
SPLITS = [tuple(map(float, s.split(","))) for s in a.split]
def in_split(t): return any(s + 0.1 < t < e - 0.1 for s, e in SPLITS)
def ts(x): x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"

ends_sentence = [w["text"].rstrip()[-1:] in ".?!" for w in SRC_WORDS]
chunks, cur = [], []
for i, w in enumerate(OW):
    starts = i > 0 and ends_sentence[i - 1]
    if cur and (starts or len(cur) == 3 or len(" ".join(x[0] for x in cur + [w])) > 15 or w[1] - cur[-1][2] > 0.3):
        chunks.append(cur); cur = []
    cur.append(w)
chunks.append(cur)

ev = []
for ci, ch in enumerate(chunks):
    start = max(ch[0][1], a.start)
    nxt = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else SPEECH_END
    end = min(nxt, ch[-1][2] + 0.35)
    if end <= start: continue
    pos = rf"{{\an5\pos(540,{a.seam_y})}}" if in_split((start + end) / 2) else ""
    for wi, (w, s, e) in enumerate(ch):
        ws = start if wi == 0 else max(s, start)
        we = ch[wi + 1][1] if wi + 1 < len(ch) else end
        if we <= ws: continue
        parts = [(rf"{{\c{ACC}\fscx112\fscy112}}" + x + r"{\c&HFFFFFF&\fscx100\fscy100}") if k == wi else x
                 for k, (x, _, _) in enumerate(ch)]
        pop = r"{\fscx90\fscy90\t(0,80,\fscx100\fscy100)}" if wi == 0 else ""
        ev.append((ws, we, pos + pop + " ".join(parts)))

out = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,98,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,9,4,2,40,40,{a.margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for s, e, t in ev: out += f"Dialogue: 2,{ts(s)},{ts(e)},Cap,,0,0,0,,{t}\n"
open(a.o, "w").write(out)
print(len(chunks), "chunks ->", a.o)
