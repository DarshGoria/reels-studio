"""Reel 3 'India #2 at AI shopping' — first reel on growth rules v1 (analytics/2026-11-02.md):
face from frame 0, hook as a sticker over the chest (visible on frame 0), payoff < 1.5 s, save ask early (chip from 2 s).
Look: clean white cards, India saffron + green accents, pops against the purple room light. Floating cards over the chest."""
import json, sys, html as H
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def E(w, n=1): return round(word_time(w, n)[1], 3)
def clip(id_, s, e, inner, cls="full", z=10):
    return (f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')

SAF, GRN, INK = "#FF8A00", "#1FAE5B", "#121318"
FZ = json.load(open("faces.json"))
HOOK = (0.0, T("ABOUT") - 0.08)
C1 = (T("ABOUT") - 0.06, T("SECOND") - 0.08)
C2 = (T("SECOND") - 0.06, T("HERE'S") - 0.08)
C3 = (T("HERE'S") - 0.06, T("TABLE") - 0.02)
C4 = (T("TABLE") - 0.02, SPEECH_END)
SPLIT = (T("ABOUT") - 0.06, SPEECH_END)          # cards live in a top panel; the face shrinks into the bottom half
PANEL_H = 820
PROMPT = "Compare these 3 phones under ₹25,000 for camera & battery. Give me a table."
TY0, TY1 = T("COMPARE"), E("TABLE")
chars = "".join(f'<span class="ch">{H.escape(c) if c != " " else " "}</span>' for c in PROMPT)

hook = '''<div class="hk in"><div class="hk1">INDIA 🇮🇳 IS #2</div><div class="hk2">IN THE WORLD AT THIS 👇</div></div>'''
rows = [("Phone A", "⭐⭐⭐⭐", "🔋🔋🔋", False), ("Phone B", "⭐⭐⭐⭐⭐", "🔋🔋🔋🔋", True), ("Phone C", "⭐⭐⭐", "🔋🔋🔋🔋🔋", False)]
table = "".join(f'<div class="tr{" best" if b else ""}" id="r{i}"><span class="tn">{n}{" 🏆" if b else ""}</span><span>{c}</span><span>{bt}</span></div>'
                for i, (n, c, bt, b) in enumerate(rows))

doc = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:MO;src:url(assets/fonts/DejaVuSansMono.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:{INK}}}
.full{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.zone{{position:absolute;left:70px;top:255px;width:940px}}
.hzone{{position:absolute;left:70px;top:{FZ['free_above'][0] + 4}px;width:940px}}
.pnl{{position:absolute;left:0;top:0;width:1080px;height:{PANEL_H}px;background:linear-gradient(180deg,#1b1030 0%,#120a22 100%);border-bottom:10px solid {SAF};box-shadow:0 10px 40px rgba(0,0,0,.5)}}
.pnl::after{{content:'';position:absolute;left:0;right:0;bottom:-20px;height:10px;background:{GRN}}}
.card{{background:rgba(255,255,255,.96);border-radius:40px;padding:24px 34px;box-shadow:0 24px 60px rgba(0,0,0,.45);border-top:10px solid {SAF};border-bottom:10px solid {GRN}}}
.hk{{text-align:center}}
.hk1{{display:inline-block;font-size:82px;line-height:1.05;background:#fff;color:{INK};padding:10px 34px;border-radius:28px;box-shadow:0 18px 40px rgba(0,0,0,.45);border-bottom:10px solid {SAF}}}
.hk2{{display:inline-block;margin-top:10px;font-size:44px;background:{SAF};color:#fff;padding:8px 30px;border-radius:99px;box-shadow:0 12px 30px rgba(0,0,0,.4)}}
.chip{{position:absolute;left:44px;top:120px;font-size:36px;background:rgba(18,19,24,.82);color:#fff;padding:10px 24px;border-radius:99px;border:3px solid {SAF}}}
.big{{font-size:190px;line-height:1;color:{SAF};letter-spacing:-.03em}}
.sub{{font-family:PM;font-size:44px;margin-top:6px}}
.ttl{{font-size:46px;margin-bottom:10px}}
.bar{{display:flex;align-items:center;gap:16px;margin:8px 0;font-size:38px}}
.lab{{width:310px;white-space:nowrap}} .trk{{flex:1;height:58px;background:#eef0f4;border-radius:16px;overflow:hidden}}
.fil{{height:100%;border-radius:16px;transform-origin:left center;display:flex;align-items:center;justify-content:flex-end;padding-right:16px;color:#fff;font-size:34px}}
.badge{{display:inline-block;margin-left:10px;font-size:30px;background:{SAF};color:#fff;padding:4px 14px;border-radius:99px;vertical-align:middle}}
.pr{{font-family:MO;font-size:38px;line-height:1.45;background:#f4f5f8;border-radius:22px;padding:22px 24px;min-height:200px}}
.caret{{display:inline-block;width:4px;height:44px;background:{SAF};vertical-align:middle;margin-left:3px}}
.th,.tr{{display:grid;grid-template-columns:1.3fr 1.2fr 1.2fr;gap:12px;font-size:36px;padding:9px 18px;border-radius:18px;align-items:center}}
.th{{font-size:32px;color:#6b6f7c}} .tr{{background:#f4f5f8;margin-top:8px}} .tn{{font-size:38px}}
.best{{background:#e9f8ef;border:4px solid {GRN}}}
.save{{position:absolute;left:0;right:-10px;top:-92px;text-align:right}}
.save span{{display:inline-block;font-size:72px;color:#fff;background:{GRN};padding:10px 40px;border-radius:30px;box-shadow:0 18px 40px rgba(0,0,0,.45);transform:rotate(-4deg)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{clip("panel", *SPLIT, '<div class="pnl" id="pnl"></div>', z=5)}
{clip("hook", *HOOK, f'<div class="hzone" id="hz">{hook}</div>', z=30)}
{clip("chip", 2.0, SPEECH_END, '<div class="chip" id="chipi">🔖 Save this for later</div>', z=25)}
{clip("c1", *C1, '<div class="zone"><div class="card in"><div class="big" id="pct">0%</div><div class="sub" id="c1s">of Indians use AI before buying 🛒</div></div></div>')}
{clip("c2", *C2, f'<div class="zone"><div class="card in"><div class="ttl">AI SHOPPING · WORLD RANK</div><div class="bar"><span class="lab">🇨🇳 China</span><div class="trk"><div class="fil" id="b1" style="width:80%;background:#9aa0ad">80%</div></div></div><div class="bar"><span class="lab">🇮🇳 India<span class="badge">#2</span></span><div class="trk"><div class="fil" id="b2" style="width:76%;background:{SAF}">76%</div></div></div><div class="bar"><span class="lab">🌍 World</span><div class="trk"><div class="fil" id="b3" style="width:53%;background:#c7cbd4">53%</div></div></div></div></div>')}
{clip("c3", *C3, f'<div class="zone"><div class="card in"><div class="ttl">📋 MY PROMPT</div><div class="pr">{chars}<span class="caret" id="caret"></span></div></div></div>')}
{clip("c4", *C4, f'<div class="zone"><div class="save" id="sv"><span>🔖 SAVE THIS</span></div><div class="card in"><div class="th"><span>Under ₹25K</span><span>📷 Camera</span><span>🔋 Battery</span></div>{table}</div></div>')}
{clip("tail", SPEECH_END, TOTAL, f'<div class="hzone" id="tz">{hook}</div>', z=60)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
// hook: fully visible on frame 0 (no pop-in delay), a little breathing scale, exits before the first card
tl.fromTo("#hz",{{scale:1.0}},{{scale:1.06,duration:{HOOK[1] - 0.3:.3f},ease:"sine.inOut"}},0)
  .to("#hz",{{opacity:0,y:-30,scale:0.95,duration:0.2,ease:"power2.in"}},{HOOK[1] - 0.22:.3f});
// tail: the same sticker returns and lands on the frame-0 state (scale 1.0, full opacity) -> loop
tl.fromTo("#tz",{{opacity:0,scale:0.85}},{{opacity:1,scale:1.0,duration:{TOTAL - SPEECH_END - 0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});
tl.fromTo("#pnl",{{y:-{PANEL_H + 30}}},{{y:0,duration:0.25,ease:"power3.out"}},{SPLIT[0]:.3f})
  .to("#pnl",{{y:-{PANEL_H + 30},duration:0.22,ease:"power3.in"}},{SPLIT[1] - 0.22:.3f});
tl.from("#chipi",{{x:-300,duration:0.35,ease:"power3.out"}},2.0);
const cards = {json.dumps({"c1": C1, "c2": C2, "c3": C3, "c4": C4})};
for (const [id,[s,e]] of Object.entries(cards)) {{
  tl.fromTo(`#${{id}} .in`,{{y:60,scale:0.9,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.3,ease:"back.out(1.5)"}},s);
  tl.to(`#${{id}} .in`,{{y:-30,opacity:0,scale:0.96,duration:0.18,ease:"power2.in"}},e-0.2);
}}
// 76% counter
const c = {{v:0}};
tl.to(c,{{v:76,duration:0.8,ease:"power2.out",onUpdate:()=>{{document.querySelector("#pct").textContent = Math.round(c.v)+"%";}}}},{T("76%"):.3f});
tl.from("#c1s",{{opacity:0,y:20,duration:0.25}},{T("INDIANS", 2):.3f});
// ranking bars
tl.fromTo(["#b1","#b2","#b3"],{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power3.out",stagger:0.15}},{C2[0] + 0.15:.3f})
  .from("#c2 .badge",{{scale:0,duration:0.3,ease:"back.out(3)"}},{T("ONLY"):.3f});
// prompt typing synced to speech
tl.set("#c3 .ch",{{opacity:0}},0);
const n = {len(PROMPT)}, t0 = {TY0:.3f}, t1 = {TY1:.3f};
for (let i=0;i<n;i++) tl.set(`#c3 .ch:nth-child(${{i+1}})`,{{opacity:1}}, t0 + (t1-t0)*i/n);
for (let k=0;k<6;k++) tl.set("#caret",{{opacity:k%2?0:1}},{C3[0]:.3f}+k*0.3);
tl.set("#caret",{{opacity:1}},t0);
// table rows + save stamp
tl.from(["#r0","#r1","#r2"],{{x:80,opacity:0,duration:0.25,ease:"power3.out",stagger:0.12}},{C4[0] + 0.1:.3f})
  .to("#r1",{{scale:1.04,duration:0.2,yoyo:true,repeat:1}},{C4[0] + 0.5:.3f})
  .fromTo("#sv",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power3.in"}},{T("SAVE"):.3f})
  .to("#chipi",{{opacity:0,duration:0.2}},{T("SAVE"):.3f});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>'''
open("hf/index.html", "w").write(doc)
json.dump({"split": SPLIT, "panel_h": PANEL_H, "hook": HOOK, "cards": {"c1": C1, "c2": C2, "c3": C3, "c4": C4}, "speech_end": SPEECH_END, "total": TOTAL},
          open("hf/events.json", "w"), indent=1)
print("ok", TOTAL)
