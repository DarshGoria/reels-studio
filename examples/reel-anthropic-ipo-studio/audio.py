import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return word_time(w, n)[0]
E = json.load(open("events.json")); SC = E["scenes"]
write("music.wav", music(TOTAL + 0.2, style="hype", seed=16))
fx = Track(TOTAL + 0.2)
fx.add(impact(), 0.0, 0.9); fx.add(ding(1568), 0.05, 0.35)
fx.add(chime(), T("PUBLIC") - 0.2, 0.5)                                   # bell ring on "public"
for c in E["cuts"]: fx.add(whoosh(0.35, True), c - 0.2, 0.55)
fx.add(ticks(1.4, 14, 10), T("WEEKS") + 0.2, 0.5)                           # flip-clock countdown
fx.add(swish_up(0.3), SC["s2"][0], 0.5); fx.add(stamp(), T("OCTOBER") - 0.05, 0.9)
fx.add(ticks(0.5, 30, 12), SC["s3"][0] + 0.05, 0.4); fx.add(pop(1200), T("16") - 0.05, 0.6); fx.add(ding(), T("16"), 0.4)
fx.add(riser(0.8), T("BIGGEST") - 0.6, 0.5); fx.add(impact(), T("BIGGEST") + 0.2, 0.7)
for i in range(8): fx.add(pop(900 + 90 * i), SC["s4"][0] + 0.2 + i * 0.3, 0.25)
fx.add(burst(), SC["s5"][0], 0.5); fx.add(click(), T("POST") - 0.05, 0.8); fx.add(ding(1760), T("POST") + 0.05, 0.5)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.4)
write("sfx.wav", fx.buf); print("ok")
