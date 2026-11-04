---
name: reels-studio
description: Edit Darsh's raw talking-head clips into finished Instagram Reels in his house style (AI news/hacks page), fusing HyperFrames, master-skills edit, video-use rules and offline Whisper.
---

# Reels Studio

One workflow that fuses the best open-source editing tools and routes each job to the right one. Input: a raw phone clip (+ the script if he has one). Output: two finished reels (full-screen floating cards + split screen), a cover JPG and a post caption.

## 0b. Growth rules (from analytics/2026-11-02.md — re-check after every batch)

These override the house style where they conflict. Log every batch in `analytics/` and update these rules from the numbers.
1. **Face in frame 1, no full-screen graphic opener.** The hook flash is now a text/sticker OVER the face (the face is visible from frame 0), never a full-screen designed slide; it reads as an ad and gets swiped. The loop tail stays, but loops back to the face shot.
2. **Payoff promise in the first 1.5 s, spoken AND on screen.** Spoken line = the claim; on-screen text = the curiosity gap ("free", "nobody tells you", a number, "you" + their problem). No warm-up words ("So", "Hey guys", a name card).
3. **Length 12-20 s.** One idea per reel. Cut every line that is context, not payoff. No "follow for daily AI" outro: end on the punchline so the loop starts cleanly.
4. **Engagement asks go early.** Share bait at the payoff ("send this to the friend who still writes long prompts"), the comment question inside the first 5 s or as on-screen text from 2 s, comment-keyword offers ("comment PROMPT and I'll DM it") for hacks.
5. **Audience = India, men 18-34.** Prefer AI tools, free hacks, money/career/jobs angles, Indian apps and prices in rupees; global news only with a "what it means for you" line. Test Hinglish.
6. **Never cover the face (Darsh flagged this, 2026-11-02).** Run `template/face_zones.py` on every cut before designing: it detects the face across the reel and writes `faces.json` (face y range, free zone above the head, free zone below the chin). Put the frame-0 hook sticker in a free zone; if the face fills the frame (close framing), cards go in a split-screen top panel, never over the chest. Split screen = `compose.py --split S,E --split-mode slide --slide-y N` (default): the full-width video slides down behind the panel, N = panel height + 20 - face top, so the face sits fully between the panel and the IG bottom bar (~1650). Never the old shrink mode: Darsh rejected the blurred side bars as unprofessional. Check stills at every card moment.
7. **Fix the light before grading.** Strong coloured room light (e.g. purple, wall green ~0) makes skin magenta: measure the wall colour, then pass a correction via `compose.py --base-vf` (reel-india-ai-shopping used colorbalance -R/+G/-B, hue s=0.72, slight lift). Remind Darsh to film under white light.
8. **Split screen only after 3 s.** The first 3 s are full-screen face (largest face = best hold); panels come in on the first concrete noun.
9. **Post-ready checklist:** cover set manually on both platforms (face + 3-4 words), YouTube title = the hook, post IG + YT together, reply to every comment in the first hour, post the hack reels on IG too.

## 0. Setup (once per session, ~3 min)

```bash
git clone --depth 1 https://github.com/DarshGoria/reels-studio ~/reels-studio
bash ~/reels-studio/setup.sh        # clones master-skills, video-use, hyperframes, remotion skills, arnndn models; installs sherpa-onnx + pocketsphinx; downloads Whisper small.en from GitHub releases
export REELS_TOOLS=~/reels-tools WHISPER_DIR=~/reels-tools/models/sherpa-onnx-whisper-small.en
export HYPERFRAMES_BROWSER_PATH=$(command -v google-chrome || command -v chromium) HYPERFRAMES_TELEMETRY=0 DO_NOT_TRACK=1
```
Then make a project folder, copy `~/reels-studio/template/*` into it, put the clip in as `raw.mov`. Each template script's first line says which parts are PER-REEL (headline, panel content, trigger words, emphasis words, titles, SFX cues); rewrite those for the new story, keep the rest. `template/run.sh` runs the steps in order. HuggingFace and most model CDNs are blocked in the sandbox; GitHub release assets work.

## 1. Probe + colour (always first)

`ffprobe` the clip. iPhone footage is usually HDR (HEVC Main10, `arib-std-b67`, bt2020). Never convert it without tone mapping (that caused the washed-out v1-v3). `render_segments.py` tone-maps every segment:
```
zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv420p
```
If the source is SDR, drop the tone map. Grade: `curves=master='0/0 0.25/0.28 0.75/0.80 1/1',colorbalance=bs=0.02:bm=0.01,eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.35,vignette=PI/7`. Tag outputs bt709.

## 2. Transcribe (offline, word-level)

