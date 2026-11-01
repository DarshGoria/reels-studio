# reels-studio template — PER-REEL: EMPH = the words that get a punch-in zoom.
import subprocess, os
from timeline import keep, out_t, SPEED, word_time

EMPH = [word_time("CHINESE")[0], word_time("CHINA")[0], word_time("COUNTRY")[0],
        word_time("TRUST")[0], word_time("FOLLOW")[0], word_time("COMPLETELY")[0]]

TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv420p")
GRADE = ("curves=master='0/0 0.25/0.28 0.75/0.80 1/1',colorbalance=bs=0.02:bm=0.01,"
         "eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.35,vignette=PI/7")

# clear segments from a previous run: a stale seg3/pNN.mkv would be counted into seg_frames.json
# and shift every caption and graphic after it
import shutil
shutil.rmtree("seg3", ignore_errors=True)
os.makedirs("seg3", exist_ok=True)
lines = []
for i, (a, b) in enumerate(keep):
    o0 = out_t(a)
    d = b - a
    base = 1.0 if i % 2 == 0 else 1.06
    T = f"(t+{o0:.3f})"
    Z = f"{base}+0.012*t"
    for te in EMPH:
        if o0 - 1.5 < te < out_t(b) + 0.1:
            Z += f"+0.05*clip(({T}-{te:.3f})/0.12,0,1)*clip(1-({T}-{te:.3f}-0.9)/0.3,0,1)"
    vf = (f"{TONEMAP},setpts=(PTS-STARTPTS)/{SPEED},fps=30,"
          f"scale=w='2*trunc(1080*({Z})/2)':h=-2:eval=frame:flags=lanczos,"
          f"crop=1080:1920:(in_w-1080)/2:(in_h-1920)*0.35,setsar=1,{GRADE}")
    od = d / SPEED
    af = (f"atempo={SPEED},afade=t=in:d=0.015,afade=t=out:st={od-0.025:.3f}:d=0.025,aresample=48000,"
          "aformat=channel_layouts=stereo")
    tmp, final = f"seg3/p{i:02d}.tmp.mkv", f"seg3/p{i:02d}.mkv"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", "raw.mov",
                    "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "12",
                    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", tmp], check=True)
    os.replace(tmp, final)
    lines.append(f"file 'seg3/p{i:02d}.mkv'")
open("parts3.txt", "w").write("\n".join(lines) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parts3.txt", "-c", "copy", "joined3.mkv"], check=True)
print("done")
