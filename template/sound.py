"""reels-studio sound kit — original synthesized music beds + SFX (numpy only, no samples, no copyright).
Usage in a per-reel audio.py:
    from sound import *
    m = music(dur, style="calm")          # or "tech", "news"
    fx = Track(dur); fx.add(impact(), 0.0, 0.9); fx.add(pop(), 3.2); ...
    write("music.wav", m); write("sfx.wav", fx.buf)
"""
import numpy as np, wave

SR = 48000
rng = np.random.default_rng(3)

def write(name, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1)
    with wave.open(name, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)

def lp(x, a):
    """one-pole low-pass; a may be a scalar or a per-sample array"""
    y = np.empty_like(x); s = 0.0
    av = np.broadcast_to(np.asarray(a, dtype=float), x.shape)
    for i in range(len(x)): s += av[i] * (x[i] - s); y[i] = s
    return y

class Track:
    def __init__(self, dur): self.buf = np.zeros(int(SR * dur))
    def add(self, x, t0, g=1.0):
        i = int(t0 * SR)
        if i < 0: x = x[-i:]; i = 0
        if i >= len(self.buf): return
        x = x[: len(self.buf) - i]; self.buf[i:i + len(x)] += x * g

def nf(m): return 440 * 2 ** ((m - 69) / 12)

# ---------------- drums / instruments
def kick(punch=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 48 + 110 * punch * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 0.9
def clap():
    n = int(0.25 * SR); x = rng.standard_normal(n); x = x - lp(x, 0.15)
    return x * env(n, 0.002, 0.06) * 0.35
def snap():
    n = int(0.12 * SR); x = rng.standard_normal(n); x = x - lp(x, 0.4)
    return x * env(n, 0.001, 0.02) * 0.3
def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR); x = rng.standard_normal(n); x = x - lp(x, 0.5)
    return x * env(n, 0.001, 0.06 if open_ else 0.015) * 0.16
def pad(freqs, dur, bright=0.035, g=0.22):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.12):
            ph = f * (1 + det / 100) * t
            x += (2 * (ph % 1) - 1) * 0.5
    x = lp(x / len(freqs), bright)
    return x * np.minimum(t / 0.4, 1) * np.minimum((dur - t) / 0.4, 1) * g
def epiano(f, dur=0.9, g=0.12):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 6))
    return x * env(n, 0.004, 0.45) * g
def pluck(f, dur=0.35, g=0.10, bright=0.12):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * 2 * f * t) * 0.3
    return lp(x, bright) * env(n, 0.003, 0.12) * g
def bass(f, dur, g=0.32):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return x * env(n, 0.005, dur * 0.6) * g

STYLES = {
    # calm, minimal: e-piano chords, soft kick/snap, no busy hats — talk/opinion reels
    "calm": dict(bpm=92, chords=[[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]], roots=[48, 45, 41, 43]),
    # tech: 122 bpm, minor arps, four-on-the-floor, 16th hats — hacks/tutorials
    "tech": dict(bpm=122, chords=[[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]], roots=[45, 41, 43, 40]),
    # tense: 100 bpm minor (Dm-Bb-Gm-A), pulsing 8th bass, ticking hats, no claps — market/crash/warning stories
    "tense": dict(bpm=100, chords=[[62, 65, 69], [58, 62, 65], [55, 58, 62], [57, 61, 64]], roots=[38, 34, 31, 33]),
    # news: 104 bpm, Am-F-C-G pads + plucks (the original test-reel bed)
    "news": dict(bpm=104, chords=[[57, 60, 64], [53, 57, 60], [48, 52, 55, 60], [55, 59, 62]], roots=[45, 41, 36, 43]),
}

