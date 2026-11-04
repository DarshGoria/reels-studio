# reels-studio template — generic. Per-reel settings live in reel.json:
#   "emph":   [["WORD", nth], ...]   words that get a +0.05 punch-in zoom (nth = which occurrence)
#   "zoom":   [base_even, base_odd]  alternating base zoom per segment (1.0/1.06 default)
#   "crop_k": 0.35                   vertical crop anchor: 0 = keep top, 1 = keep bottom (raise it when the head sits low)
# Source handling is automatic: HDR (HLG/PQ) is tone-mapped, SDR is not; 4K is pre-scaled to 1296x2304
# so every zoom up to 1.2 is a downscale (sharp).
import subprocess, os, json, shutil
from timeline import keep, out_t, SPEED, word_time

CFG = json.load(open("reel.json")) if os.path.exists("reel.json") else {}
EMPH = [word_time(w, n)[0] for w, n in CFG.get("emph", [])]
ZB = CFG.get("zoom", [1.0, 1.06])
CROP_K = CFG.get("crop_k", 0.35)

probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", "raw.mov"],
                                  capture_output=True, text=True).stdout)["streams"][0]
W, H = probe["width"], probe["height"]
rot = abs(int(next((s.get("rotation", 0) for s in probe.get("side_data_list", []) if "rotation" in s), 0)))
if rot in (90, 270): W, H = H, W
HDR = probe.get("color_transfer") in ("arib-std-b67", "smpte2084")
BIG = W > 1300
PRE_W, PRE_H = (1296, 2304) if BIG else (W, H)
size = f"w={PRE_W}:h={PRE_H}:filter=lanczos:" if BIG else ""
if HDR:
    tin = "arib-std-b67" if probe["color_transfer"] == "arib-std-b67" else "smpte2084"
    SRC = (f"zscale={size}tin={tin}:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv420p")
else:
    SRC = f"scale={PRE_W}:{PRE_H}:flags=lanczos,format=yuv420p" if BIG else "format=yuv420p"
GRADE = ("curves=master='0/0 0.25/0.28 0.75/0.80 1/1',colorbalance=bs=0.02:bm=0.01,"
         "eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.5:3:3:0.0,vignette=PI/7")
print(f"source {W}x{H} hdr={HDR} prescale={PRE_W}x{PRE_H} zoom={ZB} crop_k={CROP_K}")

# clear segments from a previous run: a stale seg3/pNN.mkv would be counted into seg_frames.json
shutil.rmtree("seg3", ignore_errors=True)
os.makedirs("seg3", exist_ok=True)
lines = []
for i, (a, b) in enumerate(keep):
    o0 = out_t(a)
    d = b - a
    base = ZB[i % 2]
    T = f"(t+{o0:.3f})"
    # QUALITY: a 1080p source is never enlarged (no drift zoom, no punch-ins) — only 4K sources get zoom moves
    Z = f"{base}+0.012*t" if BIG else "1.0"
    for te in (EMPH if BIG else []):
        if o0 - 1.5 < te < out_t(b) + 0.1:
            Z += f"+0.05*clip(({T}-{te:.3f})/0.12,0,1)*clip(1-({T}-{te:.3f}-0.9)/0.3,0,1)"
    if not BIG: base = 1.0
    geo = (f"scale=w='2*trunc(1080*({Z})/2)':h=-2:eval=frame:flags=lanczos,crop=1080:1920:(in_w-1080)/2:(in_h-1920)*{CROP_K},"
           if BIG else "")
    vf = f"{SRC},setpts=(PTS-STARTPTS)/{SPEED},fps=30,{geo}setsar=1,{GRADE}"
    od = d / SPEED
    af = (f"atempo={SPEED},afade=t=in:d=0.015,afade=t=out:st={od-0.025:.3f}:d=0.025,aresample=48000,"
          "aformat=channel_layouts=stereo")
    tmp, final = f"seg3/p{i:02d}.tmp.mkv", f"seg3/p{i:02d}.mkv"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", "raw.mov",
                    "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "6",
                    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", tmp], check=True)
    os.replace(tmp, final)
    lines.append(f"file 'seg3/p{i:02d}.mkv'")
open("parts3.txt", "w").write("\n".join(lines) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parts3.txt", "-c", "copy", "joined3.mkv"], check=True)
# real frame counts -> seg_frames.json (timeline.py rebuilds the output clock from these)
fr = []
for l in lines:
    f = l.split("'")[1]
    fr.append(int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                                  "stream=nb_read_frames", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip().strip(",")))
json.dump(fr, open("seg_frames.json", "w"))
print("done", len(fr), "segments,", sum(fr) / 30, "s")
