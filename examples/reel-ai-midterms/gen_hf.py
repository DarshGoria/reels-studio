"""AI midterms — classic split x2 + a full-screen SURPRISE: the speaker's own face gets a tracked 'deepfake scan' HUD
(glitch on the video via base-vf, verdict flips to STILL WON +7). 0.2 s ballot-box sting, poll end, loop to frame 0."""
import json, sys, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="{z}" style="z-index:{z}">{inner}</div>')
FZ = json.load(open("faces.json")); r = random.Random(26)
NAV, RED, BLU, WHT, YEL, GRN = "#0B1F4B", "#E63946", "#3B82F6", "#F8FAFC", "#FFD34D", "#22C55E"
PANEL_H = 760; SLIDE = PANEL_H + 20 - FZ["top"]
S1 = (T("CAMPAIGNS") - 0.1, T("BUT") - 0.1); FS = (S1[1], T("SHOULD") - 0.1); S2 = (FS[1], SPEECH_END)
S = {"ads": (S1[0], T("AI", 4) - 0.1), "chat": (T("AI", 4) - 0.1, T("ONE") - 0.2), "ballot": (T("ONE") - 0.2, S1[1]), "poll": S2}
CUTS = [S["chat"][0], S["ballot"][0], FS[0], S2[0]]
HOOK_TOP = FZ["free_above"][0] + 10
# face track (video is hflipped in compose → mirror x)
BX = [(b[0], 1080 - b[1] - b[3], b[2], b[3], b[4]) for b in FZ["boxes"] if FS[0] - 0.6 <= b[0] <= FS[1] + 0.6]
thumbs = "".join(f'<div class="th" id="th{i}"><div class="tv" style="background:linear-gradient(135deg,{r.choice([RED,BLU,"#7c3aed","#0ea5e9"])},#111)"><i>▶</i></div><b>🤖 AI</b></div>' for i in range(12))
voters = "".join(f'<i class="vt" id="v{i}">{e}</i>' for i, e in enumerate(["🧑", "👩", "👨‍🦳", "🧑‍🦱", "👩‍🦰"]))
pnl = f'''<div class="pnl" id="pnl"><div class="stripes"></div>
 <div class="sc" id="ads"><div class="hd">AI-MADE CAMPAIGN ADS</div><div class="cnt">$<span id="n80">0</span>M</div><div class="grid">{thumbs}</div><div class="stamp" id="nl">2 OUT OF 3 NEVER SAID “AI” 🤫</div></div>
 <div class="sc" id="chat"><div class="ph"><div class="pt">🤖 Campaign AI agent <em>● online</em></div>
   <div class="bb bot" id="b1">Hi! I’m with the campaign 👋 What issue matters most to you?</div><div class="bb me" id="b2">Honestly? Prices.</div>
   <div class="bb bot" id="b3">Totally fair. Here’s what we’d do about it…</div><div class="typ" id="typ"><i></i><i></i><i></i></div></div>
   <div class="side2"><div class="big2">FULL<br>CONVERSATIONS</div><div class="sm2">with thousands of voters at once</div></div></div>
 <div class="sc" id="ballot"><div class="vts">{voters}</div><div class="one" id="one">1 IN 5 VOTERS</div>
   <div class="bal" id="bal"><div class="bt">OFFICIAL BALLOT</div><div class="op"><i></i>Candidate A</div><div class="op"><i></i>Candidate B</div><div class="op"><i></i>Measure 12</div></div>
   <div class="ask" id="ask">🤖 “Which one should I pick?”</div></div>
 <div class="sc" id="poll"><div class="pq">SHOULD AI BE <b>BANNED</b><br>FROM ELECTIONS?</div>
   <div class="bars"><div class="bar y"><div class="fill" id="fy"></div><span>✅ YES</span></div><div class="bar n"><div class="fill" id="fn"></div><span>❌ NO</span></div></div>
   <div class="cm" id="cm">💬 COMMENT YES OR NO 👇</div></div>
</div>'''
hook = f'<div class="hz" id="hz"><div class="hk0">🇺🇸 US MIDTERMS 2026</div><div class="hk1">AMERICA’S FIRST<br><b>AI ELECTION</b> 🗳️</div><div class="hk2" id="wd">…AND IT GOT WEIRD 👀</div></div>'
tail = hook.replace('id="hz"', 'id="tz"').replace('id="wd"', 'id="wd2"')
side = '<i class="stk" id="k_a" style="left:40px;top:1300px">🤖</i><i class="stk" id="k_b" style="left:910px;top:1320px">🗳️</i>'
hud = f'''<div class="hud" id="hud"><div class="jit" id="jit"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i><div class="scan" id="scan"></div>
  <div class="tag" id="tag">SCANNING FACE… 🔍</div><div class="tag bad" id="bad">⚠️ DEEPFAKE</div><div class="tag ok" id="ok">✅ STILL WON</div></div></div>
 <div class="tw" id="tw"><span>BUT HERE’S THE TWIST</span></div><div class="won" id="won">STILL WON BY <b>+7</b> 🏆</div><div class="scanlines" id="sl"></div>'''
