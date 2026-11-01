#!/usr/bin/env bash
# HyperFrames pipeline (Nov 2026, reels 3+4): every reel gets its OWN look.
# Project folder needs: raw.mov, reel.json, glossary.json, copies of template/*.py, and two per-reel scripts:
#   gen_hf.py  -> writes hf/index.html (one full-length transparent overlay keyed to word times) + hf/events.json
#   audio.py   -> writes music.wav + sfx.wav using sound.py (style: calm | tech | news)
# Examples: examples/reel3-apple-vs-agents (cards above the head), examples/reel4-interview-hack (split screen chat UI).
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")/.." && pwd)/tools"
export HYPERFRAMES_TELEMETRY=0 DO_NOT_TRACK=1 HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-$(command -v google-chrome || command -v chromium)}"

python3 "$TOOLS/transcribe_align.py" raw.mov -o edit --glossary glossary.json --text-only
sed -E 's/^\[[^]]*\] //' edit/raw.text.txt > edit/fixed.txt
echo ">> proofread edit/fixed.txt (brand names, numbers), then press enter"; read -r _
python3 "$TOOLS/transcribe_align.py" raw.mov -o edit --text edit/fixed.txt

python3 render_segments.py            # HDR tone map + 4K prescale + cuts + zooms (reel.json), writes seg_frames.json
mkdir -p hf/assets/fonts && cp /usr/share/fonts/truetype/google-fonts/Poppins-{Bold,Medium,Regular}.ttf /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf hf/assets/fonts/ 2>/dev/null; cp -n "$(dirname "$0")/../hyperframes/card-example/gsap.min.js" hf/assets/ 2>/dev/null || (cd hf && npm i gsap >/dev/null && cp node_modules/gsap/dist/gsap.min.js assets/)
python3 gen_hf.py && python3 audio.py
(cd hf && npx hyperframes lint && npx hyperframes render --format mov -o overlay.mov)
# captions: --split S,E only for split-screen reels (read hf/events.json); accent = the reel's colour
python3 captions_reel.py --accent "${ACCENT:-FFE500}" ${SPLIT:+--split $SPLIT} -o captions.ass
python3 compose.py reel.mp4 --overlay hf/overlay.mov --ass captions.ass --music music.wav --sfx sfx.wav \
  ${SPLIT:+--split $SPLIT --split-y ${SPLIT_Y:-860}} --bar "${ACCENT:-FFE500}"
