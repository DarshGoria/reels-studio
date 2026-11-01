"""Reel 3 sound: calm minimal bed; stamps and swishes on the debate beats."""
import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
T = lambda w, n=1: word_time(w, n)[0]
ev = json.load(open("hf/events.json"))["cards"]
write("music.wav", music(TOTAL + 0.2, style="calm", seed=11))
fx = Track(TOTAL + 0.2)
fx.add(impact(), 0.0, 0.9); fx.add(whoosh(0.35, False), 0.3, 0.5)
for k, (s, e) in ev.items():
    fx.add(pop(800 if k != "c5" else 600), s + 0.05, 0.6)
fx.add(swish_up(0.25), T("SAKE"), 0.9)                 # strike-through
fx.add(stamp(), T("AI", 3), 0.8)                        # NOT HAPPENING
fx.add(whoosh(0.4, True), T("REPLACE") - 0.1, 0.5)     # robot moves in
fx.add(stamp(), T("APPS"), 0.8)                         # Apple: NO
fx.add(chime(), T("DEEPLY"), 0.6)                       # deeply human
fx.add(whoosh(0.45, False), T("REPLACE", 2), 0.6)      # apps fly into the agent
fx.add(pop(1100), T("APPS", 2), 0.7)
fx.add(pop(700), T("APPLE", 2) - 0.1, 0.7); fx.add(pop(900), T("COMPANIES") - 0.4, 0.7)
fx.add(ding(), T("COMMENT"), 0.7)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.5)
write("sfx.wav", fx.buf); print("ok")
