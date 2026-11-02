import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return word_time(w, n)[0]
E = json.load(open("events.json")); TW = E["twist"]
write("music.wav", music(TOTAL + 0.2, style="news", seed=7))
fx = Track(TOTAL + 0.2)
fx.add(impact(), 0.0, 0.8); fx.add(swish_up(0.2), T("20%") - 0.2, 0.5)
for t in (T("20%") + 0.3, T("20%") + 0.5): fx.add(pop(1000), t, 0.35)
fx.add(ticks(0.7, 26, 10), T("3%") - 0.45, 0.55); fx.add(ding(), T("3%") + 0.25, 0.5); fx.add(pop(800), T("3%") + 0.1, 0.35)
fx.add(whoosh(0.3, True), T("NOW") - 0.15, 0.4)
fx.add(impact(), T("$300") - 0.15, 0.7); fx.add(burst(), T("BILLION"), 0.4)
for i in range(4): fx.add(pop(900 + 120 * i), T("FIX") - 0.1 + 0.12 * i, 0.3)
fx.add(glitch(0.4), TW - 0.1, 0.8); fx.add(stamp(), TW + 0.15, 0.8); fx.add(impact(), TW, 0.6)
fx.add(swish_up(0.3), T("REPORT") - 0.1, 0.45)
fx.add(whoosh(0.3), T("AI") - 0.15, 0.4); fx.add(ticks(0.9, 30, 8), T("20%", 2) - 0.2, 0.5); fx.add(buzz(0.25), T("USED"), 0.45)
fx.add(whoosh(0.35, True), T("REAL") - 0.1, 0.5); fx.add(chime(), T("SERVICES"), 0.45)
fx.add(riser(0.5), T("SHOULD") - 0.5, 0.4); fx.add(impact(), T("SHOULD") - 0.05, 0.6)
fx.add(pop(1100), T("BUILD") - 0.1, 0.4); fx.add(pop(1300), T("WORKFORCE") - 0.6, 0.4); fx.add(burst(), T("WORKFORCE"), 0.5)
fx.add(click(), T("OR") - 0.1, 0.5)
write("sfx.wav", fx.buf); print("ok")
