# reels-studio

Darsh's Instagram Reels editing pipeline for an AI news & hacks page. Raw phone clip in, two
finished reels out (full-screen floating cards + split screen), plus a cover and a post caption.

It fuses open-source editing tools and routes each job to the right one:

| Job | Tool |
|---|---|
| Speech to text (offline) | Whisper small.en via [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) |
| Word timings | [PocketSphinx](https://github.com/cmusphinx/pocketsphinx) forced alignment |
| Silence / filler / retake cuts | [master-skills `edit`](https://github.com/Jakeschincariol/master-skills) `deadspace.py` |
| Motion graphics with alpha | [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP → ProRes 4444) or the PIL engine in `template/` |
| Production rules, self-check | [video-use](https://github.com/browser-use/video-use) |
| Voice denoise | ffmpeg `arnndn` + [RNNoise models](https://github.com/richardpl/arnndn-models) |
| Everything else | ffmpeg (HDR→SDR tone map, zooms, compositing, captions, mastering) |

## Quick start

```bash
git clone https://github.com/DarshGoria/reels-studio ~/reels-studio
bash ~/reels-studio/setup.sh            # engines + Whisper model (~630 MB)
# then export the variables setup.sh prints

mkdir myreel && cd myreel
cp ~/reels-studio/template/* .
cp /path/to/IMG_1234.MOV raw.mov
# edit the PER-REEL parts (see the header comment in each script), then:
bash run.sh
```

## Layout

- `tools/transcribe_align.py` — Whisper words + aligned word timings → `words.json` / `phrases.txt`
- `template/` — the approved reference pipeline (Apple × Alibaba test reel, Nov 2026). Each script's
  first line says what is generic and what to rewrite per reel. `run.sh` runs the steps in order.
- `hyperframes/card-example/` — a transparent HyperFrames card (render with
  `npx hyperframes render --format mov`); use it as the starting point for HTML-built graphics.
- `SKILL.md` — the Claude skill that drives all of this (style rules, routing, QA checklist).

## House style (summary)

Poppins Bold, yellow `#FFE500` on dark navy glass. Hook flash (0–0.45 s) + seamless loop tail,
word-by-word karaoke captions, punch-in zooms on key words, 1.1× speed, graphics that land on the
word, a poll CTA, a bell on "follow", a progress bar, an original synthesized beat with ducking and
synced SFX, −14 LUFS master. Full details in `SKILL.md`.

## Filming checklist

4K 30 fps, **HDR Video off**, phone at eye level, light in front, clip-on mic, hands at chest
height, pause 1–2 s between lines. Send screenshots or screen recordings for real visuals.
