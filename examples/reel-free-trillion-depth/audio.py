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
T2 = lambda w, n=1: word_time(w, n)[0]
for t in (0.5, 0.7, T2("FREE"), T2("FREE") + 0.25): fx.add(pop(900 + int(t * 50) % 400), t, 0.35)
fx.add(swish_up(0.25), T2("CHONK") - 0.3, 0.45); fx.add(ticks(0.8, 24, 9), T2("TRILLION") - 0.05, 0.4)
fx.add(burst(), T2("BUSINESS") - 0.05, 0.55); fx.add(snip(), T("CATCH") - 0.3, 0.5); fx.add(snip(), T("CATCH") - 0.2, 0.5)
fx.add(whoosh(0.3, True), T("YOU'D"), 0.45); fx.add(pop(700), T("LAPTOP") - 0.1, 0.4)
for i in range(3): fx.add(pop(1100 + 150 * i), T("TAG") + 0.1 + 0.25 * i, 0.35)
for t in [5.088, 7.459, 9.1, 13.201]: fx.add(whoosh(0.3), t, 0.3)
write("sfx.wav", fx.buf); print("ok")
