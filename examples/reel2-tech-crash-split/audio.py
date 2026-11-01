"""Reel 2 (split) sound: tense minor bed; stock-alert beeps, counter ticks, snip, bubble pop."""
import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
T = lambda w, n=1: word_time(w, n)[0]
E = lambda w, n=1: word_time(w, n)[1]
ev = json.load(open("hf/events.json")); SC = ev["scenes"]
write("music.wav", music(TOTAL + 0.2, style="tense", seed=5))
fx = Track(TOTAL + 0.2)
fx.add(alert(2), 0.0, 0.7); fx.add(impact(), 0.0, 0.8)
fx.add(whoosh(0.4, True), 0.18, 0.5)                                 # panel drops in under the hook
fx.add(ticks(E("TRILLION") - T("LOST")), T("LOST"), 0.8)             # counter to $1T
fx.add(stamp(), T("DAY"), 0.9)
for k in ("s2", "s3", "s4", "s5", "s6"): fx.add(whoosh(0.3, False), SC[k][0] - 0.1, 0.35)
fx.add(riser(0.5), T("MUCH") - 0.4, 0.5)
fx.add(ticks(E("BILLION") - T("OVER"), 20, 6), T("OVER"), 0.7)       # counter to $800B (decelerating)
fx.add(pop(800), T("DATA"), 0.7); fx.add(pop(1000), T("CHIPS"), 0.7)
fx.add(snip(), T("CUT"), 0.9)
fx.add(pop(600), T("30") - 0.05, 0.6); fx.add(swish_up(0.2), T("20") - 0.1, 0.8); fx.add(stamp(), T("20"), 0.6)
fx.add(swish_up(T("POP") - T("IS")), T("IS"), 0.4)                   # bubble stretching
fx.add(burst(), T("POP"), 1.0)
fx.add(pop(700), T("YES"), 0.7); fx.add(pop(900), T("NO"), 0.7); fx.add(ding(), T("COMMENTS"), 0.7)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.5)
write("sfx.wav", fx.buf); print("ok")