`tools/transcribe_align.py raw.mov -o edit --glossary glossary.json --text-only`, then proofread `edit/fixed.txt` by hand (brand names, model names, version numbers: Whisper wrote "2.7.3" for 27.3 and "agent agents" for Intelligence), then `--text edit/fixed.txt` to align. Output `edit/raw.words.json` = `{"words":[{"text","start","end"}]}` (same shape master-skills captions.py and HyperFrames transcript.json accept) + `phrases.txt` to read the take. Grow `glossary.json` with every recurring fix. Never align the script instead of the transcript: Darsh ad-libs, and script alignment clipped a word in v3.

## 3. Cut (word-boundary jump cuts, sped up)

- `timeline.py`: keep ranges from word times (pad 0.06 s, merge gaps < 0.26 s), 1.1x speed, output timeline rebuilt from the real frame count of each rendered segment (`seg_frames.json`). For fillers/retakes run `$REELS_TOOLS/master-skills/skills/edit/tools/deadspace.py --transcript edit/raw.words.json --dry-run` and drop those words before cutting.
- `render_segments.py`: one file per keep range (video-use hard rule; never one giant trim graph, it OOMs), tone map -> speed -> zoom -> grade, 30 ms audio fades, then lossless concat to `joined3.mkv`.
- Zoom: alternate base 1.00/1.06, +0.012/s drift, +0.05 punch-ins on EMPH words; keep total <= ~1.11 on 1080p (4K source allows more).
- Shorts pacing: hook payoff in the first 1-2 s, aim for no static shot over ~1.5 s.

## 4. Graphics: route to an engine

| Need | Engine |
|---|---|
| Rich cards, panels, kinetic type, hook/end cards | HyperFrames: HTML/CSS + GSAP, `npx hyperframes render --format mov` gives ProRes 4444 with alpha (see `hyperframes/card-example`). Install gsap locally and copy fonts in (CDNs may be blocked). Use its lint/check/snapshot loop. ~30 s per 3 s overlay on CPU. A HyperFrames .mov drops straight into `anims3/` in place of a PIL one. |
| The approved look, fast | `graphics3.py` (split panels, hook, loop tail, poll, stickers) + `graphics3b.py` (floating cards), PIL -> png-codec .mov with alpha |
| Darsh already has a Remotion project | Remotion agent skills |
| Stop motion | master-skills stopmotion.py |
Rules: the visual lands on the frame the word is said and shows the literal noun. Real logos and photos only if Darsh supplies them (no recreated brand logos, no downloaded photos of people). Overlays use `setpts=PTS-STARTPTS+T/TB` and `eof_action=pass`; captions are burned after every overlay.

## 4b. Every reel gets its own look (HyperFrames pipeline, `template/run_hf.sh`)

Darsh wants reels that don't feel like one template repeated. Keep the channel constants (Poppins karaoke captions, hook flash 0-0.45 s, loop tail, progress bar, poll/question CTA, both layouts allowed) and design the rest per story:
- **One full-length transparent HyperFrames overlay per reel**: `gen_hf.py` writes `hf/index.html` from word times (every card/element lands on its word), renders with `npx hyperframes render --format mov` (~3 min for 24 s on 2 CPUs, `--workers 1` while ffmpeg is busy). `compose.py` puts it over the cut, burns captions after it, adds the progress bar and masters audio.
- **Per-reel identity:** a palette + caption accent (`captions_reel.py --accent`), a layout chosen from the framing (empty wall above the head -> cards up there; head low -> split screen with `--split-y` lowered), a story-specific hook, a music style (`sound.py`: calm / tech / news / tense) and SFX that match the visuals (typing clicks for typing, stamps for verdicts, chimes for payoffs).
- Worked examples: `examples/reel2-tech-crash-split` (split screen for the WHOLE reel: start the split at 0.30 s under the hook and end it after TOTAL; market-terminal look, ticker of phrases not invented prices, counters via GSAP onUpdate, tense bed, `--split-y 650` for a centred head), `examples/reel3-apple-vs-agents` (light debate cards above the head, blue vs red, calm bed) and `examples/reel4-interview-hack` (dark chat-app split screen, live typing synced to speech, neon green, tech bed).
- 4K/60 fps HDR phone footage is normal now: `render_segments.py` pre-scales to 1296x2304 inside the tone map (zooms stay sharp) and samples to 30 fps; framing comes from `reel.json` (`zoom`, `crop_k`, `emph`). It is slow (~3 min per segment): start it first, build graphics meanwhile.
- Covers: `cover.py ... --place top --accent HEX` when the face sits low. No emoji inside headline lines (Poppins has none); put one in `--emoji`.
- Check stills at FULL size before fixing text glitches: downscaled thumbnails can fake overlapping text. Keep the progress bar a different colour from anything at the top edge (ticker, header).
- Loudness: `compose.py` corrects once if the limiter pulls the result more than 0.4 LU off -14.

