"""Reel 3 'Apple vs AI agents' — HyperFrames overlay composition, generated from word timings.
Look: clean light 'debate' cards floating in the empty wall ABOVE the head; electric blue (Apple side) vs red (AI side)."""
import json, sys
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, cls="card", z=10):
    return (f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')

BLUE, RED, INK = "#2F6BFF", "#FF3B30", "#0B0B0F"
ev = {}
ev["c1"] = (T("CEO") - 0.15, T("JOHN") - 0.06)
ev["c2"] = (T("JOHN") - 0.04, T("AND") + 0.1)
ev["c3"] = (T("BELIEVE") - 0.2, T("MAKING") - 0.06)
ev["c4"] = (T("MAKING") - 0.04, T("MEANWHILE") - 0.06)
ev["c5"] = (T("MEANWHILE") - 0.04, T("WHO") - 0.06)
ev["c6"] = (T("WHO") - 0.04, SPEECH_END)

APPS = [("📷", "#FF9F0A", "#FF375F"), ("🗺️", "#30D158", "#0A84FF"), ("🎵", "#FF2D55", "#AF52DE"),
        ("💬", "#34C759", "#30B0C7"), ("📅", "#FF453A", "#FF9F0A"), ("🛒", "#5E5CE6", "#0A84FF")]
def app_grid(cls):
    return "".join(f'<div class="app {cls}" style="background:linear-gradient(145deg,{a},{b})">{e}</div>' for e, a, b in APPS)

hook_inner = f'''<div class="hk-wrap"><div class="hk-l"><div class="hk-small">ONE COMPANY</div><div class="hk-big" style="color:{INK}">APPLE</div></div>
<div class="hk-r"><div class="hk-small" style="color:#ff8a80">VS</div><div class="hk-big" style="color:#fff">EVERY AI<br>COMPANY</div></div>
<div class="hk-vs">VS</div><div class="hk-q">Who's right? 🤔</div></div>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:{INK}}}
.card{{position:absolute;left:70px;top:250px;width:940px}}
.glass{{background:rgba(255,255,255,.95);border-radius:40px;padding:34px 40px;box-shadow:0 24px 60px rgba(0,0,0,.28);border:3px solid #E7E9F0}}
.dark{{background:rgba(14,15,20,.94);color:#fff;border:3px solid #2a2c36}}
.tag{{display:inline-block;font-size:30px;padding:8px 22px;border-radius:99px;background:{BLUE};color:#fff;letter-spacing:.04em}}
.tag.red{{background:{RED}}}
.h1{{font-size:66px;line-height:1.05;margin-top:14px;letter-spacing:-.01em}}
.sub{{font-family:PM;font-size:38px;margin-top:14px;color:#3a3d48}}
.dark .sub{{color:#c9ccd6}}
.name{{font-size:76px;letter-spacing:-.01em;line-height:1}}
.role{{font-family:PM;font-size:34px;color:#6b6f7c;margin-top:6px}}
.row{{display:flex;align-items:center;gap:20px;margin-top:22px}}
.pill{{position:relative;display:inline-block;font-size:44px;padding:12px 30px;border-radius:24px;background:#EEF2FF;color:{BLUE}}}
.strike{{position:absolute;left:-10px;right:-10px;top:50%;height:8px;background:{RED};border-radius:4px;transform-origin:left center}}
.stamp{{display:inline-block;font-size:40px;color:{RED};border:5px solid {RED};border-radius:16px;padding:6px 18px;transform:rotate(-6deg)}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-top:24px}}
.app{{height:118px;border-radius:30px;display:flex;align-items:center;justify-content:center;font-size:62px;box-shadow:0 8px 18px rgba(0,0,0,.18)}}
.bot{{position:absolute;right:30px;top:24px;font-size:96px}}
.no{{position:absolute;right:36px;bottom:30px;font-size:46px;color:#fff;background:{BLUE};padding:10px 26px;border-radius:20px}}
.big{{font-size:110px;line-height:1;color:{RED};margin-top:10px}}
.bubble{{margin-top:24px;background:#1d2030;border-radius:30px;padding:22px 30px;font-size:44px;display:inline-flex;gap:16px;align-items:center}}
.btns{{display:flex;gap:24px;margin-top:26px}}
.btn{{flex:1;text-align:center;font-size:52px;padding:26px 10px;border-radius:30px}}
.b1{{background:{BLUE};color:#fff}} .b2{{background:{INK};color:#fff}}
.cm{{display:inline-block;margin-top:22px;font-size:48px;background:#FFE14D;padding:10px 26px;border-radius:99px}}
.c5x{{padding:26px 36px}} .c5x .h1{{font-size:54px;margin-top:10px}} .c5x .sub{{margin-top:6px;font-size:34px}} .c5x .grid{{margin-top:14px;gap:12px}} .c5x .app{{height:92px;font-size:48px;border-radius:24px}} .c5x .bubble{{margin-top:14px;font-size:40px;padding:16px 26px}}
.full{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}}
.hk-wrap{{position:absolute;inset:0}}
.hk-l,.hk-r{{position:absolute;top:0;bottom:0;width:540px;display:flex;flex-direction:column;justify-content:flex-start;padding-top:470px;align-items:center;text-align:center}}
.hk-l{{left:0;background:#F4F5F8}} .hk-r{{right:0;background:#0E0F14}}
.hk-small{{font-size:34px;letter-spacing:.12em;color:#8a8f9c}}
.hk-big{{font-size:78px;line-height:1.05;margin-top:8px}}
.hk-vs{{position:absolute;left:440px;top:860px;width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,{BLUE} 50%,{RED} 50%);color:#fff;font-size:84px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 12px rgba(255,255,255,.9)}}
.hk-q{{position:absolute;left:0;right:0;top:1250px;text-align:center;font-size:58px;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.6)}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{clip("hook", 0, 0.5, f'<div class="full" id="hkz">{hook_inner}<div class="flash" id="fl"></div></div>', "full", 50)}
{clip("c1", *ev["c1"], '<div class="glass in"><span class="tag">BREAKING</span><div class="h1">Apple\'s new CEO said something 😬</div><div class="sub" id="c1s">…every AI company will hate.</div></div>')}
{clip("c2", *ev["c2"], f'<div class="glass in"><div class="name">JOHN TERNUS</div><div class="role">CEO, Apple</div><div class="row"><span class="sub" style="margin:0">won\'t ship</span><span class="pill" id="pl">AI for AI\'s sake<span class="strike" id="sk"></span></span></div><div class="row"><span class="stamp" id="st">✕ NOT HAPPENING</span></div></div>')}
{clip("c3", *ev["c3"], f'<div class="glass in" style="position:relative"><span class="tag red">THE BIG QUESTION</span><div class="h1">Will AI agents<br>replace apps?</div><div class="grid">{app_grid("a3")}</div><div class="bot" id="bot">🤖</div><div class="no" id="no">Apple: NO 🙅</div></div>')}
{clip("c4", *ev["c4"], '<div class="glass in"><div class="sub" style="margin:0">Making products is</div><div class="big" style="color:#2F6BFF">DEEPLY<br>HUMAN ❤️</div></div>')}
{clip("c5", *ev["c5"], f'<div class="glass dark in c5x"><span class="tag red">MEANWHILE</span><div class="h1">Every other AI company 🤖</div><div class="sub" id="c5s">is betting the opposite 💰</div><div class="grid" id="g5">{app_grid("a5")}</div><div class="bubble" id="bb">🤖 One agent. Every app.</div></div>')}
{clip("c6", *ev["c6"], '<div class="glass in" style="text-align:center"><div class="h1" style="margin:0">WHO\'S RIGHT?</div><div class="btns"><div class="btn b1" id="o1">🍏 APPLE</div><div class="btn b2" id="o2">🤖 AI COS</div></div><div class="cm" id="cm">COMMENT 👇</div></div>')}
{clip("tail", SPEECH_END, TOTAL, f'<div class="full" id="tlz">{hook_inner}</div>', "full", 60)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
// hook: 1.10 -> 1.0 zoom, white flash out
tl.fromTo("#hkz",{{scale:1.10}},{{scale:1.0,duration:0.5,ease:"power2.out"}},0)
  .to("#fl",{{opacity:0.7,duration:0.1,ease:"none"}},0.38);
// tail: fades in, zooms 1.0 -> 1.10 so the last frame == the first frame
tl.fromTo("#tlz",{{opacity:0,scale:1.0}},{{opacity:1,duration:0.12,ease:"none"}},{SPEECH_END:.3f})
  .to("#tlz",{{scale:1.10,duration:{TOTAL - SPEECH_END - 0.02:.3f},ease:"power2.in"}},{SPEECH_END:.3f});
// card in/out
const cards = {json.dumps({k: v for k, v in ev.items()})};
for (const [id,[s,e]] of Object.entries(cards)) {{
  tl.fromTo(`#${{id}} .in`,{{y:-50,scale:0.9,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.32,ease:"back.out(1.5)"}},s)
    .to(`#${{id}} .in`,{{y:-30,scale:0.96,opacity:0,duration:0.2,ease:"power2.in"}},e-0.22);
}}
tl.from("#c1s",{{opacity:0,y:20,duration:0.25}},{T("HATE") - 0.25:.3f});
tl.from("#pl",{{scale:0.5,opacity:0,duration:0.28,ease:"back.out(2)"}},{T("SHIP"):.3f})
  .fromTo("#sk",{{scaleX:0}},{{scaleX:1,duration:0.25,ease:"power3.out"}},{T("SAKE"):.3f})
  .from("#st",{{scale:2.2,opacity:0,duration:0.22,ease:"power3.in"}},{T("AI", 3):.3f});
tl.from(".a3",{{scale:0,duration:0.25,ease:"back.out(2)",stagger:0.05}},{ev["c3"][0] + 0.2:.3f})
  .from("#bot",{{x:200,opacity:0,duration:0.3,ease:"power3.out"}},{T("AGENTS"):.3f})
  .to("#bot",{{x:-560,y:170,scale:0.8,duration:0.5,ease:"power2.inOut"}},{T("REPLACE"):.3f})
  .to(".a3",{{scale:0.75,opacity:0.35,duration:0.3,stagger:0.03}},{T("REPLACE") + 0.2:.3f})
  .from("#no",{{scale:2,opacity:0,duration:0.22,ease:"power3.in"}},{T("APPS"):.3f})
  .to("#bot",{{x:300,opacity:0,duration:0.3}},{T("APPS") + 0.2:.3f})
  .to(".a3",{{scale:1,opacity:1,duration:0.3}},{T("APPS") + 0.2:.3f});
tl.from("#c4 .big",{{scale:0.6,opacity:0,duration:0.3,ease:"back.out(2)"}},{T("DEEPLY"):.3f});
tl.from("#c5s",{{opacity:0,y:20,duration:0.25}},{T("BETTING"):.3f})
  .from(".a5",{{scale:0,duration:0.22,ease:"back.out(2)",stagger:0.04}},{ev["c5"][0] + 0.3:.3f})
  .to(".a5",{{y:150,x:(i)=>(2.5-i)*150,scale:0.2,opacity:0,duration:0.4,ease:"power2.in",stagger:0.03}},{T("REPLACE", 2):.3f})
  .from("#bb",{{scale:0,opacity:0,duration:0.3,ease:"back.out(2)"}},{T("APPS", 2):.3f});
tl.from("#o1",{{x:-300,opacity:0,duration:0.3,ease:"power3.out"}},{T("APPLE", 2) - 0.1:.3f})
  .from("#o2",{{x:300,opacity:0,duration:0.3,ease:"power3.out"}},{T("COMPANIES") - 0.4:.3f})
  .from("#cm",{{scale:0,duration:0.25,ease:"back.out(2)"}},{T("COMMENT"):.3f});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>'''
open("hf/index.html", "w").write(html)
json.dump({"cards": ev, "speech_end": SPEECH_END, "total": TOTAL}, open("hf/events.json", "w"), indent=1)
print("ok", TOTAL)
