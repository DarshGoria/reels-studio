# reels-studio template — Generic (layout positions per element live in `pos`).
"""Final composite for both styles + two-pass audio master (fixed gain to -14 LUFS, true-peak limiter)."""
import json, os, subprocess, sys, re
from timeline import TOTAL

MODE = sys.argv[1]            # split | cards
OUT = sys.argv[2]
T = json.load(open("anims3/times.json")); S = json.load(open("splits.json"))
RNN = os.path.expanduser(os.environ.get("REELS_TOOLS", "~/reels-tools")) + "/arnndn-models/std.rnnn"

panels = ["pa", "pb", "pc"] if MODE == "split" else ["ca", "cb", "cc"]
order = ["s1", "c1", "s2"] + panels + ["poll", "s4"]
tkey = {"ca": "pa", "cb": "pb", "cc": "pc"}
pos = {"s1": (650, 300), "c1": (0, 0), "s2": (10, 700), "pa": (0, 0), "pb": (0, 0), "pc": (0, 0),
       "ca": (0, 830), "cb": (0, 830), "cc": (0, 830), "poll": (120, 790), "s4": (650, 560)}
inputs = ["joined3.mkv"] + [f"anims3/{k}.mov" for k in order] + ["anims3/hook.mov", "anims3/tail.mov", "music3.wav", "sfx3.wav"]

f = []
if MODE == "split":
    def ease(a, b): return f"min(1-pow(1-clip((t-{a:.3f})/0.25,0,1),3),1-pow(1-clip(({b:.3f}-t)/0.22,0,1),3))"
    E = "max(" + ",".join(ease(a, b) for a, b in S) + ")"
    f += ["[0:v]tpad=stop_mode=clone:stop_duration=0.6,split=2[m][bgs]",
          "[bgs]scale=270:480,boxblur=12:2,scale=1080:1920,eq=brightness=-0.12:saturation=0.8[bg]",
          f"[m]scale=w='2*trunc(1080*(1-0.28*{E})/2)':h='2*trunc(1920*(1-0.28*{E})/2)':eval=frame:flags=lanczos[sm]",
          f"[bg][sm]overlay=x='(W-w)/2':y='860*{E}':eval=frame[v0]"]
    ass = "overlay3.ass"
else:
    f += ["[0:v]tpad=stop_mode=clone:stop_duration=0.6[v0]"]
    ass = "overlay3b.ass"
cur = "v0"
for j, k in enumerate(order, 1):
    st = T[tkey.get(k, k)][0]
    f.append(f"[{j}:v]setpts=PTS-STARTPTS+{st:.3f}/TB[a{j}]")
    f.append(f"[{cur}][a{j}]overlay={pos[k][0]}:{pos[k][1]}:eof_action=pass[o{j}]"); cur = f"o{j}"
f.append(f"[{cur}]ass={ass}:fontsdir=/usr/share/fonts/truetype[cap]")
f.append(f"color=c=0xFFE500:s=1080x10:r=30:d={TOTAL:.3f}[bar]")
f.append(f"[cap][bar]overlay=x='-1080+1080*t/{TOTAL:.3f}':y=0:eval=frame[pb_]")
nh = len(order) + 1; nt = nh + 1; nm = nt + 1; ns = nt + 2
f.append(f"[{nh}:v]setpts=PTS-STARTPTS[hk]")
f.append("[pb_][hk]overlay=0:0:eof_action=pass[h1]")
f.append(f"[{nt}:v]tpad=stop_mode=clone:stop_duration=0.5,setpts=PTS-STARTPTS+{T['tail'][0]:.3f}/TB[tl]")
f.append("[h1][tl]overlay=0:0:eof_action=pass[vout]")
# voice: RNNoise denoise, clean-up EQ, de-ess. No compressor / no AGC.
f.append(f"[0:a]arnndn=m={RNN}:mix=0.9,highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,"
         "treble=g=1.5:f=9000,deesser,apad,asplit=2[voice][key]")
f.append(f"[{nm}:a]volume=0.16[mus]")
f.append("[mus][key]sidechaincompress=threshold=0.035:ratio=6:attack=15:release=300[duck]")
f.append(f"[{ns}:a]volume=0.5[fx]")
f.append("[voice][duck][fx]amix=inputs=3:duration=longest:normalize=0[aout]")
open(f"final_{MODE}.txt", "w").write(";\n".join(f))

cmd = ["ffmpeg", "-v", "error", "-y"]
for i in inputs: cmd += ["-i", i]
tmp = OUT.replace(".mp4", ".pre.mp4")
cmd += ["-filter_complex_script", f"final_{MODE}.txt", "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-r", "30",
        "-c:a", "pcm_s24le", "-ar", "48000", tmp.replace(".mp4", ".mov")]
subprocess.run(cmd, check=True)
pre = tmp.replace(".mp4", ".mov")

# two-pass master: measure, one fixed gain to -14 LUFS, look-ahead true-peak limiter at -1.5 dBTP
m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", pre, "-map", "0:a:0", "-af", "highpass=f=75,ebur128=peak=true",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); G = -14 - I
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-map", "0:v", "-map", "0:a", "-c:v", "copy",
                "-af", f"highpass=f=75,volume={G:.2f}dB,aresample=192000,alimiter=limit=0.841:attack=5:release=50:level=false,aresample=48000",
                "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", OUT + ".tmp.mp4"], check=True)
import os; os.replace(OUT + ".tmp.mp4", OUT); os.remove(pre)
m2 = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", OUT, "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
print(MODE, "pre I=%.1f gain=%+.1f dB ->" % (I, G), re.findall(r"I:\s+(-?[\d.]+) LUFS", m2)[-1], "LUFS, peak", re.findall(r"Peak:\s+(-?[\d.]+)", m2)[-1], "dBFS")
