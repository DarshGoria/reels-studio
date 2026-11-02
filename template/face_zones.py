"""Face-aware layout: where is the face in the cut, and where is it safe to put graphics?
usage: python3 face_zones.py            (reads joined3.mkv, writes faces.json)
Prints the face box range and the free zones above the head / below the chin, so gen_hf.py can
place stickers and cards where they never cover the face. Uses OpenCV's frontal-face cascade
(the xml ships inside the opencv-python 4.x wheel: setup.sh extracts it to $REELS_TOOLS/models/opencv/)."""
import cv2, json, os, subprocess, numpy as np
CASC = os.path.expanduser(os.environ.get("REELS_TOOLS", "~/reels-tools")) + "/models/opencv/haarcascade_frontalface_default.xml"
casc = cv2.CascadeClassifier(CASC)
assert not casc.empty(), f"face cascade missing: {CASC}"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "joined3.mkv"],
                           capture_output=True, text=True).stdout)
boxes = []
for t in np.arange(0.2, dur - 0.1, 0.5):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", "joined3.mkv", "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True).stdout
    g = np.frombuffer(raw, np.uint8).reshape(1920, 1080)
    f = casc.detectMultiScale(g, 1.1, 5, minSize=(200, 200))
    if len(f):
        x, y, w, h = max(f, key=lambda b: b[2] * b[3]); boxes.append([round(float(t), 2), int(x), int(y), int(w), int(h)])
a = np.array([b[1:] for b in boxes])
out = {"boxes": boxes,
       "top": int(a[:, 1].min()), "chin": int((a[:, 1] + a[:, 3]).max() + 0.12 * a[:, 3].max()),   # cascade box stops above the chin
       "left": int(a[:, 0].min()), "right": int((a[:, 0] + a[:, 2]).max())}
out["free_above"] = [200, max(200, out["top"] - 30)]            # below the IG top bar, above the hair
out["free_below"] = [out["chin"] + 30, 1470]                     # below the chin, above the caption block
json.dump(out, open("faces.json", "w"), indent=1)
print(f"{len(boxes)} frames | face y {out['top']}-{out['chin']} x {out['left']}-{out['right']} | "
      f"free above {out['free_above']} | free below {out['free_below']}")
