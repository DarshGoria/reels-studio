"""Reel 4 sound: fast tech bed; glitch hook, error buzz, typing clicks, success chime."""
import json
from sound import *
from timeline import word_time, SPEECH_END, TOTAL
T = lambda w, n=1: word_time(w, n)[0]
E = lambda w, n=1: word_time(w, n)[1]
ev = json.load(open("hf/events.json")); P0, P1 = ev["split"]
write("music.wav", music(TOTAL + 0.2, style="tech", seed=7))
fx = Track(TOTAL + 0.2)
fx.add(glitch(0.45), 0.0, 0.7); fx.add(impact(), 0.0, 0.7)
fx.add(buzz(0.3), T("WRONG"), 0.6)
fx.add(whoosh(0.4, True), P0 - 0.12, 0.6)
fx.add(stamp(), T("PROMPTS"), 0.9)
fx.add(pop(), T("ONE"), 0.7)
ty0, ty1 = T("BEFORE"), E("QUESTIONS"); n = len("Before you answer, ask me 5 questions.")
for i in range(n):
    fx.add(click(), ty0 + (ty1 - ty0) * i / n, 0.55)
fx.add(swish_up(0.25), ty1 + 0.12, 0.9)                 # send
for i in range(5): fx.add(pop(700 + 80 * i), T("INTERVIEWS") + i * 0.32, 0.5)
fx.add(riser(0.6), T("SCARY") - 0.3, 0.6); fx.add(chime(), T("ACCURATE"), 0.7)
fx.add(whoosh(0.35, False), P1 - 0.2, 0.5)
fx.add(pop(1000), ev["card1"][0] + 0.05, 0.7)
fx.add(ding(), ev["card2"][0] + 0.3, 0.9)
fx.add(riser(0.45), SPEECH_END - 0.05, 0.5)
write("sfx.wav", fx.buf); print("ok")
