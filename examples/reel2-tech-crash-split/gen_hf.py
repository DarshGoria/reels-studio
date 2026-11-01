"""Reel 2 'Tech stocks lost $1 trillion' — SPLIT-SCREEN variant. HyperFrames overlay, split for the whole reel.
Look: market-crash terminal: black, alarm red, amber, ticker tape, a self-drawing crash chart, counters, a popping bubble."""
import json, sys, math
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def E(w, n=1): return round(word_time(w, n)[1], 3)
def clip(id_, s, e, inner, cls="", z=10):
    return (f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')

RED, AMB, GRN, BG = "#FF3B3B", "#FFB020", "#22D37A", "#07090C"
P0, P1 = 0.30, TOTAL                                    # split for the whole reel (the shrink happens under the hook)
SC = {
    "s1": (P0, T("REASON") - 0.12),
    "s2": (T("REASON") - 0.1, T("WE") - 0.08),
    "s3": (T("WE") - 0.06, T("AND", 2) - 0.08),
    "s4": (T("AND", 2) - 0.06, T("SO") - 0.08),
    "s5": (T("SO") - 0.06, T("YES") - 0.08),
    "s6": (T("YES") - 0.06, SPEECH_END),
}
# ticker: phrases only, no invented prices
TICK = "   ·   ".join(["TECH SELL-OFF ▼", "$1T WIPED OUT ▼", "AI SPENDING FEARS ▼", "OPENAI ROUND CUT ▼", "BUBBLE TALK ▲"] * 4)
pts = []
for i in range(41):
    x = 40 + i * 24
    y = 120 + 18 * math.sin(i * 0.9) + 6 * math.sin(i * 2.3)
    if i > 24: y += (i - 24) ** 1.6 * 14
    pts.append(f"{x:.0f},{y:.0f}")
PATH = "M" + " L".join(pts)
AREA = PATH + " L1000,520 L40,520 Z"

hook = f'''<div class="hk"><div class="hk-chart"><svg width="1080" height="600" viewBox="0 0 1080 600"><path d="{PATH}" fill="none" stroke="{RED}" stroke-width="10" stroke-linejoin="round" opacity=".35"/></svg></div>
<div class="hk-1">TECH JUST LOST</div><div class="hk-2">$1 TRILLION</div><div class="hk-3">IN ONE DAY 📉</div></div>'''

panel = f'''<div class="pn">
<div class="tick"><div class="tk" id="tk">{TICK}</div></div>
<div class="sc" id="s1"><div class="hd"><span class="live">● LIVE</span> TECH STOCKS</div>
  <svg class="chart" width="1080" height="560" viewBox="0 0 1080 560"><defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity=".45"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>
  <path id="area" d="{AREA}" fill="url(#ga)" opacity="0"/><path id="line" d="{PATH}" fill="none" stroke="{RED}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/></svg>
  <div class="ctr" id="ctr1">−$0B</div><div class="stamp" id="day">IN ONE DAY</div></div>
<div class="sc" id="s2"><div class="big" id="why">THE REASON? 🤔</div>
  <div class="fear" id="fear">😨 FEAR OF AI OVERSPENDING</div>
  <div class="barw"><div class="lim" id="lim"><span>TOO MUCH?</span></div><div class="bar" id="bar"><span>AI SPENDING 💸</span></div></div></div>
<div class="sc" id="s3"><div class="lbl">AI SPENDING</div><div class="big2" id="ctr3">$0B</div>
  <div class="tiles"><div class="tile" id="t1"><div class="ico">🏢</div>DATA CENTERS</div><div class="tile" id="t2"><div class="chip"><div class="core">AI</div></div>CHIPS</div></div></div>
<div class="sc" id="s4"><div class="hd2">OPENAI · FUNDING TARGET</div><div class="rep" id="rep">REPORTEDLY ✂️</div>
  <div class="cutfx" id="cutfx"><span id="tgt">🎯</span><span id="sci">✂️</span></div><div class="money"><div class="m30" id="m30">$30B<div class="strk" id="strk"></div></div><div class="arr" id="arr">→</div><div class="m20" id="m20">$20B</div></div>
  <div class="down" id="down">▼ $10B CUT</div><div class="src">via Financial Times</div></div>
<div class="sc" id="s5"><div class="q">IS THE AI BUBBLE…</div><div class="bub" id="bub"><span>AI</span></div>
  {"".join(f'<div class="pt" id="pt{i}"></div>' for i in range(14))}<div class="popt" id="popt">POP? 💥</div></div>
<div class="sc" id="s6"><div class="q">ABOUT TO POP?</div><div class="btns"><div class="btn yes" id="yes">YES 💥</div><div class="btn no" id="no">NO 🚀</div></div><div class="cm" id="cm">COMMENT 👇</div></div>
<div class="div"></div></div>'''

doc = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}}
.full{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}}
.hk{{position:absolute;inset:0;background:radial-gradient(90% 60% at 50% 45%,#2a0608 0%,{BG} 70%);display:flex;flex-direction:column;align-items:center;justify-content:center}}
.hk-chart{{position:absolute;left:0;top:600px}}
.hk-1{{font-size:78px;letter-spacing:.04em}} .hk-2{{font-size:150px;color:{RED};line-height:1.05;letter-spacing:-.02em}} .hk-3{{font-size:78px}}
.pw{{position:absolute;left:0;top:0;width:1080px;height:960px}}
.pn{{position:absolute;inset:0;background:linear-gradient(180deg,#0d1015 0%,{BG} 100%);overflow:hidden}}
.pn::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:90px 90px}}
.tick{{position:absolute;left:0;right:0;top:0;height:74px;background:{RED};overflow:hidden;display:flex;align-items:center}}
.tk{{white-space:nowrap;flex:0 0 auto;display:inline-block;font-size:36px;color:#fff;padding-left:40px;word-spacing:6px}}
.sc{{position:absolute;left:0;top:74px;width:1080px;height:780px}}
.hd{{position:absolute;left:50px;top:36px;font-size:44px;color:#e7e9ee}} .live{{color:{RED}}}
.chart{{position:absolute;left:0;top:120px}}
.ctr{{position:absolute;right:50px;top:30px;font-size:84px;color:{RED}}}
.stamp{{position:absolute;left:280px;top:470px;font-size:96px;color:{AMB};border:9px solid {AMB};border-radius:24px;padding:2px 34px;background:rgba(7,9,12,.85)}}
.big{{position:absolute;left:0;right:0;top:70px;text-align:center;font-size:110px}}
.fear{{position:absolute;left:0;right:0;top:240px;text-align:center;font-size:56px;color:{AMB}}}
.barw{{position:absolute;left:150px;right:150px;top:360px;height:400px}}
.bar{{position:absolute;left:180px;right:180px;bottom:0;height:380px;background:linear-gradient(0deg,{RED},#ff7a59);border-radius:22px 22px 0 0;transform-origin:bottom center;display:flex;align-items:flex-start;justify-content:center;padding-top:20px;font-size:40px}}
.lim{{position:absolute;left:-40px;right:-40px;top:120px;border-top:6px dashed #fff;font-size:36px;color:#fff;text-align:right}}
.lim span{{position:relative;top:-54px}}
.lbl{{position:absolute;left:0;right:0;top:60px;text-align:center;font-size:50px;color:#c9ccd6;letter-spacing:.08em}}
.big2{{position:absolute;left:0;right:0;top:120px;text-align:center;font-size:200px;color:{AMB}}}
.tiles{{position:absolute;left:90px;right:90px;top:430px;display:flex;gap:40px}}
.tile{{flex:1;height:300px;border-radius:36px;background:#141821;border:3px solid #2a3040;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;font-size:46px}}
.ico{{font-size:120px}}
.chip{{width:130px;height:130px;border-radius:20px;background:#1f2533;border:6px solid {AMB};position:relative}}
.chip .core{{position:absolute;inset:22px;border-radius:10px;background:{AMB};color:#000;font-size:44px;display:flex;align-items:center;justify-content:center}}
.hd2{{position:absolute;left:0;right:0;top:60px;text-align:center;font-size:52px;color:#e7e9ee}}
.rep{{position:absolute;left:0;right:0;top:150px;text-align:center;font-size:44px;color:#9aa0ad}}
.cutfx{{position:absolute;left:0;right:0;top:250px;text-align:center;font-size:200px;letter-spacing:40px}}
.money{{position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center;align-items:center;gap:40px}}
.m30{{position:relative;font-size:170px;color:#e7e9ee}} .m20{{font-size:170px;color:{RED}}} .arr{{font-size:120px;color:#9aa0ad}}
.strk{{position:absolute;left:-10px;right:-10px;top:52%;height:16px;background:{RED};border-radius:8px;transform-origin:left center}}
.down{{position:absolute;left:0;right:0;top:530px;text-align:center;font-size:66px;color:{RED}}}
.src{{position:absolute;left:0;right:0;top:640px;text-align:center;font-family:PM;font-size:30px;color:#6f7686}}
.q{{position:absolute;left:0;right:0;top:50px;text-align:center;font-size:76px}}
.bub{{position:absolute;left:340px;top:220px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle at 32% 28%,rgba(255,255,255,.9) 0 6%,rgba(255,176,32,.55) 7% 40%,rgba(255,59,59,.35) 70%,rgba(255,59,59,.15) 100%);border:6px solid rgba(255,255,255,.6);display:flex;align-items:center;justify-content:center;font-size:130px}}
.pt{{position:absolute;left:530px;top:410px;width:26px;height:26px;border-radius:50%;background:{AMB};opacity:0}}
.popt{{position:absolute;left:0;right:0;top:620px;text-align:center;font-size:96px;color:{AMB}}}
.btns{{position:absolute;left:80px;right:80px;top:250px;display:flex;gap:40px}}
.btn{{flex:1;text-align:center;font-size:96px;padding:60px 10px;border-radius:44px}}
.yes{{background:{RED}}} .no{{background:{GRN};color:#04140b}}
.cm{{position:absolute;left:0;right:0;top:600px;text-align:center;font-size:62px;color:{AMB}}}
.div{{position:absolute;left:0;right:0;bottom:0;height:8px;background:{RED}}}
.flash{{position:absolute;inset:0;background:{RED};opacity:0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{clip("panel", P0, P1, f'<div class="pw" id="pw">{panel}</div>', "full", 20)}
{clip("hook", 0, 0.5, f'<div class="full" id="hkz">{hook}<div class="flash" id="fl"></div></div>', "full", 50)}
{clip("tail", SPEECH_END, TOTAL, f'<div class="full" id="tlz">{hook}</div>', "full", 60)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#hkz",{{scale:1.10}},{{scale:1.0,duration:0.5,ease:"power2.out"}},0).to("#fl",{{opacity:0.55,duration:0.1}},0.38);
tl.fromTo("#tlz",{{opacity:0,scale:1.0}},{{opacity:1,duration:0.12,ease:"none"}},{SPEECH_END:.3f})
  .to("#tlz",{{scale:1.10,duration:{TOTAL - SPEECH_END - 0.02:.3f},ease:"power2.in"}},{SPEECH_END:.3f});
tl.fromTo("#pw",{{y:-960}},{{y:0,duration:0.25,ease:"power3.out"}},{P0:.3f});
tl.fromTo("#tk",{{x:0}},{{x:-2600,duration:{TOTAL:.3f},ease:"none"}},0);
const sc = {json.dumps(SC)};
tl.set(".sc",{{opacity:0}},0);
for (const [id,[s,e]] of Object.entries(sc)) {{
  tl.fromTo(`#${{id}}`,{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.2,ease:"power2.out"}},s)
    .to(`#${{id}}`,{{opacity:0,y:-20,duration:0.15,ease:"power2.in"}},e-0.15);
}}
// S1 crash chart draws, counter climbs to $1 trillion, stamp
const L = document.querySelector("#line").getTotalLength();
tl.set("#line",{{strokeDasharray:L,strokeDashoffset:L}},0)
  .to("#line",{{strokeDashoffset:0,duration:{T("TRILLION") + 0.3 - P0 - 0.2:.3f},ease:"power1.in"}},{P0 + 0.2:.3f})
  .to("#area",{{opacity:1,duration:0.4}},{T("TRILLION"):.3f});
const c1 = {{v:0}};
tl.to(c1,{{v:1000,duration:{E("TRILLION") - T("LOST"):.3f},ease:"power2.in",onUpdate:()=>{{document.querySelector("#ctr1").textContent = c1.v>=999.5 ? "−$1 TRILLION" : "−$"+Math.round(c1.v)+"B";}}}},{T("LOST"):.3f});
tl.fromTo("#day",{{scale:2.4,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-7,duration:0.2,ease:"power3.in"}},{T("DAY"):.3f});
// S2 reason -> fear -> the spending bar breaks the limit line
tl.from("#why",{{scale:0.6,duration:0.3,ease:"back.out(2)"}},{SC["s2"][0]:.3f})
  .from("#fear",{{opacity:0,y:30,duration:0.25}},{T("FEAR"):.3f})
  .fromTo("#bar",{{scaleY:0.05}},{{scaleY:0.55,duration:0.6,ease:"power2.out"}},{T("SPENDING"):.3f})
  .from("#lim",{{opacity:0,duration:0.2}},{T("SPENDING"):.3f})
  .to("#bar",{{scaleY:1.0,duration:0.35,ease:"back.out(2)"}},{T("MUCH"):.3f});
// S3 counter to $800B+, tiles on their words
const c3 = {{v:0}};
tl.to(c3,{{v:800,duration:{E("BILLION") - T("OVER"):.3f},ease:"power3.out",onUpdate:()=>{{document.querySelector("#ctr3").textContent = c3.v>=799.5 ? "$800B+" : "$"+Math.round(c3.v)+"B";}}}},{T("OVER"):.3f});
tl.from("#t1",{{y:60,opacity:0,scale:0.8,duration:0.3,ease:"back.out(2)"}},{T("DATA"):.3f})
  .from("#t2",{{y:60,opacity:0,scale:0.8,duration:0.3,ease:"back.out(2)"}},{T("CHIPS"):.3f});
// S4 OpenAI $30B -> $20B
tl.from("#rep",{{opacity:0,y:20,duration:0.25}},{T("REPORTEDLY"):.3f})
  .from("#tgt",{{scale:0,duration:0.3,ease:"back.out(2)"}},{T("REPORTEDLY"):.3f})
  .from("#sci",{{x:400,rotation:-40,opacity:0,duration:0.3,ease:"power3.out"}},{T("CUT") - 0.1:.3f})
  .to("#sci",{{x:-150,rotation:20,duration:0.25,ease:"power2.in"}},{T("CUT") + 0.25:.3f})
  .to("#tgt",{{scale:0.8,rotation:-10,duration:0.2}},{T("CUT") + 0.4:.3f})
  .to("#cutfx",{{opacity:0,y:-30,duration:0.2}},{T("30") - 0.25:.3f})
  .from("#m30",{{scale:0.4,opacity:0,duration:0.3,ease:"back.out(2)"}},{T("30") - 0.05:.3f})
  .set(["#arr","#m20","#down"],{{opacity:0}},0)
  .fromTo("#strk",{{scaleX:0}},{{scaleX:1,duration:0.25,ease:"power3.out"}},{T("20") - 0.1:.3f})
  .to("#arr",{{opacity:1,duration:0.15}},{T("20") - 0.05:.3f})
  .fromTo("#m20",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{T("20"):.3f})
  .fromTo("#down",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.25}},{E("DOLLARS", 4):.3f});
// S5 bubble inflates, wobbles, pops on "pop"
tl.fromTo("#bub",{{scale:0.35}},{{scale:1.15,duration:{T("POP") - T("IS"):.3f},ease:"power1.in"}},{T("IS"):.3f});
for (let k=0;k<8;k++) tl.to("#bub",{{x:(k%2?-1:1)*(4+k),duration:0.08}},{T("ABOUT"):.3f}+k*0.06);
tl.to("#bub",{{scale:1.7,opacity:0,duration:0.12,ease:"power2.out"}},{T("POP"):.3f});
for (let i=0;i<14;i++) {{ const a = i/14*Math.PI*2; tl.fromTo(`#pt${{i}}`,{{opacity:1,x:0,y:0}},{{opacity:0,x:Math.cos(a)*360,y:Math.sin(a)*300,duration:0.45,ease:"power3.out"}},{T("POP"):.3f}); }}
tl.set("#popt",{{opacity:0}},0).fromTo("#popt",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.2,ease:"back.out(3)"}},{T("POP") + 0.02:.3f});
// S6 poll
tl.from("#yes",{{x:-300,opacity:0,duration:0.25,ease:"power3.out"}},{T("YES"):.3f})
  .from("#no",{{x:300,opacity:0,duration:0.25,ease:"power3.out"}},{T("NO"):.3f})
  .from("#cm",{{scale:0,duration:0.25,ease:"back.out(2)"}},{T("COMMENTS") - 0.1:.3f});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>'''
open("hf/index.html", "w").write(doc)
json.dump({"split": [P0, round(TOTAL + 1.0, 3)], "scenes": SC, "speech_end": SPEECH_END, "total": TOTAL}, open("hf/events.json", "w"), indent=1)
print("ok", TOTAL)
