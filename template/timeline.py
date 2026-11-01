# reels-studio template — PER-REEL: disp() display fixes for brand words (iOS, iPHONE). Everything else is generic.
"""Shared timeline for v3: cut list, 1.1x speed, word timings mapped to output time."""
import json

SPEED = 1.10
SRC_DUR = 41.90
HOOK_FLASH = 0.45     # graphic flash over the first moments (overlaps speech, adds no time)
LOOP_TAIL = 0.45      # end card that flows back into the hook

SRC_WORDS = json.load(open("edit/raw.words.json"))["words"]
def disp(t):
    c = t.strip(".,!?;:")
    return {"iOS": "iOS", "iPhone": "iPHONE"}.get(c, c.upper())
WORDS = [[disp(w["text"]), w["start"], w["end"]] for w in SRC_WORDS]

# --- keep ranges from word timing: merge gaps < 0.26s, pad 0.06s
PAD, MERGE = 0.06, 0.26
keep = []
for _, s, e in WORDS:
    s, e = max(0, s - PAD), min(SRC_DUR, e + PAD)
    if keep and s - keep[-1][1] < MERGE:
        keep[-1][1] = max(keep[-1][1], e)
    else:
        keep.append([s, e])

import os
FR = json.load(open("seg_frames.json")) if os.path.exists("seg_frames.json") else None
def out_t(x):
    acc = 0.0
    for i, (a, b) in enumerate(keep):
        segd = FR[i] / 30 if FR else (b - a) / SPEED
        if x < a: return acc
        if x <= b: return acc + min((x - a) / SPEED, segd)
        acc += segd
    return acc

SPEECH_END = out_t(SRC_DUR)
TOTAL = SPEECH_END + LOOP_TAIL
OW = [[w, out_t(s), out_t(e)] for w, s, e in WORDS]

def word_time(word, nth=1):
    c = 0
    for w, s, e in OW:
        if w == word:
            c += 1
            if c == nth: return s, e
    raise KeyError(word)

if __name__ == "__main__":
    print("segments", len(keep), "speech %.2fs total %.2fs" % (SPEECH_END, TOTAL))
    print(" ".join(f"{w}@{s:.2f}" for w, s, e in OW))
