"""Edge-aware matte refinement: guided filter (He et al.) at full res, guide = video luma. Sharpens hair edges, kills halos."""
import numpy as np, cv2, subprocess, sys
W, H = 1080, 1920
src, mat, out = sys.argv[1], sys.argv[2], sys.argv[3]
rv = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
rm = subprocess.Popen(["ffmpeg", "-v", "error", "-i", mat, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
wo = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "ffv1", out], stdin=subprocess.PIPE)
def box(x, r): return cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1))
def gf(I, p, r=12, eps=1e-3):
    mI, mp = box(I, r), box(p, r); cov = box(I * p, r) - mI * mp; var = box(I * I, r) - mI * mI
    a = cov / (var + eps); b = mp - a * mI
    return box(a, r) * I + box(b, r)
n = 0
while True:
    v = rv.stdout.read(W * H); m = rm.stdout.read(W * H)
    if len(m) < W * H: break
    I = np.frombuffer(v, np.uint8).reshape(H, W).astype(np.float32) / 255 if len(v) == W * H else I
    p = np.frombuffer(m, np.uint8).reshape(H, W).astype(np.float32) / 255
    q = gf(I, p); q = np.clip((q - 0.12) / 0.76, 0, 1)
    wo.stdin.write((q * 255).astype(np.uint8).tobytes()); n += 1
wo.stdin.close(); wo.wait(); print("refined", n)
