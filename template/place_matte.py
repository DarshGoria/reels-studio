"""Scale + place a full-frame matte to the presenter box, fading the box's side edges so the cut never shows."""
import numpy as np, cv2, subprocess, sys, json
W, H = 1080, 1920; src, out = sys.argv[1], sys.argv[2]; s, X, Y = float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
w, h = round(W * s), round(H * s); fade = 70
m = np.ones((h, w), np.float32); ramp = np.linspace(0, 1, fade)[None, :]
m[:, :fade] *= ramp; m[:, -fade:] *= ramp[:, ::-1]
rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
wo = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "ffv1", out], stdin=subprocess.PIPE)
n = 0
while True:
    b = rd.stdout.read(W * H)
    if len(b) < W * H: break
    a = cv2.resize(np.frombuffer(b, np.uint8).reshape(H, W), (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) * m
    f = np.zeros((H, W), np.uint8); f[Y:Y + h, X:X + w] = a[: H - Y].astype(np.uint8)
    wo.stdin.write(f.tobytes()); n += 1
wo.stdin.close(); wo.wait(); print("placed", n)
