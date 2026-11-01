#!/usr/bin/env bash
# Reference pipeline (the approved Apple x Alibaba test reel, Nov 2026).
# Run inside a project folder that contains raw.mov and copies of the template/*.py files.
# Story-specific parts to rewrite per reel are marked "PER-REEL" in the scripts:
#   timeline.py      -> display-word fixes (disp()), emphasis words live in render_segments.py
#   render_segments.py -> EMPH list (punch-in words)
#   graphics3.py     -> hook headline, panels A/B/C content + which words trigger them, poll text
#   graphics3b.py    -> the same content as floating cards
#   captions3.py     -> title texts
#   audio_gen3.py    -> SFX cue words
set -euo pipefail
TOOLS="$(cd "$(dirname "$0")/.." && pwd)/tools"

# 1. transcribe (Whisper) -> proofread -> align (word timings)
python3 "$TOOLS/transcribe_align.py" raw.mov -o edit --glossary glossary.json --text-only
sed -E 's/^\[[^]]*\] //' edit/raw.text.txt > edit/fixed.txt
echo ">> proofread edit/fixed.txt (brand names, numbers), then press enter"; read -r _
python3 "$TOOLS/transcribe_align.py" raw.mov -o edit --text edit/fixed.txt

# 2. cut + tone-map + zoom + grade, one file per segment, then lossless concat
rm -f seg_frames.json
python3 render_segments.py
for f in $(sed -E "s/^file .(.*).$/\1/" parts3.txt); do ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 "$f"; done \
  | python3 -c "import sys,json,re; json.dump([int(x) for x in re.findall(r'\d+',sys.stdin.read())], open('seg_frames.json','w'))"

# 3. graphics (PIL engine; HyperFrames compositions can replace any .mov in anims3/)
python3 graphics3.py && python3 graphics3b.py

# 4. captions for both layouts
python3 captions3.py && python3 captions3.py --nosplit
python3 - <<'EOF'
s=open('overlay3b.ass').read().replace(',1,9,4,2,40,40,400,1',',1,9,4,2,40,40,330,1'); open('overlay3b.ass','w').write(s)
EOF

# 5. music + SFX
python3 audio_gen3.py

# 6. composite + two-pass master, both layouts
python3 make_final.py split reel_split.mp4 & python3 make_final.py cards reel_fullscreen.mp4 & wait
echo "done: reel_split.mp4 reel_fullscreen.mp4  (then: python3 cover.py <sec> 'L1' 'L2' 'L3' --tag TAG [--place top] [--accent HEX])"
