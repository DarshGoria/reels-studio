#!/usr/bin/env bash
# One-time setup per session/machine. Installs the open-source engines and models the
# reels-studio pipeline uses. Safe to re-run (skips what is already there).
set -euo pipefail
T="${REELS_TOOLS:-$HOME/reels-tools}"
mkdir -p "$T" && cd "$T"

clone() { [ -d "$2" ] || git clone -q --depth 1 "https://github.com/$1.git" "$2"; }
clone Jakeschincariol/master-skills master-skills     # edit tools: probe, deadspace, captions, stopmotion (MIT)
clone browser-use/video-use        video-use          # hard rules + self-eval method (MIT)
clone heygen-com/hyperframes       hyperframes        # HTML/GSAP motion graphics engine + skills (Apache-2.0)
clone remotion-dev/skills          remotion-skills    # only when a Remotion project already exists
clone richardpl/arnndn-models      arnndn-models      # RNNoise voice-denoise models for ffmpeg arnndn

pip install --break-system-packages -q sherpa-onnx pocketsphinx numpy pillow 2>/dev/null \
  || pip install -q sherpa-onnx pocketsphinx numpy pillow

mkdir -p models
if [ ! -d models/sherpa-onnx-whisper-small.en ]; then
  echo "downloading Whisper small.en (~630 MB, GitHub release)…"
  curl -sSL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.en.tar.bz2 | tar xj -C models
fi

npx -y hyperframes --version >/dev/null && echo "hyperframes ok"
python3 master-skills/skills/edit/tools/probe.py --doctor || true

cat <<EOF

Done. Export these in your shell:
  export REELS_TOOLS="$T"
  export WHISPER_DIR="$T/models/sherpa-onnx-whisper-small.en"
  export HYPERFRAMES_BROWSER_PATH="\$(command -v google-chrome || command -v chromium || command -v chromium-browser)"
  export HYPERFRAMES_TELEMETRY=0 DO_NOT_TRACK=1
EOF
