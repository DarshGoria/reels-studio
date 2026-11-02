"""Reel 3 'India #2 at AI shopping' sound: bright news bed; counter ticks, bar pops, typing clicks, save stamp."""
import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
T = lambda w, n=1: word_time(w, n)[0]
E = lambda w, n=1: word_time(w, n)[1]
ev = json.load(open("hf/events.json")); C = ev["cards"]
write("music.wav", music(TOTAL + 0.2, style="news", seed=21))
fx = Track(TOTAL + 0.2)
fx.add(impact(), 0.0, 0.6); fx.add(pop(1100), 0.02, 0.6)              # hook sticker lands on frame 0
fx.add(swish_up(0.25), 2.0, 0.5)                                       # save chip slides in
for k in ("c1", "c2", "c3", "c4"): fx.add(whoosh(0.3, True), C[k][0] - 0.12, 0.45)
fx.add(ticks(0.8, 30, 10), T("76%"), 0.7)                              # 76% counter
for i in range(3): fx.add(pop(700 + 120 * i), C["c2"][0] + 0.15 + 0.15 * i, 0.6)
fx.add(ding(1568), T("ONLY"), 0.5)                                     # #2 badge
ty0, ty1 = T("COMPARE"), E("TABLE"); n = len("Compare these 3 phones under ₹25,000 for camera & battery. Give me a table.")
for i in range(n): fx.add(click(), ty0 + (ty1 - ty0) * i / n, 0.4)
for i in range(3): fx.add(pop(900), C["c4"][0] + 0.1 + 0.12 * i, 0.5)
fx.add(stamp(), T("SAVE"), 0.9)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