## 5. House style (approved Nov 2026)

Palette: yellow #FFE500, dark navy glass rgba(14,16,34,.85), white. Font: Poppins Bold. 1080x1920, 30 fps.
- **Hook 0-1.5 s (changed 2026-11-02):** face full screen from frame 0 with a punch-in zoom, curiosity headline as a big text sticker over the wall/chest (not over the face), bass impact. No full-screen graphic opener (see 0b).
- **Loop tail (last 0.45 s):** match the first frame (same face framing + the same headline sticker) so the replay is seamless.
- **Titles** (top, y~250, boxed): yellow box with black text for the hook title, black box with white text for the rest.
- **Karaoke captions (ASS, burned last):** Poppins Bold 98, white, 9 px black outline, shadow 4; the active word is yellow at 112%, and each chunk pops in from 90%. Chunks of 1-3 words / <=15 chars, broken at pauses > 0.3 s and at sentence starts. Bottom margin 400 (330 in cards mode); on the divider (y 900) during split screen.
- **Layout A, floating cards (talking/opinion):** face full screen; glass cards (rounded 46, yellow 4 px rim, shadow) pop in over the chest (y~830-1470), gentle bob, exit by shrinking.
- **Layout B, split screen (visual-heavy):** a panel slides into the top 960 px with a yellow divider while the full video smoothly shrinks to 72% and slides to y=860 over a blurred, darkened copy of itself. Never crop the face into a strip (Darsh rejected that).
- **Elements:** feature tiles tick in on each word, a calendar drops on the date, flags pop on "country", a poll card ("WOULD YOU TRUST IT? YES/NO 👇") on the question, a ringing bell 🔔 on "follow", a yellow 10 px progress bar along the top.
- **One full-screen cutaway max** (~2 s, e.g. a name card); everything else keeps the face visible.
- Deliver both layouts unless Darsh picks one.

## 6. Audio

- Voice (`make_final.py`): `arnndn` RNNoise (std.rnnn, mix 0.9), highpass 80, -2 dB at 250 Hz, +2.5 dB at 3.5 kHz, +1.5 dB treble, deesser. No compressor, no single-pass loudnorm (it pumps).
- Music (`audio_gen3.py`): an original synthesized bed (104 BPM, Am-F-C-G), sidechain-ducked under the voice. No copyrighted tracks. Offer a no-music version if he wants trending IG audio.
- SFX synced to graphics: impact on the hook, risers into cutaways, whooshes on panel/card in/out, pops on each tile/sticker, a ding on the bell, a riser into the loop tail.
- Master in two passes: measure (`highpass=f=75,ebur128=peak=true`), then a fixed gain G = -14 - I, then `aresample=192000,alimiter=limit=0.841:attack=5:release=50:level=false,aresample=48000`, AAC 256k. Report I and peak.

## 7. Export + self-check before sending

x264 medium CRF 17, High profile, yuv420p, bt709 tags, `+faststart`. Check: stills at the first frame, every panel/card moment, the poll and the last frame (last == first); nothing over the face; text inside x 90-950, y 240-1470 (except captions); captions match words.json; A/V durations match; loudness numbers. Fix and re-check at most 3 times.

Also deliver: `cover.py` (best face frame, dark gradient, 3-line headline with the middle line yellow, inside the centre 3:4 grid-safe area) and post_caption.txt (hook line, 2-3 lines of news, a YES/NO question, "Follow for daily AI news & hacks", 10-15 hashtags). For news reels, re-verify the facts with a web search on the day.

## 8. Remind Darsh when relevant

Film 4K 30 fps with HDR Video off, phone at eye level, light in front, a clip-on mic, hands at chest height, a 1-2 s pause between lines. Send screenshots or screen recordings for real visuals. Turn on "Upload at highest quality" in Instagram.

