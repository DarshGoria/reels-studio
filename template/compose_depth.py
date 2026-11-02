"""DEPTH variant of compose.py (text behind the speaker). Final composite for a reel whose graphics are ONE full-length transparent overlay (HyperFrames .mov)
+ two-pass audio master (fixed gain to -14 LUFS, true-peak limiter).
usage: compose.py OUT.mp4 --overlay hf/overlay.mov --ass captions.ass --music music.wav --sfx sfx.wav
                  [--split S,E ...]   video shrinks to 72% at y=860 over a blurred copy during each window
                  [--music-gain 0.16] [--bar FFE500]
"""
import argparse, json, os, re, subprocess
from timeline import TOTAL

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--overlay", required=True, help="FRONT overlay (on top of the person)")
ap.add_argument("--back", required=True, help="BACK overlay: depth text that sits behind the person")
ap.add_argument("--matte", default="matte.mkv", help="person matte from person_matte.py"); ap.add_argument("--ass", required=True)
ap.add_argument("--music", required=True); ap.add_argument("--sfx", required=True)
ap.add_argument("--split", action="append", default=[]); ap.add_argument("--music-gain", type=float, default=0.16)
ap.add_argument("--bar", default="FFE500")
ap.add_argument("--base-vf", default="", help="extra ffmpeg filters on the face video, e.g. colour correction")
ap.add_argument("--split-mode", default="slide", choices=["slide", "shrink"],
                help="slide: video stays full width and slides down behind the panel (no side bars). shrink: old 72%% PiP over a blurred copy")
ap.add_argument("--slide-y", type=int, default=340, help="slide mode: how far the video moves down (use face_zones.py: panel_h + 20 - face top)")
ap.add_argument("--split-y", type=int, default=860, help="top of the shrunk video in split mode; lower it when the head sits low in frame")
a = ap.parse_args()
RNN = os.path.expanduser(os.environ.get("REELS_TOOLS", "~/reels-tools")) + "/arnndn-models/std.rnnn"
S = [tuple(map(float, s.split(","))) for s in a.split]

f = []
if S:
    def ease(s, e): return f"min(1-pow(1-clip((t-{s:.3f})/0.25,0,1),3),1-pow(1-clip(({e:.3f}-t)/0.22,0,1),3))"
    E = ease(*S[0])
    for s_, e_ in S[1:]: E = f"max({E},{ease(s_, e_)})"   # ffmpeg max() takes exactly two args
    base = f"[0:v]{a.base_vf + ',' if a.base_vf else ''}tpad=stop_mode=clone:stop_duration=0.6"
    if a.split_mode == "slide":   # full-width video slides down behind the panel: no scaling, no side bars
        f += [f"{base}[m]", f"color=c=black:s=1080x1920:r=30:d={TOTAL + 1:.3f}[blk]",
              f"[blk][m]overlay=x=0:y='{a.slide_y}*{E}':eval=frame:shortest=1[v0]"]
    else:
        f += [f"{base},split=2[m][bgs]",
              "[bgs]scale=270:480,boxblur=12:2,scale=1080:1920,eq=brightness=-0.12:saturation=0.8[bg]",
              f"[m]scale=w='2*trunc(1080*(1-0.28*{E})/2)':h='2*trunc(1920*(1-0.28*{E})/2)':eval=frame:flags=lanczos[sm]",
              f"[bg][sm]overlay=x='(W-w)/2':y='{a.split_y}*{E}':eval=frame[v0]"]
else:
    f += [f"[0:v]{a.base_vf + ',' if a.base_vf else ''}tpad=stop_mode=clone:stop_duration=0.6[v0]"]
# depth stack: base -> back text -> person cut-out (base through the matte) -> front graphics -> captions
f[-1] = f[-1].replace("[v0]", "[v00]")
f.append("[v00]split=2[vb][vp]")
f.append("[4:v]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.5,format=yuva420p[bk]")
f.append("[vb][bk]overlay=0:0:eof_action=pass:format=auto[vbk]")
f.append("[5:v]setpts=PTS-STARTPTS,format=gray[mt]")
f.append("[vp]format=yuva420p[vpa]")
f.append("[vpa][mt]alphamerge[person]")
f.append("[vbk][person]overlay=0:0:format=auto[v0]")
# the overlay owns the hook (frame 0) and the loop tail, so captions go under it only where it is opaque;
# captions are burned after every card overlay (video-use hard rule) and before the full-screen hook/tail frames
f.append("[1:v]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.5,format=yuva420p[ov]")  # hold the last frame: the loop tail must cover the final output frame
f.append("[v0][ov]overlay=0:0:eof_action=pass:format=auto[o1]")
f.append(f"[o1]ass={a.ass}:fontsdir=/usr/share/fonts/truetype[cap]")
f.append(f"color=c=0x{a.bar}:s=1080x10:r=30:d={TOTAL:.3f}[bar]")
f.append(f"[cap][bar]overlay=x='-1080+1080*t/{TOTAL:.3f}':y=0:eval=frame[vout]")
f.append(f"[0:a]arnndn=m={RNN}:mix=0.9,highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,"
         "treble=g=1.5:f=9000,deesser,apad,asplit=2[voice][key]")
f.append(f"[2:a]volume={a.music_gain}[mus]")
f.append("[mus][key]sidechaincompress=threshold=0.035:ratio=6:attack=15:release=300[duck]")
f.append("[3:a]volume=0.5[fx]")
f.append("[voice][duck][fx]amix=inputs=3:duration=longest:normalize=0[aout]")
open("compose_filter.txt", "w").write(";\n".join(f))

pre = a.out.replace(".mp4", ".pre.mov")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "joined3.mkv", "-i", a.overlay, "-i", a.music, "-i", a.sfx, "-i", a.back, "-i", a.matte,
                "-filter_complex_script", "compose_filter.txt", "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-r", "30",
                "-c:a", "pcm_s24le", "-ar", "48000", pre], check=True)
def lufs(path, pre_filter="highpass=f=75,"):
    m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-map", "0:a:0", "-af", pre_filter + "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+)", m)[-1])
def master(G):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-map", "0:v", "-map", "0:a", "-c:v", "copy",
                    "-af", f"highpass=f=75,volume={G:.2f}dB,aresample=192000,alimiter=limit=0.79:attack=5:release=50:level=false,aresample=48000,alimiter=limit=0.79:attack=1:release=30:level=false",  # 2nd limiter catches resampler overshoot (seen: +5 dBTP spike)
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", a.out + ".tmp.mp4"], check=True)
    os.replace(a.out + ".tmp.mp4", a.out)
I0, _ = lufs(pre); G = -14 - I0
master(G)
I1, P1 = lufs(a.out, "")
if abs(-14 - I1) > 0.4 and G < 12:          # the limiter ate loud SFX peaks: one correction pass
    G += -14 - I1; master(G); I1, P1 = lufs(a.out, "")
os.remove(pre)
print(a.out, "I=%.1f gain=%+.1f dB -> %.1f LUFS, peak %.1f dBFS" % (I0, G, I1, P1))
