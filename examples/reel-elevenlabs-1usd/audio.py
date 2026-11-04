import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return word_time(w, n)[0]
E = json.load(open("events.json")); S = E["scenes"]
write("music.wav", music(TOTAL + 0.2, style="tech", seed=21))
fx = Track(TOTAL + 0.2)
fx.add(whoosh(0.25, True), 0.0, 0.6); fx.add(impact(), 0.2, 0.8)
for i in range(4): fx.add(pop(900 + 120 * i), T("CLONE") + 0.25 * i, 0.35)
for c in E["cuts"] + [E["split"][0]]: fx.add(whoosh(0.35, True), c - 0.2, 0.5)
fx.add(snip(), T("$1", 2) - 0.25, 0.6); fx.add(impact(), T("$1", 2), 0.6); fx.add(stamp(), T("FIRST"), 0.6)
fx.add(swish_up(0.3), S["date"][0], 0.5); fx.add(alert(), T("ENDS"), 0.45); fx.add(ticks(0.5, 20, 10), T("8"), 0.4)
for w in ("30", "COMMERCIAL", "INSTANT"): fx.add(swish_up(0.2), T(w) - 0.1, 0.35); fx.add(ding(1320), T(w) + 0.2, 0.4)
fx.add(riser(0.6), T("MINUTE") - 0.2, 0.35); fx.add(glitch(0.3), T("TALKS") - 0.15, 0.5); fx.add(chime(), T("EXACTLY"), 0.45)
fx.add(buzz(0.25), T("$6", 2), 0.45); fx.add(click(), T("MONTH", 2), 0.8); fx.add(burst(), T("2") + 0.1, 0.5)
fx.add(pop(1100), T("SAVE"), 0.5); fx.add(pop(1300), T("SEND"), 0.5); fx.add(whoosh(0.4, True), T("YOUTUBE") + 0.3, 0.5)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