def music(dur, style="news", seed=3):
    global rng
    rng = np.random.default_rng(seed)
    S = STYLES[style]; beat = 60 / S["bpm"]; bar = beat * 4
    tr = Track(dur + 1)
    K, C, SN = kick(), clap(), snap()
    for b in range(int(dur / bar) + 1):
        t0 = b * bar; ci = b % 4; ch = S["chords"][ci]
        if style == "calm":
            for k in (0, 2.5): tr.add(np.sum([epiano(nf(m)) for m in ch], 0), t0 + k * beat, 0.8)
            tr.add(pad([nf(m) for m in ch], bar + 0.2, bright=0.02, g=0.12), t0)
            tr.add(kick(0.7), t0, 0.7); tr.add(kick(0.7), t0 + 2.5 * beat, 0.5)
            for c in (1, 3): tr.add(SN, t0 + c * beat, 0.9)
            tr.add(bass(nf(S["roots"][ci]), beat * 2, 0.26), t0)
            for s in range(8): tr.add(hat(), t0 + s * beat / 2 + beat / 4, 0.5)
        elif style == "tech":
            tr.add(pad([nf(m) for m in ch], bar + 0.2, bright=0.05, g=0.14), t0)
            for s in range(16):
                ts_ = t0 + s * beat / 4
                tr.add(pluck(nf(ch[s % len(ch)] + 12 * (s // 8 % 2)), 0.18, 0.09, 0.2), ts_)
                tr.add(hat(open_=(s % 4 == 2)), ts_, 0.8 if s % 2 else 0.5)
            for k in range(4): tr.add(K, t0 + k * beat)
            for c in (1, 3): tr.add(C, t0 + c * beat)
            for k in range(8): tr.add(bass(nf(S["roots"][ci]), beat * 0.45, 0.24), t0 + k * beat / 2 + beat / 4)
        elif style == "tense":
            tr.add(pad([nf(m) for m in ch], bar + 0.2, bright=0.02, g=0.18), t0)
            for k in range(8): tr.add(bass(nf(S["roots"][ci]), beat * 0.42, 0.30), t0 + k * beat / 2)
            for s in range(16): tr.add(hat(), t0 + s * beat / 4, 0.7 if s % 4 == 0 else 0.35)
            for k in (0, 2): tr.add(K, t0 + k * beat)
            tr.add(K, t0 + 3.5 * beat, 0.5)
            for s in (3, 7): tr.add(pluck(nf(ch[0] + 12), 0.5, 0.08, 0.06), t0 + s * beat / 2)
        else:
            tr.add(pad([nf(m) for m in ch], bar + 0.2), t0)
            for s in range(8):
                tr.add(hat(open_=(s == 7)), t0 + s * beat / 2)
                tr.add(pluck(nf(ch[[0, 2, 1, 2][s % 4] % len(ch)] + 12)), t0 + s * beat / 2)
            for k in (0, 2.5): tr.add(K, t0 + k * beat)
            tr.add(K, t0 + 3 * beat, 0.6)
            for c in (1, 3): tr.add(C, t0 + c * beat)
            tr.add(bass(nf(S["roots"][ci]), beat * 1.5), t0); tr.add(bass(nf(S["roots"][ci]), beat), t0 + beat * 2.5)
    x = tr.buf[: int(SR * dur)]
    fo = int(1.0 * SR); x[-fo:] *= np.linspace(1, 0, fo)
    return x / (np.max(np.abs(x)) + 1e-9) * 0.8

# ---------------- SFX
def whoosh(dur=0.45, up=True):
    n = int(dur * SR); x = rng.standard_normal(n); t = np.linspace(0, 1, n)
    y = lp(x, (0.02 + 0.35 * t) if up else (0.37 - 0.35 * t))
    return y * np.sin(np.pi * t) ** 2 * 0.9
def pop(f0=900):
    n = int(0.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 - 500 * t / 0.12) / SR) * env(n, 0.001, 0.03) * 0.5
def impact():
    n = int(1.0 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(40 + 120 * np.exp(-t * 18)) / SR) * np.exp(-t * 3.5)
    return (x + lp(rng.standard_normal(n), 0.08) * np.exp(-t * 10) * 0.6) * 0.8
def riser(dur=0.6):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    y = lp(rng.standard_normal(n), 0.01 + 0.4 * t ** 2)
    return (y + np.sin(2 * np.pi * np.cumsum(200 + 800 * t ** 2) / SR) * 0.15) * t ** 2 * 0.8
def ding(f=1320):
    n = int(0.9 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 5) * 0.22
def chime():
    out = np.zeros(int(1.2 * SR))
    for i, f in enumerate((1047, 1319, 1568)):
        d = ding(f) * 0.8; o = int(i * 0.07 * SR); out[o:o + len(d)] += d[: len(out) - o]
    return out
def click():
    n = int(0.025 * SR); x = rng.standard_normal(n); x = x - lp(x, 0.3)
    return x * env(n, 0.0005, 0.004) * 0.7
def buzz(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 116 * t)) * 0.5
    return lp(x, 0.2) * np.minimum(t / 0.01, 1) * np.minimum((dur - t) / 0.05, 1) * 0.35
def stamp():
    n = int(0.3 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * np.cumsum(90 + 200 * np.exp(-t * 40)) / SR) * np.exp(-t * 18)
            + lp(rng.standard_normal(n), 0.3) * np.exp(-t * 30) * 0.5) * 0.8
def glitch(dur=0.4):
    n = int(dur * SR); x = np.zeros(n)
    for k in range(0, n, int(0.03 * SR)):
        seg = min(int(0.03 * SR), n - k)
        if rng.random() > 0.35: x[k:k + seg] = rng.standard_normal(seg) * rng.uniform(0.2, 0.6)
    return lp(x, 0.4) * 0.6
def swish_up(dur=0.25):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    return np.sin(2 * np.pi * np.cumsum(400 + 1600 * t ** 2) / SR) * np.sin(np.pi * t) * 0.18

def alert(n=3, f=(988, 1319)):
    """stock-alert style two-tone beeps"""
    out = np.zeros(int(SR * (0.16 * n * 2 + 0.1)))
    for k in range(n * 2):
        m = int(0.12 * SR); t = np.arange(m) / SR
        b = np.sin(2 * np.pi * f[k % 2] * t) * np.minimum(t / 0.005, 1) * np.minimum((0.12 - t) / 0.01, 1) * 0.25
        o = int(k * 0.16 * SR); out[o:o + m] += b
    return out
def ticks(dur, start_rate=8, end_rate=30):
    """accelerating counter ticks over dur seconds"""
    out = np.zeros(int(SR * dur) + SR // 10); t = 0.0
    while t < dur:
        c = click() * 0.6; o = int(t * SR); out[o:o + len(c)] += c[: len(out) - o]
        r = start_rate + (end_rate - start_rate) * (t / dur); t += 1.0 / r
    return out
def snip():
    a = click(); n = int(0.08 * SR); b = lp(rng.standard_normal(n), 0.5) * env(n, 0.001, 0.02) * 0.5
    out = np.zeros(int(0.2 * SR)); out[:len(a)] += a; out[int(0.07 * SR):int(0.07 * SR) + n] += b; return out
def burst():
    """balloon/bubble pop"""
    n = int(0.35 * SR); t = np.arange(n) / SR
    return (rng.standard_normal(n) * np.exp(-t * 25) * 0.8 + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30) * 0.5)
