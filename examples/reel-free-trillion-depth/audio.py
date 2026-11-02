"""N2 depth edit sound: tense-cinematic bed; deep boom per depth word, glitch on the catch, ticks on the RAM bar."""
import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
T = lambda w, n=1: word_time(w, n)[0]
ev = json.load(open("events.json")); B, F = ev["back"], ev["front"]
write("music.wav", music(TOTAL + 0.2, style="tense", seed=42))
fx = Track(TOTAL + 0.2)
fx.add(impact(), 0.0, 0.9)                                    # FREE lands on frame 0
fx.add(swish_up(0.2), 0.15, 0.5)
fx.add(whoosh(0.35, True), F["name"][0] - 0.1, 0.5)
fx.add(impact(), T("TRILLION"), 0.8)
fx.add(pop(1000), F["biz"][0], 0.6)
fx.add(glitch(0.45), T("CATCH") - 0.3, 0.8); fx.add(stamp(), T("CATCH"), 0.7)
fx.add(impact(), T("500"), 0.8); fx.add(ticks(0.9, 30, 8), T("500"), 0.6)
fx.add(buzz(0.25), T("16"), 0.5)
fx.add(pop(800), F["tag"][0], 0.7); fx.add(ding(), F["tag"][0] + 0.25, 0.5)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