css = f'''@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}} @font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}} @font-face{{font-family:MO;src:url(assets/fonts/DejaVuSansMono.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}} .full{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.hz{{position:absolute;left:30px;right:30px;top:{HOOK_TOP}px;text-align:center}}
.hk0{{display:inline-block;font-size:42px;background:{NAV};border:4px solid {RED};padding:8px 28px;border-radius:99px;margin-bottom:18px}}
.hk1{{font-size:86px;line-height:1.05;background:{WHT};color:{NAV};padding:20px 30px;border-radius:30px;box-shadow:0 18px 40px rgba(0,0,0,.3)}} .hk1 b{{color:{RED}}}
.hk2{{display:inline-block;margin-top:18px;font-size:54px;background:{YEL};color:#111;padding:8px 26px;border-radius:18px;transform:rotate(-2deg)}}
.stk{{position:absolute;font-size:120px;font-style:normal;filter:drop-shadow(0 10px 16px rgba(0,0,0,.35))}}
.pnl{{position:absolute;left:0;top:0;width:1080px;height:{PANEL_H}px;overflow:hidden;background:{NAV};border-bottom:10px solid {RED}}}
.stripes{{position:absolute;inset:0;background:repeating-linear-gradient(135deg,rgba(255,255,255,.035) 0 40px,transparent 40px 80px)}}
.sc{{position:absolute;inset:0;opacity:0}} .hd{{position:absolute;left:0;right:0;top:40px;text-align:center;font-size:46px;letter-spacing:.06em;color:#c7d2fe}}
.cnt{{position:absolute;left:0;right:0;top:95px;text-align:center;font-size:150px;line-height:1;color:{YEL}}}
.grid{{position:absolute;left:60px;right:60px;top:290px;display:grid;grid-template-columns:repeat(6,1fr);gap:14px}}
.th{{background:#0f172a;border:3px solid #334155;border-radius:16px;padding:8px;text-align:center}} .th b{{display:block;font-size:22px;margin-top:4px;color:{YEL}}}
.tv{{height:100px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:40px}} .tv i{{font-style:normal;opacity:.8}}
.stamp{{position:absolute;left:0;right:0;top:600px;margin:auto;width:max-content;font-size:54px;color:{RED};border:8px solid {RED};padding:2px 26px;border-radius:16px;transform:rotate(-4deg);background:rgba(11,31,75,.92)}}
.ph{{position:absolute;left:60px;top:40px;width:560px;height:680px;background:#f1f5f9;border-radius:46px;border:10px solid #111;padding:24px;color:#111;overflow:hidden}}
.pt{{font-size:30px;padding-bottom:14px;border-bottom:2px solid #cbd5e1;margin-bottom:20px}} .pt em{{font-style:normal;color:{GRN};font-family:PM;font-size:24px}}
.bb{{font-family:PM;font-size:31px;line-height:1.25;padding:16px 20px;border-radius:24px;margin:12px 0;max-width:86%}} .bot{{background:#e2e8f0}} .me{{background:{BLU};color:#fff;margin-left:auto}}
.typ{{display:flex;gap:8px;padding:18px 22px;background:#e2e8f0;border-radius:24px;width:max-content}} .typ i{{width:14px;height:14px;border-radius:50%;background:#64748b}}
.side2{{position:absolute;left:650px;right:20px;top:200px}} .big2{{font-size:50px;line-height:1.05;color:{YEL}}} .sm2{{font-family:PM;font-size:32px;color:#c7d2fe;margin-top:16px}}
.vts{{position:absolute;left:0;right:0;top:40px;display:flex;justify-content:center;gap:40px;font-size:120px}} .vt{{font-style:normal;opacity:.35}}
.one{{position:absolute;left:0;right:0;top:200px;text-align:center;font-size:76px;color:{YEL}}}
.bal{{position:absolute;left:120px;top:320px;width:470px;height:400px;background:#fff;color:#111;border-radius:10px;padding:26px;transform:rotate(-3deg);box-shadow:0 30px 60px rgba(0,0,0,.5)}}
.bt{{font-size:34px;letter-spacing:.1em;border-bottom:4px solid #111;padding-bottom:10px;margin-bottom:16px;text-align:center}} .op{{font-family:PM;font-size:36px;display:flex;align-items:center;gap:20px;margin:22px 0}}
.op i{{width:46px;height:46px;border:4px solid #111;border-radius:8px}} .ask{{position:absolute;left:620px;right:30px;top:420px;font-size:44px;background:{BLU};padding:20px 24px;border-radius:30px 30px 30px 6px}}
.pq{{position:absolute;left:0;right:0;top:50px;text-align:center;font-size:76px;line-height:1.1}} .pq b{{color:{RED}}}
.bars{{position:absolute;left:100px;right:100px;top:300px}} .bar{{position:relative;height:120px;border-radius:24px;background:rgba(255,255,255,.1);margin:24px 0;overflow:hidden}}
.bar .fill{{position:absolute;left:0;top:0;bottom:0;width:100%;transform-origin:left}} .y .fill{{background:{GRN}}} .n .fill{{background:{RED}}}
.bar span{{position:absolute;left:30px;top:30px;font-size:54px}} .cm{{position:absolute;left:0;right:0;top:620px;margin:auto;width:max-content;font-size:52px;background:{WHT};color:{NAV};padding:12px 34px;border-radius:24px}}
.hud{{position:absolute;left:0;top:0;width:400px;height:400px;border:3px solid rgba(255,255,255,.35)}}
.c{{position:absolute;width:70px;height:70px;border:10px solid {YEL}}} .tl{{left:-8px;top:-8px;border-right:none;border-bottom:none}} .tr{{right:-8px;top:-8px;border-left:none;border-bottom:none}}
.bl{{left:-8px;bottom:-8px;border-right:none;border-top:none}} .br{{right:-8px;bottom:-8px;border-left:none;border-top:none}}
.jit{{position:absolute;inset:0}} .scan{{position:absolute;left:0;right:0;top:0;height:8px;background:{YEL};box-shadow:0 0 30px {YEL}}}
.tag{{position:absolute;left:0;top:-90px;font-family:MO;font-size:40px;background:{YEL};color:#111;padding:6px 18px;white-space:nowrap}} .bad{{background:{RED};color:#fff;opacity:0}} .ok{{background:{GRN};color:#fff;opacity:0}}
.tw{{position:absolute;left:0;right:0;top:220px;text-align:center}} .tw span{{display:inline-block;font-size:76px;background:{RED};padding:10px 34px;border-radius:20px;transform:rotate(-3deg)}}
.won{{position:absolute;left:0;right:0;top:280px;margin:auto;width:max-content;font-size:96px;color:{GRN};border:12px solid {GRN};padding:4px 36px;border-radius:24px;transform:rotate(-4deg);background:rgba(0,0,0,.55)}} .won b{{color:#fff}}
.scanlines{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 3px,transparent 3px 7px);opacity:0}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.leak{{position:absolute;left:-400px;top:-300px;width:700px;height:2600px;background:linear-gradient(90deg,transparent,rgba(230,57,70,.5),rgba(59,130,246,.4),transparent);filter:blur(34px);transform:rotate(16deg)}}
.sh{{position:absolute;left:0;right:0;height:960px;background:{NAV}}} .sh.t{{top:0;border-bottom:6px solid {RED}}} .sh.b{{top:960px;border-top:6px solid {RED}}}
.shl{{position:absolute;left:0;right:0;top:860px;text-align:center;font-size:200px;line-height:1}}'''
def sc(k): s, e = S[k]; return f'tl.set("#{k}",{{opacity:1}},{s:.3f}).set("#{k}",{{opacity:0}},{e:.3f});'
hudk = "".join(f'tl.to("#hud",{{x:{x - 40},y:{y - 60},width:{w + 80},height:{h + 120},duration:0.5,ease:"sine.inOut"}},{t - 0.25:.3f});' for t, x, y, w, h in BX)
x0, y0, w0, h0 = BX[0][1:]
js = "\n".join(sc(k) for k in S) + f'''
tl.fromTo("#shl",{{scale:1.8,rotation:-30}},{{scale:0.3,rotation:30,opacity:0,duration:0.16,ease:"power2.in"}},0)
  .to("#sht",{{y:-980,duration:0.2,ease:"power3.in"}},0.08).to("#shb",{{y:980,duration:0.2,ease:"power3.in"}},0.08).set("#f0",{{opacity:0.7}},0.2).to("#f0",{{opacity:0,duration:0.1}},0.21);
tl.from("#wd",{{scale:0,rotation:-20,duration:0.3,ease:"back.out(2.5)"}},{T("WEIRD") - 0.15:.3f});
tl.to("#hz",{{scale:1.03,duration:{S1[0]-0.4:.3f},ease:"sine.inOut"}},0).to("#hz",{{opacity:0,y:-30,duration:0.2}},{S1[0]-0.15:.3f});
tl.from(["#k_a","#k_b"],{{scale:0,rotation:-30,duration:0.3,stagger:0.25,ease:"back.out(2.5)"}},{T("AI"):.3f}).to(["#k_a","#k_b"],{{scale:0,duration:0.15}},{S1[0]-0.15:.3f});
tl.set("#wd2",{{opacity:1}},0).fromTo("#tz",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:{TOTAL-SPEECH_END-0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});
tl.fromTo("#pnl",{{y:-{PANEL_H+20}}},{{y:0,duration:0.25,ease:"power3.out"}},{S1[0]:.3f}).to("#pnl",{{y:-{PANEL_H+20},duration:0.22,ease:"power3.in"}},{S1[1]-0.22:.3f})
  .to("#pnl",{{y:0,duration:0.25,ease:"power3.out"}},{S2[0]:.3f}).to("#pnl",{{y:-{PANEL_H+20},duration:0.22,ease:"power3.in"}},{S2[1]-0.22:.3f});
const N=(id,to,d,at)=>{{const o={{v:0}};tl.to(o,{{v:to,duration:d,ease:"power2.out",onUpdate:()=>{{document.getElementById(id).textContent=Math.round(o.v)}}}},at);}};
N("n80",80,0.9,{T("80") - 0.2:.3f}); tl.from(".th",{{scale:0,duration:0.22,stagger:0.07,ease:"back.out(2)"}},{T("AI", 2) - 0.2:.3f});
tl.fromTo("#nl",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{T("DIDN'T"):.3f}).to(".th",{{opacity:0.45,duration:0.2,stagger:{{each:0.02,from:"random"}}}},{T("DIDN'T") + 0.1:.3f});
tl.from(".ph",{{y:800,duration:0.4,ease:"power3.out"}},{S["chat"][0]:.3f}).from("#b1",{{scale:0,transformOrigin:"left bottom",duration:0.25}},{T("TEXTING") - 0.1:.3f})
  .from("#b2",{{scale:0,transformOrigin:"right bottom",duration:0.25}},{T("HAVING"):.3f}).from("#b3",{{scale:0,transformOrigin:"left bottom",duration:0.25}},{T("CONVERSATIONS") + 0.1:.3f})
  .from(".side2",{{x:500,opacity:0,duration:0.3}},{T("FULL") - 0.1:.3f}).to("#typ i",{{y:-10,duration:0.18,yoyo:true,repeat:9,stagger:0.08}},{T("ON", 2) - 0.2:.3f});
tl.from(".vt",{{y:150,duration:0.3,stagger:0.08,ease:"back.out(2)"}},{S["ballot"][0] + 0.05:.3f}).to("#v2",{{opacity:1,scale:1.3,duration:0.25}},{T("FIVE"):.3f})
  .from("#one",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{T("ONE"):.3f}).from("#bal",{{y:500,rotation:12,duration:0.4,ease:"power3.out"}},{T("PLANNED") - 0.2:.3f})
  .from("#ask",{{scale:0,transformOrigin:"left bottom",duration:0.3,ease:"back.out(2)"}},{T("ASK") - 0.05:.3f});
// ---- SURPRISE: full-screen deepfake scan
tl.set("#hud",{{x:{x0 - 40},y:{y0 - 60},width:{w0 + 80},height:{h0 + 120}}},0);
{hudk}
tl.fromTo("#tw",{{scale:2.5,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{T("TWIST") - 0.2:.3f}).to("#tw",{{opacity:0,duration:0.2}},{T("CANDIDATE", 2) - 0.1:.3f});
tl.from("#hud",{{opacity:0,scale:1.4,duration:0.3}},{T("CANDIDATE", 2) - 0.1:.3f}).fromTo("#scan",{{y:0}},{{y:{h0 + 110},duration:0.7,repeat:4,yoyo:true,ease:"sine.inOut"}},{T("CANDIDATE", 2):.3f});
tl.set("#tag",{{opacity:0}},{T("DEEP") - 0.05:.3f}).set("#bad",{{opacity:1}},{T("DEEP") - 0.05:.3f}).set(".c",{{borderColor:"{RED}"}},{T("DEEP") - 0.05:.3f}).set("#scan",{{background:"{RED}"}},{T("DEEP") - 0.05:.3f})
  .set("#sl",{{opacity:1}},{T("DEEP") - 0.05:.3f}).set("#sl",{{opacity:0}},{T("VIDEO") + 0.7:.3f});
[0,0.08,0.16,0.24,0.32,0.40].forEach((d,i)=>tl.set("#jit",{{x:(i==5?0:(i%2?18:-18))}},{T("DEEP"):.3f}+d));
tl.set("#bad",{{opacity:0}},{T("STILL") - 0.05:.3f}).set("#ok",{{opacity:1}},{T("STILL") - 0.05:.3f}).set(".c",{{borderColor:"{GRN}"}},{T("STILL") - 0.05:.3f}).set("#scan",{{opacity:0}},{T("STILL") - 0.05:.3f})
  .fromTo("#won",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{T("WON") - 0.05:.3f}).to("#won",{{scale:1.08,duration:0.12,yoyo:true,repeat:3}},{T("7"):.3f});
tl.from(".pq",{{y:-200,opacity:0,duration:0.3}},{S2[0] + 0.1:.3f}).fromTo("#fy",{{scaleX:0}},{{scaleX:0.62,duration:0.6}},{T("BANNED"):.3f}).fromTo("#fn",{{scaleX:0}},{{scaleX:0.38,duration:0.6}},{T("BANNED") + 0.1:.3f})
  .to("#fy",{{scaleX:0.5,duration:0.4,yoyo:true,repeat:1}},{T("COMMENT"):.3f}).from("#cm",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{T("COMMENT") - 0.05:.3f}).to("#cm",{{scale:1.08,duration:0.2,yoyo:true,repeat:3}},{T("YES"):.3f});
{"".join(f'tl.set("#fl{i}",{{opacity:0.5}},{t:.3f}).to("#fl{i}",{{opacity:0,duration:0.15}},{t + 0.02:.3f}).fromTo("#lk{i}",{{x:-300}},{{x:1500,duration:0.5,ease:"power1.inOut"}},{t - 0.12:.3f});' for i, t in enumerate(CUTS))}'''
body = (clip("panel", S1[0], SPEECH_END, pnl, 5) + clip("fs", FS[0], FS[1], hud, 40) + clip("hook", 0, S1[0] + 0.05, hook + side, 30) + clip("tail", SPEECH_END, TOTAL, tail, 30) +
        clip("intro", 0, 0.32, '<div class="sh t" id="sht"></div><div class="sh b" id="shb"></div><div class="shl" id="shl">🗳️</div><div class="flash" id="f0"></div>', 80) +
        "".join(clip(f"tr{i}", t - 0.12, t + 0.4, f'<div class="flash" id="fl{i}"></div><div class="leak" id="lk{i}"></div>', 60) for i, t in enumerate(CUTS)))
doc = (f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body>'
       f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">{body}</div>'
       f'<script>const tl = gsap.timeline({{paused:true}});\n{js}\nwindow.__timelines["main"] = tl; tl.seek(0);</script></body></html>')
open("hf/index.html", "w").write(doc)
json.dump({"s1": S1, "fs": FS, "s2": S2, "scenes": S, "cuts": CUTS, "slide": SLIDE, "glitch": [T("DEEP") - 0.05, T("VIDEO") + 0.7],
           "speech_end": SPEECH_END, "total": TOTAL}, open("events.json", "w"), indent=1)
print("ok", S1, FS, S2, "slide", SLIDE)
