"""N1 'Genie 4 builds worlds' — HyperFrames overlay. Look: night-sky game world in a top panel (split from 'world').
Face-first frame 0 with the hook in the free zone from faces.json; slide-mode split; loop back to frame 0."""
import json, sys, html as H, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def E(w, n=1): return round(word_time(w, n)[1], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')

FZ = json.load(open("faces.json"))
CY, IND, PINK = "#3BE8FF", "#0B1026", "#FF5FA2"
PANEL_H = 760
SPLIT = (T("WORLD") - 0.15, SPEECH_END)
HOOK_TOP = FZ["free_above"][0] + 4 if FZ["free_above"][1] - FZ["free_above"][0] >= 170 else FZ["free_below"][0]
P1, P2 = "make it rain", "add a person"
def typed(txt, cls): return "".join(f'<span class="{cls}">{H.escape(c) if c != " " else "&nbsp;"}</span>' for c in txt)
random.seed(4)
drops = "".join(f'<div class="dr" style="left:{random.randint(10, 1060)}px;top:{random.randint(-300, 0)}px"></div>' for _ in range(46))
stars = "".join(f'<div class="st" style="left:{random.randint(0, 1070)}px;top:{random.randint(20, 300)}px"></div>' for _ in range(40))
hook = '<div class="hk"><div class="hk1">TYPE → A WORLD APPEARS 🤯</div></div>'

world = f'''<div class="pnl" id="pnl">
 <div class="sky"></div>{stars}
 <div class="sun" id="sun"></div>
 <svg class="mt" id="mt" width="1080" height="420" viewBox="0 0 1080 420"><polygon points="0,420 140,170 280,330 420,110 600,320 760,150 900,300 1080,190 1080,420" fill="#1d2a5c"/>
  <polygon points="0,420 200,260 360,380 540,230 720,370 880,260 1080,360 1080,420" fill="#24357a"/></svg>
 <div class="gr" id="gr"></div>
 {"".join(f'<div class="tr tr{i}" style="left:{x}px">🌲</div>' for i, x in enumerate([90, 230, 760, 900, 980]))}
 <div class="rain" id="rain">{drops}</div>
 <div class="walker" id="wk"><span style="display:inline-block;transform:scaleX(-1)">🚶</span></div>
 <div class="snd" id="snd"><span class="spk">🔊</span><span class="w w1"></span><span class="w w2"></span><span class="w w3"></span></div>
 {"".join(f'<div class="nt" id="nt{i}">{c}</div>' for i, c in enumerate("♪♫♪♫"))}
 <div class="badge" id="badge">GENIE 4 <span>· Google DeepMind</span></div>
 <div class="cmd" id="cmd"><span class="pr">›</span><span class="tx" id="tx1">{typed(P1, "c1")}</span><span class="tx" id="tx2">{typed(P2, "c2")}</span><span class="car" id="car"></span></div>
 <div class="lock" id="lock"><div class="lk">🔒</div><div>NOT PUBLIC YET</div><div class="ls">testers only · waitlist</div></div>
 <div class="game" id="game"><div class="gi">🎮</div><div>MAKE GAMES</div><div class="nc" id="nc">WITHOUT CODE <span>&lt;/&gt;</span></div></div>
 <div class="poll" id="poll"><div class="pq">WOULD YOU TRY IT?</div><div class="pb"><span class="y" id="py">YES 🎮</span><span class="n" id="pn">NO 🙅</span></div></div>
</div>'''

doc = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:MO;src:url(assets/fonts/DejaVuSansMono.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}}
.full{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.hz{{position:absolute;left:40px;right:40px;top:{HOOK_TOP}px;text-align:center}}
.hk1{{display:inline-block;font-size:70px;line-height:1.1;background:{IND};color:#fff;padding:16px 34px;border-radius:28px;border:5px solid {CY};box-shadow:0 0 0 6px rgba(59,232,255,.18),0 18px 40px rgba(0,0,0,.5)}}
.pnl{{position:absolute;left:0;top:0;width:1080px;height:{PANEL_H}px;overflow:hidden;border-bottom:10px solid {CY}}}
.sky{{position:absolute;inset:0;background:linear-gradient(180deg,#050816 0%,{IND} 45%,#1a1450 100%)}}
.st{{position:absolute;width:5px;height:5px;border-radius:50%;background:#fff;opacity:.7}}
.sun{{position:absolute;left:760px;top:120px;width:150px;height:150px;border-radius:50%;background:radial-gradient(circle,#fff6c7 0%,#ffd76a 55%,#ff9d4d 100%);box-shadow:0 0 60px rgba(255,200,90,.6)}}
.mt{{position:absolute;left:0;top:250px;transform-origin:bottom center}}
.gr{{position:absolute;left:0;right:0;top:580px;height:200px;background:linear-gradient(180deg,#1f7a4d,#0f4a2e);transform-origin:bottom center}}
.tr{{position:absolute;top:470px;font-size:110px}}
.rain{{position:absolute;inset:0}}
.dr{{position:absolute;width:4px;height:46px;border-radius:2px;background:linear-gradient(180deg,rgba(150,220,255,0),rgba(150,220,255,.9))}}
.walker{{position:absolute;left:-140px;top:470px;font-size:130px}}
.snd{{position:absolute;left:70px;top:150px;display:flex;align-items:center;gap:10px}}
.spk{{font-size:100px}} .w{{display:inline-block;width:26px;height:80px;border:7px solid {CY};border-left:none;border-top-color:transparent;border-bottom-color:transparent;border-radius:0 50% 50% 0}}
.w2{{height:120px;width:40px}} .w3{{height:160px;width:56px}}
.nt{{position:absolute;left:330px;top:300px;font-size:70px;color:{PINK}}}
.badge{{position:absolute;left:40px;top:40px;font-size:62px;background:rgba(5,8,22,.75);border:4px solid {CY};padding:6px 28px;border-radius:22px}}
.badge span{{font-family:PM;font-size:34px;color:#b9c6ff}}
.cmd{{position:absolute;left:60px;right:60px;top:620px;height:100px;border-radius:30px;background:rgba(5,8,22,.85);border:4px solid {CY};display:flex;align-items:center;padding:0 30px;font-family:MO;font-size:46px;white-space:nowrap}}
.pr{{color:{CY};margin-right:18px}} .tx{{position:absolute;left:88px;display:flex}} .car{{position:absolute;right:40px;width:5px;height:54px;background:{CY}}}
.lock,.game,.poll{{position:absolute;left:120px;right:120px;top:150px;text-align:center;background:rgba(5,8,22,.92);border:5px solid {CY};border-radius:40px;padding:34px 20px;font-size:64px}}
.lk,.gi{{font-size:120px;line-height:1.1}} .ls{{font-family:PM;font-size:38px;color:#b9c6ff;margin-top:6px}}
.nc{{font-size:54px;color:{PINK};margin-top:6px}} .nc span{{font-family:MO;text-decoration:line-through}}
.pq{{font-size:62px}} .pb{{display:flex;gap:30px;margin-top:26px;justify-content:center}}
.pb span{{font-size:64px;padding:20px 40px;border-radius:26px}} .y{{background:{CY};color:{IND}}} .n{{background:{PINK};color:#fff}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{clip("panel", *SPLIT, world, 5)}
{clip("hook", 0, SPLIT[0] + 0.05, f'<div class="hz" id="hz">{hook}</div>', 30)}
{clip("tail", SPEECH_END, TOTAL, f'<div class="hz" id="tz">{hook}</div>', 60)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#hz",{{scale:1.0}},{{scale:1.05,duration:{SPLIT[0] - 0.2:.3f},ease:"sine.inOut"}},0)
  .to("#hz",{{opacity:0,y:-30,duration:0.2}},{SPLIT[0] - 0.15:.3f});
tl.fromTo("#tz",{{opacity:0,scale:0.85}},{{opacity:1,scale:1.0,duration:{TOTAL - SPEECH_END - 0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});
// panel slides in with the video (slide-mode split), out at the end
tl.fromTo("#pnl",{{y:-{PANEL_H + 20}}},{{y:0,duration:0.25,ease:"power3.out"}},{SPLIT[0]:.3f})
  .to("#pnl",{{y:-{PANEL_H + 20},duration:0.22,ease:"power3.in"}},{SPLIT[1] - 0.22:.3f});
// the world builds itself while he says "builds a whole world while you are walking through it"
const b0 = {SPLIT[0] + 0.2:.3f};
tl.from("#sun",{{scale:0,duration:0.4,ease:"back.out(2)"}},b0)
  .from("#mt",{{scaleY:0,duration:0.6,ease:"power3.out"}},b0 + 0.2)
  .from("#gr",{{scaleY:0,duration:0.4,ease:"power3.out"}},b0 + 0.5)
  .from(".tr",{{scale:0,y:60,duration:0.3,ease:"back.out(2.5)",stagger:0.12}},b0 + 0.8)
  .from(".st",{{opacity:0,duration:0.3,stagger:0.01}},b0);
tl.from("#badge",{{x:-500,duration:0.35,ease:"power3.out"}},{T("GENIE"):.3f});
// prompt 1: "make it rain" typed as he says it, rain on "rains"
tl.set([".c1",".c2"],{{opacity:0}},0).set(["#cmd"],{{opacity:0}},0)
  .to("#cmd",{{opacity:1,duration:0.2}},{T("TYPE") - 0.1:.3f});
const a1 = {T("MAKE"):.3f}, b1 = {E("RAIN"):.3f}, n1 = {len(P1)};
for (let i=0;i<n1;i++) tl.set(`#tx1 .c1:nth-child(${{i+1}})`,{{opacity:1}}, a1 + (b1-a1)*i/n1);
tl.set(".rain",{{opacity:0}},0).set(".rain",{{opacity:1}},{T("RAINS") - 0.1:.3f})
  .to("#sun",{{opacity:0.25,duration:0.4}},{T("RAINS"):.3f});
document.querySelectorAll(".dr").forEach((d,i)=>{{ tl.fromTo(d,{{y:0}},{{y:1000,duration:0.55,ease:"none",repeat:7}},{T("RAINS") - 0.1:.3f} + (i%10)*0.05); }});
tl.to(".rain",{{opacity:0,duration:0.3}},{T("TYPE", 2) + 0.4:.3f});
// prompt 2: "add a person" -> walker
tl.set("#tx1",{{opacity:0}},{T("TYPE", 2) - 0.05:.3f});
const a2 = {T("ADD"):.3f}, b2 = {E("PERSON"):.3f}, n2 = {len(P2)};
for (let i=0;i<n2;i++) tl.set(`#tx2 .c2:nth-child(${{i+1}})`,{{opacity:1}}, a2 + (b2-a2)*i/n2);
tl.to("#wk",{{x:560,duration:{T("AND") + 0.6 - T("SOMEONE"):.3f},ease:"none"}},{T("SOMEONE"):.3f})
  .to("#wk",{{y:-14,duration:0.15,yoyo:true,repeat:{int((T("AND") + 0.6 - T("SOMEONE")) / 0.3) * 2 - 1}}},{T("SOMEONE"):.3f})
  .to("#cmd",{{opacity:0,duration:0.2}},{T("AND"):.3f});
// sounds
tl.set(["#snd",".nt"],{{opacity:0}},0).to("#snd",{{opacity:1,duration:0.2}},{T("SOUNDS") - 0.1:.3f});
for (let k=0;k<4;k++) tl.fromTo(".w",{{opacity:0.2,scale:0.8}},{{opacity:1,scale:1.05,duration:0.18,stagger:0.08}},{T("SOUNDS"):.3f}+k*0.3);
for (let i=0;i<4;i++) tl.fromTo(`#nt${{i}}`,{{opacity:1,x:0,y:0}},{{opacity:0,x:120+i*90,y:-200,duration:1.1,ease:"power1.out"}},{T("SOUNDS"):.3f}+i*0.18);
// can't use it yet -> lock; games without code; poll
tl.set(["#lock","#game","#poll"],{{opacity:0}},0)
  .to("#snd",{{opacity:0,duration:0.15}},{T("CAN'T") - 0.1:.3f})
  .fromTo("#lock",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{T("CAN'T") - 0.05:.3f})
  .to("#lock",{{opacity:0,scale:0.95,duration:0.18}},{T("IMAGINE") - 0.15:.3f})
  .fromTo("#game",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{T("IMAGINE") - 0.05:.3f})
  .from("#nc",{{opacity:0,y:20,duration:0.2}},{T("WITHOUT"):.3f})
  .to("#game",{{opacity:0,scale:0.95,duration:0.18}},{T("WOULD") - 0.15:.3f})
  .fromTo("#poll",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{T("WOULD") - 0.05:.3f})
  .from("#py",{{x:-200,opacity:0,duration:0.2}},{T("TRY"):.3f})
  .from("#pn",{{x:200,opacity:0,duration:0.2}},{T("TRY") + 0.12:.3f});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>'''
open("hf/index.html", "w").write(doc)
json.dump({"split": SPLIT, "panel_h": PANEL_H, "hook_top": HOOK_TOP, "speech_end": SPEECH_END, "total": TOTAL}, open("hf/events.json", "w"), indent=1)
print("ok", TOTAL, "split", SPLIT, "hook_top", HOOK_TOP)
