import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return word_time(w, n)[0]
E = json.load(open("events.json")); S = E["scenes"]
write("music.wav", music(TOTAL + 0.2, style="news", seed=9))
fx = Track(TOTAL + 0.2)
fx.add(whoosh(0.25, True), 0.0, 0.6); fx.add(impact(), 0.2, 0.8); fx.add(alert(), 0.35, 0.35)
for i, t in enumerate((T("CHARGING") - 0.6 + k * 0.25 for k in range(4))): fx.add(pop(900 + 120 * i), t, 0.35)
for c in E["cuts"] + [E["split"][0]]: fx.add(whoosh(0.35, True), c - 0.2, 0.5)
fx.add(ticks(1.2, 12, 10), S["year"][0] + 0.3, 0.45); fx.add(stamp(), T("CLAIMED") - 0.1, 0.8)
fx.add(swish_up(0.3), S["nov"][0], 0.5); fx.add(snip(), T("NOVEMBER"), 0.5); fx.add(alert(), T("4TH") + 0.2, 0.55)
for i in range(3): fx.add(ding(1320 - 110 * i), S["debit"][0] + 0.3 + i * 0.45, 0.45)
fx.add(buzz(0.25), T("AUTOMATICALLY"), 0.4)
for w in ("SETTINGS", "ACCOUNT", "MANAGE"): fx.add(click(), T(w), 0.7)
fx.add(pop(1300), T("CHECK"), 0.5); fx.add(click(), T("CANCEL") + 0.25, 0.8); fx.add(burst(), T("CANCEL") + 0.4, 0.6); fx.add(chime(), T("CANCEL") + 0.45, 0.45)
fx.add(swish_up(0.4), S["send"][0], 0.6); fx.add(pop(1100), T("FRIEND") - 0.1, 0.4)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
