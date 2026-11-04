import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return word_time(w, n)[0]
E = json.load(open("events.json")); S = E["scenes"]
write("music.wav", music(TOTAL + 0.2, style="tense", seed=26))
fx = Track(TOTAL + 0.2)
fx.add(whoosh(0.25, True), 0.0, 0.6); fx.add(impact(), 0.2, 0.8)
fx.add(pop(1000), T("AI") - 0.1, 0.4); fx.add(pop(1200), T("AI") + 0.15, 0.4); fx.add(stamp(), T("WEIRD") - 0.15, 0.6)
for c in E["cuts"] + [E["s1"][0]]: fx.add(whoosh(0.35, True), c - 0.2, 0.5)
fx.add(ticks(0.9, 26, 10), T("80") - 0.2, 0.45); fx.add(ding(), T("80") + 0.7, 0.4)
for i in range(12): fx.add(pop(800 + 40 * i), T("AI", 2) - 0.2 + 0.07 * i, 0.18)
fx.add(stamp(), T("DIDN'T"), 0.7)
for w in ("TEXTING", "HAVING", "CONVERSATIONS"): fx.add(ding(1568), T(w), 0.35)
fx.add(pop(1300), T("ONE"), 0.5); fx.add(chime(), T("FIVE"), 0.4); fx.add(pop(1100), T("ASK"), 0.4)
fx.add(riser(0.6), T("TWIST") - 0.6, 0.5); fx.add(impact(), T("TWIST") - 0.05, 0.8)
fx.add(ticks(1.4, 20, 9), T("CANDIDATE", 2), 0.35); fx.add(glitch(0.6), T("DEEP") - 0.05, 0.9); fx.add(alert(), T("DEEP"), 0.45)
fx.add(impact(), T("WON") - 0.05, 0.8); fx.add(burst(), T("WON"), 0.5); fx.add(ding(1760), T("7"), 0.45)
fx.add(swish_up(0.3), E["s2"][0], 0.5); fx.add(click(), T("COMMENT"), 0.7)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
