"""N1 Genie 4 sound: tech bed; world-build riser, rain hiss, footsteps, sound-wave pings, lock click, poll pops."""
import json, numpy as np
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
T = lambda w, n=1: word_time(w, n)[0]
E = lambda w, n=1: word_time(w, n)[1]
ev = json.load(open("hf/events.json")); S0 = ev["split"][0]
write("music.wav", music(TOTAL + 0.2, style="tech", seed=31))
fx = Track(TOTAL + 0.2)
fx.add(impact(), 0.0, 0.6); fx.add(pop(1200), 0.02, 0.5)
fx.add(whoosh(0.4, True), S0 - 0.12, 0.6); fx.add(riser(0.9), S0 + 0.1, 0.5)
for i in range(5): fx.add(pop(600 + 100 * i), S0 + 1.0 + 0.12 * i, 0.45)        # trees pop
fx.add(swish_up(0.25), T("GENIE"), 0.6)
for a, b, s in ((T("MAKE"), E("RAIN"), "make it rain"), (T("ADD"), E("PERSON"), "add a person")):
    for i in range(len(s)): fx.add(click(), a + (b - a) * i / len(s), 0.4)
n = int(SR * 2.0); rain = lp(rng.standard_normal(n), 0.35) * 0.18; rain *= np.minimum(np.arange(n) / (0.2 * SR), 1) * np.minimum((n - np.arange(n)) / (0.4 * SR), 1)
fx.add(rain, T("RAINS") - 0.1, 0.8)
for k in range(int((T("AND") + 0.6 - T("SOMEONE")) / 0.3)): fx.add(click(), T("SOMEONE") + k * 0.3, 0.6)   # footsteps
for k in range(4): fx.add(ding(880 + 220 * k), T("SOUNDS") + k * 0.3, 0.35)
fx.add(stamp(), T("CAN'T"), 0.6); fx.add(pop(900), T("IMAGINE"), 0.6); fx.add(swish_up(0.2), T("WITHOUT"), 0.6)
fx.add(pop(700), T("TRY"), 0.7); fx.add(pop(1000), T("TRY") + 0.12, 0.7)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