## Cinematic depth style (N2 example)
Giant word BEHIND the head: `person_matte.py --win S,E ... -o matte.mkv` (u2net_human_seg), then
`compose_depth.py --back hf_back/back.mov --matte matte.mkv --overlay hf_front/front.mov ...`.
Layer order: video → back text → person cut-out → front cards → captions → bar.
Rules: back words 300–400px placed so the head overlaps their bottom third; front cards only above y0 (top of head); single-word captions (`--max-words 1 --size 112`). Matte only in depth windows (~1.4 s/frame on 2 CPU).
Asset density rule (Darsh, N2 v2): every 2–3 s needs a new visual beat — sticker/emoji pops in safe zones (top band, side edges, bottom corners), a background asset behind the person (bokeh, binary rain, neural net, server racks, RGB halo), confetti/tape/light-leak transitions, each with a matching SFX. Run the matte over the whole reel so back assets work everywhere. Never use random() in HyperFrames JS — precompute arrays in Python.
NN3 additions: plot-twist "freeze" = B&W + contrast hit on the base video via --base-vf `hue=s=0:enable='between(t\,A\,B)'` (escape commas) + PLOT TWIST stamp + glitch/stamp SFX. Depth cover: template/cover_depth.py (giant stat behind head via u2net matte, pill on top, two-line question block bottom, Noto emoji stickers; keep inside 3:4 crop y 240–1680).
Default style = CLASSIC SPLIT (Darsh prefers it over depth): face-first hook in free_above, slide split after 3s with an animated top panel (PANEL_H 760, slide = 780 - face top), one panel scene per beat, captions on the seam, hook visible on frame 0 and again at the end for the loop. Example: examples/reel-india-ai-paradox-split. Never fromTo(opacity) on a flash with immediateRender — use set+to.

## Virtual studio (background replacement) — NN4 example
Use when the real background looks bad. person_matte.py over the WHOLE reel → template/refine_matte.py (guided filter at full res, kills hair ghosting) →
shift speaker down (base-vf `crop=1080:1770:0:0,pad=1080:1920:0:150:black` + same on matte) to free the top for a "video wall".
hf_back = opaque set (gradient + grid + bokeh + glowing chart + ticker band at shoulder height + video wall with one scene per beat);
compose_depth.py with --back = set. Wall content must end above the head top (keep the wall at y 140–580). New music style: sound.py "hype" (140 bpm trap).

## Content-first studio (Darsh, NN4 v2) — preferred for news reels
- The background content is the star; the speaker is a small presenter: scale 0.6 at x=216,y=768 (base-vf `scale=648:1152,pad=1080:1920:216:768:black`),
  matte via `template/place_matte.py matte_r.mkv matte_p.mkv 0.6 216 768` (fades the box sides so the cut never shows), news desk in the FRONT layer at y 1700+ hides the body cut; captions sit on the desk (`--margin 70 --size 92`).
- Video wall 1000x900 (y 100–1000) holds one scene per beat; ticker band at y 1040 behind the head; chart/bokeh on the sides.
- Start every reel with a 0.1–0.3 s intro sting (shutter bars + spinning logo + white flash, front layer, z 80).
- Real brand logos: `npm pack @lobehub/icons-static-svg` / `simple-icons` (npm registry works when the web is blocked). Inline the SVG (currentColor) so CSS can colour it; copies in assets/logos/. No photos of real people.

## Classic split + Darsh's rules (₹399 ChatGPT Go example) — "old way"
When Darsh says "old way": examples/reel-chatgpt-go-399-split. Checklist baked in: 0.2 s shutter intro with the brand logo, face-first hook in free_above,
stickers pop around the face (never on it), slide split after ~5 s (slide = 780 - face top, no blur bars), one animated panel scene per beat
(timeline/calendar/phone notifications/app walkthrough with tap cursor/cancel confetti/share), flash+light-leak on every scene cut with whoosh,
captions on the seam, hook again at the end for the loop, colour-fix purple light with --base-vf. Logos inlined from assets/logos (openai, claude, anthropic).
Don't GSAP-tween a property that CSS also sets via transform (lint error) — use fromTo.

## QUALITY RULES (Darsh: "camera quality is dropping") — mandatory
- Never enlarge a 1080p source: render_segments.py now disables drift zoom + punch-ins when the source is < 4K (zoom moves only for 4K).
- Intermediates x264 CRF 6; final x264 CRF 13 preset slow tune film (≈40 Mbps at 1080x1920) — Instagram re-encodes, so feed it the cleanest file.
- Only colour-correct when the light is bad (purple/pink); good daylight footage gets no --base-vf grade.
- Front camera footage is mirrored (shirt text backwards) → --base-vf hflip.
- Ask Darsh to record 4K 30fps (iPhone Settings → Camera → Record Video), and to enable Instagram "Upload at highest quality".
- reel.json "drop": [[FROM,nth,TO,nth]] removes a spoken span (used to cut a line we can't truthfully show).

## Full-screen "face scan" surprise (AI midterms example)
Classic split can drop away mid-reel (two --split ranges) for a full-screen beat: a HUD box tracks the face from faces.json boxes
(mirror x when the video is hflipped), a scan line sweeps (animate y, not top), verdict tags flip colour, and the VIDEO itself glitches via
--base-vf `rgbashift/noise ... :enable='between(t\,A\,B)'`. Jitter a child wrapper with absolute x values (relative "+=" on a tracked element is a lint error).
4K HDR sources render slowly (~10 min for 38 s) — run render_segments.py in the background and poll for "done".
