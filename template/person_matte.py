"""Person matte for depth text ("text behind the speaker").
usage: python3 person_matte.py --win S,E [--win S,E ...] [-o matte.mkv]
Runs U^2-Net human segmentation (rembg's u2net_human_seg.onnx, downloaded from rembg's GitHub release by setup.sh)
on joined3.mkv frames inside the windows only, feathers + temporally smooths the mask, and writes a full-length
1080x1920 gray matte video. Outside the windows the matte is white (the person layer equals the base video there),
so compose_depth.py can always stack: base -> back text -> person cut-out -> front graphics."""
import argparse, os, subprocess, json
import numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("--win", action="append", required=True); ap.add_argument("-o", default="matte.mkv")
ap.add_argument("--model", default=os.path.expanduser(os.environ.get("REELS_TOOLS", "~/reels-tools")) + "/models/seg/u2net_human_seg.onnx")
ap.add_argument("--step", type=int, default=2, help="segment every Nth frame and hold the mask in between (2 = half the time)")
ap.add_argument("--tail", type=float, default=0.6, help="seconds the base video is held at the end (matches compose tpad)")
a = ap.parse_args()
W, H, FPS = 1080, 1920, 30
wins = [tuple(map(float, w.split(","))) for w in a.win]
nfr = sum(json.load(open("seg_frames.json"))) + int(round(a.tail * FPS))
sess = ort.InferenceSession(a.model, providers=["CPUExecutionProvider"])
inp = sess.get_inputs()[0].name
mean, std = np.array([0.485, 0.456, 0.406]), np.array([0.229, 0.224, 0.225])

def seg(rgb):
    im = Image.fromarray(rgb).resize((320, 320), Image.BILINEAR)
    x = (np.asarray(im, np.float32) / 255.0 - mean) / std
    out = sess.run(None, {inp: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    m = Image.fromarray((out * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    return np.asarray(m, np.float32)

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "joined3.mkv", "-vf", f"tpad=stop_mode=clone:stop_duration={a.tail}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "ffv1", a.o], stdin=subprocess.PIPE)
white = np.full((H, W), 255, np.uint8); prev = None; done = 0
for i in range(nfr):
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = i / FPS
    if any(s - 0.1 <= t <= e + 0.1 for s, e in wins):
        if prev is None or i % a.step == 0:
            m = seg(np.frombuffer(buf, np.uint8).reshape(H, W, 3)); done += 1
            prev = m if prev is None else 0.6 * m + 0.4 * prev        # temporal smoothing: no edge flicker
        enc.stdin.write(np.clip(prev, 0, 255).astype(np.uint8).tobytes())
    else:
        prev = None; enc.stdin.write(white.tobytes())
enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.wait()
print(f"matte: {i + 1} frames, segmented {done}")
