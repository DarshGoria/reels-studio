#!/usr/bin/env python3
"""Offline word-level transcription: Whisper (sherpa-onnx) for the words, PocketSphinx forced
alignment for the timings. No API keys, no network after the model download.

usage: transcribe_align.py INPUT -o OUT_DIR [--glossary glossary.json] [--model DIR] [--text-only]
       transcribe_align.py INPUT -o OUT_DIR --text fixed.txt      # align a proofread transcript

writes OUT/<stem>.text.txt (raw Whisper text per window), OUT/<stem>.words.json
({"words":[{"text","start","end"}]}), OUT/<stem>.phrases.txt
"""
import argparse, json, os, re, subprocess, sys, wave
import numpy as np

MODEL = os.environ.get("WHISPER_DIR", os.path.expanduser("~/reels-tools/models/sherpa-onnx-whisper-small.en"))
SR = 16000

def extract(inp, wav):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", inp, "-vn", "-ac", "1", "-ar", str(SR), wav], check=True)

def windows(x, max_len=25.0, min_sil=0.25):
    """split audio at quiet points into <= max_len windows of speech"""
    hop = SR // 100
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    db = 20 * np.log10(e)
    floor, speech = np.percentile(db, 10), np.percentile(db, 90)
    gate = max(floor + 8, speech - 30)
    voiced = db > gate
    segs, i, n = [], 0, len(voiced)
    while i < n:
        if voiced[i]:
            j = i
            gap = 0
            while j < n and gap < min_sil * 100:
                gap = 0 if voiced[j] else gap + 1
                j += 1
            segs.append([max(0, i - 15) / 100, min(n, j - gap + 15) / 100])
            i = j
        else:
            i += 1
    out = []
    for a, b in segs:  # merge into windows
        if out and b - out[-1][0] <= max_len and a - out[-1][1] < 1.0:
            out[-1][1] = b
        else:
            out.append([a, b])
    return out

NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}
TEEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
def int_words(n):
    if n < 10: return [NUM[str(n)]]
    if n < 20: return [TEEN[n - 10]]
    if n < 100: return [TENS[n // 10]] + ([NUM[str(n % 10)]] if n % 10 else [])
    if n < 1000: return [NUM[str(n // 100)], "hundred"] + (int_words(n % 100) if n % 100 else [])
    if 1900 < n < 2100: return int_words(n // 100) + int_words(n % 100)
    return [NUM[c] for c in str(n)]
def speak(tok):
    """display token -> list of spoken lowercase words for the aligner"""
    t = tok.lower().strip(".,!?;:\"()[]")
    t = t.replace("’", "'")
    if not t: return []
    m = re.fullmatch(r"(\d+)\.(\d+)", t)
    if m: return int_words(int(m.group(1))) + ["point"] + [NUM[c] for c in m.group(2)]
    if t.isdigit(): return int_words(int(t))
    if t.endswith("%") and t[:-1].isdigit(): return int_words(int(t[:-1])) + ["percent"]
    if re.fullmatch(r"[a-z]{2,4}", t) and t.upper() == tok.strip(".,!?") and t not in ("a", "i"):
        return list(t)  # acronyms said letter by letter: AI -> a i
    return [w for w in re.split(r"[-/]", t) if w]

# crude grapheme->phoneme for words missing from the CMU dictionary
G2P = [("tion", "SH AH N"), ("ch", "CH"), ("sh", "SH"), ("th", "TH"), ("ph", "F"), ("ck", "K"), ("ng", "NG"), ("qu", "K W"),
       ("ee", "IY"), ("oo", "UW"), ("ou", "AW"), ("ai", "EY"), ("ay", "EY"), ("ea", "IY"), ("oa", "OW"),
       ("a", "AE"), ("b", "B"), ("c", "K"), ("d", "D"), ("e", "EH"), ("f", "F"), ("g", "G"), ("h", "HH"), ("i", "IH"),
       ("j", "JH"), ("k", "K"), ("l", "L"), ("m", "M"), ("n", "N"), ("o", "AA"), ("p", "P"), ("q", "K"), ("r", "R"),
       ("s", "S"), ("t", "T"), ("u", "AH"), ("v", "V"), ("w", "W"), ("x", "K S"), ("y", "Y"), ("z", "Z")]
LETTER = {"a": "EY", "b": "B IY", "c": "S IY", "d": "D IY", "e": "IY", "f": "EH F", "g": "JH IY", "h": "EY CH", "i": "AY",
          "j": "JH EY", "k": "K EY", "l": "EH L", "m": "EH M", "n": "EH N", "o": "OW", "p": "P IY", "q": "K Y UW", "r": "AA R",
          "s": "EH S", "t": "T IY", "u": "Y UW", "v": "V IY", "w": "D AH B AH L Y UW", "x": "EH K S", "y": "W AY", "z": "Z IY"}
def g2p(w):
    ph, i = [], 0
    w = re.sub(r"[^a-z]", "", w)
    while i < len(w):
        for g, p in G2P:
            if w.startswith(g, i): ph.append(p); i += len(g); break
        else: i += 1
    return " ".join(ph) or "AH"

def align(decoder, audio_bytes, offset, spoken):
    known = []
    for w in spoken:
        if decoder.lookup_word(w) is None:
            ph = LETTER[w] if len(w) == 1 and w in LETTER else g2p(w)
            try: decoder.add_word(w, ph, True)
            except RuntimeError: pass
        known.append(w)
    decoder.set_align_text(" ".join(known))
    decoder.start_utt(); decoder.process_raw(audio_bytes, full_utt=True); decoder.end_utt()
    out = []
    for s in decoder.seg():
        if s.word in ("<sil>", "<s>", "</s>", "(NULL)", "[NOISE]"): continue
        out.append((s.word.split("(")[0], offset + s.start_frame / 100, offset + (s.end_frame + 1) / 100))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("-o", "--out", default="edit")
    ap.add_argument("--model", default=MODEL); ap.add_argument("--glossary")
    ap.add_argument("--text", help="proofread transcript to align instead of Whisper output (one line per window, or plain text)")
    ap.add_argument("--text-only", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(a.input))[0]
    wav = os.path.join(a.out, stem + ".16k.wav")
    extract(a.input, wav)
    w = wave.open(wav); raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    wins = windows(x)
    gl = json.load(open(a.glossary)) if a.glossary else {}

    texts = []
    if a.text:
        lines = [l.strip() for l in open(a.text) if l.strip()]
        texts = lines if len(lines) == len(wins) else None
        if texts is None:  # plain text: let the aligner place it across the whole take
            wins = [[wins[0][0], wins[-1][1]]]; texts = [" ".join(lines)]
    else:
        import sherpa_onnx
        p = lambda n: os.path.join(a.model, f"{os.path.basename(a.model).split('whisper-')[-1]}-{n}")
        rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=p("encoder.int8.onnx"), decoder=p("decoder.int8.onnx"),
                                                         tokens=p("tokens.txt"), language="en", task="transcribe", num_threads=os.cpu_count() or 2)
        for s0, s1 in wins:
            st = rec.create_stream(); st.accept_waveform(SR, x[int(s0 * SR):int(s1 * SR)]); rec.decode_stream(st)
            t = st.result.text.strip()
            for k, v in gl.items(): t = re.sub(rf"\b{re.escape(k)}\b", v, t, flags=re.I)
            texts.append(t)
    with open(os.path.join(a.out, stem + ".text.txt"), "w") as f:
        for (s0, s1), t in zip(wins, texts): f.write(f"[{s0:07.2f}-{s1:07.2f}] {t}\n")
    if a.text_only:
        print(open(os.path.join(a.out, stem + ".text.txt")).read()); return

    from pocketsphinx import Decoder
    dec = Decoder(samprate=SR)
    words = []
    for (s0, s1), t in zip(wins, texts):
        disp = t.split()
        spoken, owner = [], []
        for i, d in enumerate(disp):
            for sw in speak(d): spoken.append(sw); owner.append(i)
        if not spoken: continue
        seg = align(dec, raw[int(s0 * SR) * 2:int(s1 * SR) * 2], s0, spoken)
        # map aligned spoken tokens back to display words (aligner returns them in order)
        times = {}
        for k, (_, ws, we) in enumerate(seg[:len(owner)]):
            i = owner[k]; a0, a1 = times.get(i, (ws, we)); times[i] = (min(a0, ws), max(a1, we))
        last = s0
        for i, d in enumerate(disp):
            ws, we = times.get(i, (last, last + 0.2))
            words.append({"text": d, "start": round(ws, 3), "end": round(we, 3)}); last = we
    json.dump({"words": words}, open(os.path.join(a.out, stem + ".words.json"), "w"), indent=1)
    # phrases view
    lines, cur = [], []
    for wd in words:
        if cur and (wd["start"] - cur[-1]["end"] > 0.3 or cur[-1]["text"][-1:] in ".?!"):
            lines.append(cur); cur = []
        cur.append(wd)
    if cur: lines.append(cur)
    with open(os.path.join(a.out, stem + ".phrases.txt"), "w") as f:
        for l in lines: f.write(f"[{l[0]['start']:06.2f}-{l[-1]['end']:06.2f}] {' '.join(w['text'] for w in l)}\n")
    print(open(os.path.join(a.out, stem + ".phrases.txt")).read())

if __name__ == "__main__":
    main()
