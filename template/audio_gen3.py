# reels-studio template — PER-REEL: SFX cue words at the bottom. Music generator is generic.
"""Original background beat + SFX, synthesized from scratch."""
import numpy as np, wave

SR = 48000
DUR = 31.6
N = int(SR * DUR)
rng = np.random.default_rng(3)

def write(name, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(name, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)

def add(buf, x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += x * g

def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a * (x[i] - s); y[i] = s
    return y

# ---------------- music: 104 BPM, Am - F - C - G, chill tech/lo-fi
BPM = 104; beat = 60 / BPM; bar = beat * 4
music = np.zeros(N)

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 0.9
def clap():
    n = int(0.25 * SR); x = rng.standard_normal(n)
    x = x - lp(x, 0.15)  # highpass-ish
    return x * env(n, 0.002, 0.06) * 0.35
def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR); x = rng.standard_normal(n)
    x = x - lp(x, 0.5)
    return x * env(n, 0.001, 0.06 if open_ else 0.015) * 0.18

def note_f(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55, 60], [55, 59, 62]]  # Am F C G
roots = [45, 41, 36, 43]

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.12):
            ph = 2 * np.pi * f * (1 + det / 100) * t
            x += (2 * ((ph / (2 * np.pi)) % 1) - 1) * 0.5  # saw
    x = lp(x / len(freqs), 0.035)
    e = np.minimum(t / 0.4, 1) * np.minimum((dur - t) / 0.4, 1)
    return x * e * 0.22

def bass(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return x * env(n, 0.005, dur * 0.6) * 0.32

def pluck(f, dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * 2 * f * t) * 0.3
    return lp(x, 0.12) * env(n, 0.003, 0.12) * 0.10

K, C = kick(), clap()
nbars = int(DUR / bar) + 1
arp_pat = [0, 2, 1, 2, 0, 2, 1, 2]
for b in range(nbars):
    t0 = b * bar; ci = b % 4
    add(music, pad([note_f(m) for m in chords[ci]], bar + 0.2), t0)
    intro = False
    for s in range(8):
        ts_ = t0 + s * beat / 2
        if not intro:
            add(music, hat(open_=(s == 7)), ts_)
        add(music, pluck(note_f(chords[ci][arp_pat[s] % len(chords[ci])] + 12)), ts_)
    if not intro:
        for k in (0, 2.5): add(music, K, t0 + k * beat)
        add(music, K, t0 + 3 * beat, 0.6)
        for c in (1, 3): add(music, C, t0 + c * beat)
        add(music, bass(note_f(roots[ci]), beat * 1.5), t0)
        add(music, bass(note_f(roots[ci]), beat * 1.0), t0 + beat * 2.5)
        add(music, bass(note_f(roots[ci] + 12), beat * 0.5), t0 + beat * 3.5)

# fade out at the end
fo = int(1.2 * SR); music[-fo:] *= np.linspace(1, 0, fo)
music /= np.max(np.abs(music)) + 1e-9
write("music3.wav", music * 0.8)


# ---------------- SFX (v3, driven by the graphics timeline)
import json
from timeline import word_time, SPEECH_END
T = json.load(open("anims3/times.json"))
sfx = np.zeros(N)
def whoosh(dur=0.45, up=True):
    n = int(dur * SR); x = rng.standard_normal(n); t = np.linspace(0, 1, n)
    cut = (0.02 + 0.35 * t) if up else (0.37 - 0.35 * t)
    y = np.empty(n); s_ = 0.0
    for i in range(n): s_ += cut[i] * (x[i] - s_); y[i] = s_
    return y * np.sin(np.pi * t) ** 2 * 0.9
def pop(f0=900):
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = f0 - 500 * t / 0.12
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03) * 0.5
def impact():
    n = int(1.0 * SR); t = np.arange(n) / SR
    f = 40 + 120 * np.exp(-t * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5)
    nz = lp(rng.standard_normal(n), 0.08) * np.exp(-t * 10)
    return (x + nz * 0.6) * 0.8
def riser(dur=0.6):
    n = int(dur * SR); t = np.linspace(0, 1, n); x = rng.standard_normal(n)
    y = np.empty(n); s_ = 0.0
    for i in range(n): s_ += (0.01 + 0.4 * t[i] ** 2) * (x[i] - s_); y[i] = s_
    tone = np.sin(2 * np.pi * np.cumsum(200 + 800 * t ** 2) / SR) * 0.15
    return (y + tone) * t ** 2 * 0.8
def ding():
    n = int(0.9 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 1980 * t)) * np.exp(-t * 5) * 0.22
def click():
    n = int(0.03 * SR); x = rng.standard_normal(n) * env(n, 0.0005, 0.004); return x * 0.6

add(sfx, impact(), 0.0, 0.9)
add(sfx, whoosh(0.35, False), 0.30, 0.5)                    # flash -> face
add(sfx, riser(0.55), T["c1"][0] - 0.55, 0.6)               # build into the Qwen card
add(sfx, impact(), T["c1"][0], 0.45)
add(sfx, whoosh(0.35, False), T["c1"][0] + T["c1"][1] - 0.15, 0.5)
for k in ("pa", "pb", "pc"):
    add(sfx, whoosh(0.4, True), T[k][0] - 0.12, 0.6)
add(sfx, whoosh(0.35, False), T["pa"][0] + T["pa"][1] - 0.2, 0.45)
add(sfx, whoosh(0.35, False), T["pc"][0] + T["pc"][1] - 0.2, 0.45)
for w, n_ in (("SIRI", 2), ("WRITING", 1), ("VISUAL", 1), ("PHOTO", 1)):
    add(sfx, pop(), word_time(w, n_)[0], 0.7)
add(sfx, impact(), word_time("ALIBABA'S", 2)[0], 0.35)
add(sfx, pop(1100), word_time("DECEMBER")[0], 0.7)
add(sfx, pop(700), word_time("DIFFERENT")[0], 0.7)
add(sfx, pop(1000), word_time("COUNTRY")[0], 0.6); add(sfx, pop(1200), word_time("COUNTRY")[0] + 0.08, 0.6)
for k in ("s1", "s2", "poll"): add(sfx, pop(), T[k][0] + 0.05, 0.7)
add(sfx, ding(), T["s4"][0] + 0.05, 0.9)
add(sfx, riser(0.45), SPEECH_END - 0.05, 0.5)                # loop tail swells back into the hook
write("sfx3.wav", sfx)
print("ok")
