"""NN3 'India's AI paradox' — cinematic depth + dense assets + surprises
(slot-machine 20%->3% roll, money rain behind him, PLOT TWIST freeze, GPU gauge, live comment poll)."""
import json, sys, os, shutil, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')
rnd = random.Random(11)
SAF, GRN, WHT, YEL, RED, CYN, NAVY = "#FF9933", "#22C55E", "#FFF6EA", "#FFD34D", "#FF3D3D", "#3BE8FF", "#1E2A78"
HEAD = '''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script><style>
@font-face{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}
@font-face{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}
#root{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}
.full{position:absolute;left:0;top:0;width:1080px;height:1920px}
'''
def page(css, body, js):
    return (HEAD + css + f'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" '
            f'data-width="1080" data-height="1920">{body}</div><script>const tl = gsap.timeline({{paused:true}});\n{js}\n'
            'window.__timelines["main"] = tl; tl.seek(0);</script></body></html>')

TW = T("BUT", 2)                 # "But a new report..." = plot twist
B = {"pct": (0.0, T("CENTERS") + 0.35), "bill": (T("$300") - 0.15, TW - 0.05),
     "chip": (T("ABOUT") - 0.1, T("REAL") - 0.1), "serv": (T("REAL") - 0.05, T("SHOULD") - 0.05),
     "tail": (SPEECH_END, TOTAL)}

# ---------------- BACK (behind the person; full-length matte)
bokeh = "".join(f'<div class="bk" style="left:{rnd.randint(0,1040)}px;top:{rnd.randint(80,1500)}px;width:{(d:=rnd.randint(14,56))}px;height:{d}px;'
                f'background:{rnd.choice([SAF,GRN,WHT,SAF,GRN])};opacity:{rnd.uniform(.15,.38):.2f}"></div>' for _ in range(36))
cols = "".join(f'<div class="bc" style="left:{x}px">' + "<br>".join(rnd.choice("01") for _ in range(44)) + '</div>' for x in range(30, 1080, 74))
cash = "".join(f'<div class="cash" style="left:{rnd.randint(-20,1000)}px;font-size:{rnd.randint(70,120)}px">{rnd.choice(["💵","💵","💰","💸"])}</div>' for _ in range(26))
CASH_Y = [rnd.randint(-900, -150) for _ in range(26)]; CASH_R = [rnd.randint(-40, 40) for _ in range(26)]
roll = "".join(f"<div>{d}</div>" for d in "2198765430")   # tens digit rolls 2 -> 0 (blank), ones 0 -> 3
back_css = f'''.dw{{position:absolute;left:0;right:0;text-align:center;line-height:.86;letter-spacing:-.04em;text-shadow:0 10px 50px rgba(0,0,0,.35)}}
.bk{{position:absolute;border-radius:50%;filter:blur(6px)}}
.bc{{position:absolute;top:-200px;font-family:PM;font-size:26px;line-height:34px;color:{SAF};opacity:.12;text-align:center}}
.slot{{position:absolute;left:0;right:0;top:360px;display:flex;justify-content:center;font-size:400px;line-height:400px;letter-spacing:-.04em;text-shadow:0 10px 50px rgba(0,0,0,.35)}}
.win{{height:400px;overflow:hidden}} .reel{{display:flex;flex-direction:column}}
.cash{{position:absolute;top:0;line-height:1}}
#bill .dw{{top:420px;font-size:330px;color:{GRN}}}
#chipb .dw{{top:400px;font-size:380px;color:{RED}}}
#serv .dw{{top:470px;font-size:210px;color:{SAF}}}
#tail .dw{{top:250px;font-size:400px;color:{SAF}}}
.halo{{position:absolute;left:90px;top:200px;width:900px;height:900px;border-radius:50%;
 background:conic-gradient({SAF},{WHT},{GRN},{SAF});filter:blur(50px);opacity:.6}}
.chak{{position:absolute;left:340px;top:330px;width:400px;height:400px}}'''
spokes = "".join(f'<line x1="200" y1="200" x2="{200+180*__import__("math").cos(i*3.14159/12):.1f}" y2="{200+180*__import__("math").sin(i*3.14159/12):.1f}"/>' for i in range(24))
chakra = f'<svg class="chak" id="chk" viewBox="0 0 400 400"><g stroke="{NAVY}" stroke-width="6" fill="none" opacity=".9"><circle cx="200" cy="200" r="185" stroke-width="14"/>{spokes}<circle cx="200" cy="200" r="22" fill="{NAVY}"/></g></svg>'
back_body = (clip("bokeh", 0, TOTAL, f'<div id="bkw">{bokeh}</div>', 1) + clip("bin", 0, TOTAL, f'<div id="bnc">{cols}</div>', 2) +
             clip("pct", *B["pct"], f'<div class="slot" id="sl" style="color:{SAF}"><div class="win" id="w1"><div class="reel" id="r1">{roll}</div></div>'
                  f'<div class="win"><div class="reel" id="r2"><div>0</div><div>1</div><div>2</div><div>3</div></div></div><div>%</div></div>', 10) +
             clip("cashb", B["bill"][0], B["bill"][1] + 0.6, f'<div id="cw">{cash}</div>', 4) +
             clip("bill", *B["bill"], '<div class="dw" id="bw">$300B</div>', 10) +
             clip("chipb", *B["chip"], '<div class="dw" id="cpw">20%</div>', 10) +
             clip("serv", *B["serv"], '<div class="dw" id="sv">SERVICES</div>', 10) +
             clip("halob", T("SHOULD") - 0.1, SPEECH_END, '<div class="halo" id="hl"></div>' + chakra, 6) +
             clip("tail", *B["tail"], f'<div class="slot" style="color:{SAF}">20%</div>', 60))
back_js = f'''tl.to("#bkw .bk",{{y:"-=160",x:"+=30",duration:{TOTAL:.3f},ease:"none"}},0);
tl.fromTo("#bnc",{{y:0}},{{y:420,duration:{TOTAL:.3f},ease:"none"}},0);
tl.set("#r1",{{y:0}},0).set("#r2",{{y:0}},0);
tl.fromTo("#sl",{{scale:1}},{{scale:1.06,duration:{T("3%") - 0.5:.3f},ease:"sine.inOut"}},0);
tl.to("#r1",{{y:-400*9,duration:0.7,ease:"power3.inOut"}},{T("3%") - 0.45:.3f}).to("#r2",{{y:-400*3,duration:0.7,ease:"power3.inOut"}},{T("3%") - 0.45:.3f})
  .to("#w1",{{width:0,opacity:0,duration:0.25,ease:"power2.in"}},{T("3%") + 0.25:.3f}).to("#sl",{{color:"{GRN}",duration:0.2}},{T("3%") + 0.1:.3f}).to("#sl",{{opacity:0,y:-40,duration:0.2}},{B["pct"][1] - 0.2:.3f});
const CY={CASH_Y},CR={CASH_R};
tl.fromTo("#cw .cash",{{y:(i)=>CY[i],rotation:0}},{{y:(i)=>2200+CY[i],rotation:(i)=>CR[i]*6,duration:2.6,ease:"none",stagger:0.06}},{B["bill"][0]:.3f});
tl.from("#bw",{{scale:0.4,opacity:0,duration:0.35,ease:"back.out(2)"}},{B["bill"][0]:.3f}).to("#bw",{{scale:1.07,duration:2,ease:"sine.inOut"}},{B["bill"][0] + 0.35:.3f})
  .to("#bw",{{opacity:0,duration:0.15}},{B["bill"][1] - 0.15:.3f});
tl.from("#cpw",{{y:250,opacity:0,duration:0.3,ease:"power3.out"}},{T("20%", 2) - 0.25:.3f}).to("#cpw",{{opacity:0,duration:0.15}},{B["chip"][1] - 0.15:.3f});
tl.from("#sv",{{x:-1200,duration:0.35,ease:"power4.out"}},{B["serv"][0]:.3f}).to("#sv",{{x:1200,duration:0.25,ease:"power3.in"}},{B["serv"][1] - 0.25:.3f});
tl.from("#hl",{{scale:0.3,opacity:0,duration:0.5,ease:"power3.out"}},{T("SHOULD") - 0.1:.3f}).to("#hl",{{rotation:360,duration:{SPEECH_END - T("SHOULD"):.3f},ease:"none"}},{T("SHOULD") - 0.1:.3f})
  .from("#chk",{{scale:0,opacity:0,duration:0.5,ease:"back.out(1.8)"}},{T("SHOULD"):.3f}).to("#chk",{{rotation:720,duration:{SPEECH_END - T("SHOULD"):.3f},ease:"none"}},{T("SHOULD"):.3f});
tl.fromTo("#tail .slot",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:{TOTAL - SPEECH_END - 0.03:.3f}}},{SPEECH_END:.3f});'''

# ---------------- FRONT (top band 200-580, side edges, bottom corners; never the face)
F = {"lab": (T("20%") - 0.1, T("3%") - 0.5), "cmp": (T("3%") - 0.3, T("NOW") - 0.1), "fix": (T("FIX") - 0.2, TW - 0.05),
     "twist": (TW - 0.05, T("REPORT") - 0.1), "news": (T("REPORT") - 0.1, T("AI") - 0.1), "gpu": (T("AI") - 0.1, T("REAL") - 0.1),
     "edge": (T("REAL") - 0.05, T("SHOULD") - 0.05), "poll": (T("SHOULD") - 0.05, SPEECH_END)}
def stk(id_, txt, x, y, sz=120):
    return f'<div class="st" id="{id_}" style="left:{x}px;top:{y}px;font-size:{sz}px">{txt}</div>'
conf = "".join(f'<i class="cf" style="left:540px;top:400px;background:{rnd.choice([SAF,GRN,WHT,YEL])}"></i>' for _ in range(40))
CX, CYF, CRF = [rnd.randint(-520, 520) for _ in range(40)], [rnd.randint(-250, 1000) for _ in range(40)], [rnd.randint(-720, 720) for _ in range(40)]
front_css = f'''.st{{position:absolute;line-height:1;filter:drop-shadow(0 12px 18px rgba(0,0,0,.45))}}
.pill{{position:absolute;left:0;right:0;text-align:center}}
.pill span{{display:inline-block;font-size:44px;background:rgba(10,10,12,.8);border:3px solid {SAF};padding:10px 30px;border-radius:99px}}
.card{{position:absolute;left:60px;right:60px;background:rgba(10,10,12,.84);border-radius:30px;padding:24px 32px;border:3px solid rgba(255,255,255,.2)}}
.row{{display:flex;align-items:center;gap:18px;margin:10px 0;font-size:38px}} .row .l{{width:330px}}
.tk{{flex:1;height:44px;background:rgba(255,255,255,.1);border-radius:22px;overflow:hidden}}
.fl{{height:100%;border-radius:22px;transform-origin:left center}} .v{{width:96px;text-align:right;font-size:40px}}
.twist{{position:absolute;left:0;right:0;top:300px;text-align:center}}
.twist span{{display:inline-block;font-size:120px;color:{RED};border:12px solid {RED};padding:0 36px;border-radius:24px;letter-spacing:.04em;background:rgba(0,0,0,.35)}}
.news{{position:absolute;left:150px;right:150px;top:230px;background:#f3ecdd;color:#141414;border-radius:8px;padding:22px 30px;box-shadow:0 30px 60px rgba(0,0,0,.6);transform-origin:50% 0%}}
.news .mast{{font-family:PB;font-size:30px;letter-spacing:.3em;border-bottom:4px double #141414;padding-bottom:6px;text-align:center}}
.news .hl{{font-family:PB;font-size:52px;line-height:1.05;margin-top:12px}} .news .sub{{font-family:PM;font-size:28px;color:#555;margin-top:6px}}
.gpu{{position:absolute;left:60px;right:60px;top:220px;display:flex;align-items:center;gap:30px;background:rgba(10,10,12,.84);border-radius:30px;padding:24px 32px;border:3px solid rgba(255,255,255,.2)}}
.gauge{{width:260px;height:150px;position:relative}}
.needle{{position:absolute;left:126px;top:20px;width:8px;height:118px;background:{WHT};border-radius:4px;transform-origin:50% 100%}}
.gt{{font-size:40px;line-height:1.15}} .gt b{{color:{RED};font-size:64px}}
.poll{{position:absolute;left:50px;right:50px;top:215px;background:rgba(10,10,12,.86);border-radius:32px;padding:26px 30px;border:3px solid {SAF}}}
.pq{{font-size:46px;text-align:center;margin-bottom:14px}}
.opt{{position:relative;height:96px;margin:14px 0;border-radius:24px;background:rgba(255,255,255,.08);overflow:hidden;display:flex;align-items:center;padding:0 26px;font-size:40px}}
.opt .bar{{position:absolute;left:0;top:0;bottom:0;transform-origin:left center}} .opt span{{position:relative}} .opt b{{position:relative;margin-left:auto;font-size:44px}}
.cmt{{position:absolute;left:0;right:0;top:1395px;text-align:center}}
.cmt span{{display:inline-block;font-size:50px;background:{WHT};color:#111;padding:12px 34px;border-radius:24px}}
.cf{{position:absolute;width:18px;height:30px;border-radius:4px}}
.leak{{position:absolute;left:-300px;top:-200px;width:700px;height:2400px;background:linear-gradient(90deg,transparent,rgba(255,153,51,.55),rgba(34,197,94,.3),transparent);filter:blur(30px);transform:rotate(14deg)}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}'''
gauge = (f'<div class="gauge"><svg width="260" height="150" viewBox="0 0 260 150"><path d="M20 140 A110 110 0 0 1 240 140" stroke="rgba(255,255,255,.15)" stroke-width="26" fill="none"/>'
         f'<path id="garc" d="M20 140 A110 110 0 0 1 240 140" stroke="{RED}" stroke-width="26" fill="none" stroke-dasharray="346" stroke-dashoffset="346"/></svg><div class="needle" id="nd"></div></div>')
leaks = [T("NOW") - 0.15, TW - 0.1, T("AI") - 0.15, T("REAL") - 0.1, T("SHOULD") - 0.15]
front_body = (
    clip("lab", *F["lab"], '<div class="pill" style="top:230px" id="lb"><span>🇮🇳 INDIA\'S AI PARADOX</span></div>' + stk("s1", "📱", 50, 1380) + stk("s2", "🌍", 900, 1390), 20) +
    clip("cmp", *F["cmp"], f'<div class="card" id="cm" style="top:215px"><div class="row"><span class="l">📊 World\'s data</span><div class="tk"><div class="fl" id="b1" style="width:100%;background:{SAF}"></div></div><span class="v">20%</span></div>'
         f'<div class="row"><span class="l">🏢 Data centres</span><div class="tk"><div class="fl" id="b2" style="width:15%;background:{GRN}"></div></div><span class="v">3%</span></div></div>' + stk("s3", "🤯", 40, 620, 110) + stk("s4", "🏚️", 910, 620, 110), 20) +
    clip("fix", *F["fix"], '<div class="pill" style="top:230px" id="fx"><span>🏗️ ~$300B promised to fix it</span></div>' + stk("s5", "🏗️", 40, 1380) + stk("s6", "⚡", 910, 1380) + stk("s7", "🏭", 900, 600, 110), 20) +
    clip("twist", *F["twist"], '<div class="flash" id="fl"></div><div class="twist" id="tw"><span>PLOT TWIST</span></div>', 40) +
    clip("news", *F["news"], '<div class="news" id="nw"><div class="mast">THE AI DAILY</div><div class="hl">India\'s AI chips sitting mostly idle</div><div class="sub">New report · compute utilisation</div></div>', 30) +
    clip("gpu", *F["gpu"], f'<div class="gpu" id="gp">{gauge}<div class="gt">🖥️ GPU usage<br><b id="gv">0%</b></div></div>' + stk("s8", "😴", 60, 640, 110) + stk("s9", "💤", 900, 620, 100), 20) +
    clip("edge", *F["edge"], '<div class="pill" style="top:230px" id="eg"><span>💪 India\'s real edge</span></div>' + stk("s10", "👩‍💻", 40, 1370) + stk("s11", "🌐", 910, 1380) + stk("s12", "🤝", 60, 600, 110) + stk("s13", "🚀", 900, 600, 110), 20) +
    clip("poll", *F["poll"], f'<div class="poll" id="pl"><div class="pq">🇮🇳 What should India do?</div>'
         f'<div class="opt" id="o1"><div class="bar" id="pb1" style="width:100%;background:{SAF}"></div><span>1️⃣ Build our own AI 🏗️</span><b id="pv1">0%</b></div>'
         f'<div class="opt" id="o2"><div class="bar" id="pb2" style="width:100%;background:{GRN}"></div><span>2️⃣ Be the AI workforce 👩‍💻</span><b id="pv2">0%</b></div></div>'
         '<div class="cmt" id="cmt"><span>💬 Comment 1 or 2 👇</span></div>' + conf, 25) +
    "".join(clip(f"lk{i}", t, t + 0.45, f'<div class="leak" id="lk{i}x"></div>', 70) for i, t in enumerate(leaks)))
front_js = f'''const CX={CX},CYF={CYF},CRF={CRF};
tl.from("#lb span",{{y:-30,opacity:0,duration:0.3,ease:"power3.out"}},{F["lab"][0]:.3f}).to("#lb",{{opacity:0,duration:0.15}},{F["lab"][1] - 0.15:.3f});
tl.from(["#s1","#s2"],{{scale:0,rotation:-25,duration:0.35,ease:"back.out(2.5)",stagger:0.2}},{F["lab"][0] + 0.3:.3f}).to(["#s1","#s2"],{{y:"-=20",duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{F["lab"][0] + 0.7:.3f});
tl.from("#cm",{{y:-60,opacity:0,duration:0.3,ease:"power3.out"}},{F["cmp"][0]:.3f})
  .fromTo("#b1",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out"}},{F["cmp"][0] + 0.1:.3f}).fromTo("#b2",{{scaleX:0}},{{scaleX:1,duration:0.4}},{T("3%"):.3f})
  .from(["#s3","#s4"],{{scale:0,duration:0.3,ease:"back.out(3)",stagger:0.15}},{T("3%") + 0.1:.3f}).to("#cm",{{opacity:0,duration:0.15}},{F["cmp"][1] - 0.15:.3f});
tl.from("#fx span",{{scale:0.4,opacity:0,duration:0.3,ease:"back.out(2.2)"}},{F["fix"][0]:.3f}).from(["#s5","#s6","#s7"],{{scale:0,y:50,duration:0.3,ease:"back.out(2.5)",stagger:0.12}},{F["fix"][0] + 0.1:.3f})
  .to(["#s5","#s6"],{{rotation:12,duration:0.15,yoyo:true,repeat:5}},{F["fix"][0] + 0.5:.3f});
tl.to("#fl",{{opacity:0.85,duration:0.04}},{TW - 0.05:.3f}).to("#fl",{{opacity:0,duration:0.25}},{TW:.3f})
  .fromTo("#tw",{{scale:3,rotation:-14,opacity:0}},{{scale:1,rotation:-8,opacity:1,duration:0.22,ease:"power4.in"}},{TW:.3f}).to("#tw",{{opacity:0,duration:0.15}},{F["twist"][1] - 0.15:.3f});
tl.fromTo("#nw",{{rotationX:-90,opacity:0}},{{rotationX:0,opacity:1,duration:0.45,ease:"back.out(1.6)"}},{F["news"][0]:.3f}).to("#nw",{{y:-20,rotation:-1.5,duration:0.8,ease:"sine.inOut"}},{F["news"][0] + 0.7:.3f})
  .to("#nw",{{opacity:0,duration:0.15}},{F["news"][1] - 0.15:.3f});
const gv={{v:0}};
tl.from("#gp",{{y:-60,opacity:0,duration:0.3,ease:"power3.out"}},{F["gpu"][0]:.3f}).fromTo("#nd",{{rotation:-90}},{{rotation:-54,duration:0.9,ease:"elastic.out(1,0.5)"}},{T("20%", 2) - 0.2:.3f})
  .to("#garc",{{strokeDashoffset:277,duration:0.9,ease:"power2.out"}},{T("20%", 2) - 0.2:.3f})
  .to(gv,{{v:20,duration:0.9,ease:"power2.out",onUpdate:()=>{{document.getElementById("gv").textContent=Math.round(gv.v)+"%"}}}},{T("20%", 2) - 0.2:.3f})
  .from(["#s8","#s9"],{{scale:0,duration:0.3,ease:"back.out(3)",stagger:0.15}},{T("USED"):.3f}).to("#s9",{{y:-30,opacity:.5,duration:0.6,yoyo:true,repeat:1}},{T("USED") + 0.3:.3f})
  .to("#gp",{{opacity:0,duration:0.15}},{F["gpu"][1] - 0.15:.3f});
tl.from("#eg span",{{scale:0.4,opacity:0,duration:0.3,ease:"back.out(2.2)"}},{F["edge"][0]:.3f}).from(["#s10","#s11","#s12","#s13"],{{scale:0,rotation:20,duration:0.3,ease:"back.out(2.5)",stagger:0.1}},{F["edge"][0] + 0.15:.3f})
  .to("#s13",{{y:-60,x:30,duration:0.8,ease:"power2.in"}},{T("SERVICES"):.3f});
const pv={{a:0,b:0}};
tl.from("#pl",{{y:-80,opacity:0,duration:0.35,ease:"power3.out"}},{F["poll"][0]:.3f})
  .fromTo("#pb1",{{scaleX:0}},{{scaleX:0.52,duration:1.1,ease:"power2.out"}},{T("BUILD") - 0.1:.3f})
  .fromTo("#pb2",{{scaleX:0}},{{scaleX:0.48,duration:1.1,ease:"power2.out"}},{T("WORKFORCE") - 0.6:.3f})
  .to(pv,{{a:52,duration:1.1,ease:"power2.out",onUpdate:()=>{{document.getElementById("pv1").textContent=Math.round(pv.a)+"%"}}}},{T("BUILD") - 0.1:.3f})
  .to(pv,{{b:48,duration:1.1,ease:"power2.out",onUpdate:()=>{{document.getElementById("pv2").textContent=Math.round(pv.b)+"%"}}}},{T("WORKFORCE") - 0.6:.3f})
  .from("#cmt span",{{y:80,opacity:0,duration:0.35,ease:"back.out(2)"}},{T("OR") - 0.1:.3f}).to("#cmt span",{{scale:1.08,duration:0.3,yoyo:true,repeat:5}},{T("OR") + 0.3:.3f})
  .fromTo(".cf",{{x:0,y:0,rotation:0,opacity:1}},{{x:(i)=>CX[i],y:(i)=>CYF[i],rotation:(i)=>CRF[i],opacity:0,duration:1.6,ease:"power2.out"}},{T("WORKFORCE"):.3f});
{"".join(f'tl.fromTo("#lk{i}x",{{x:-200,opacity:0}},{{x:1400,opacity:1,duration:0.45,ease:"power1.inOut"}},{t:.3f});' for i, t in enumerate(leaks))}'''

for d, css, body, js in (("hf_back", back_css, back_body, back_js), ("hf_front", front_css, front_body, front_js)):
    os.makedirs(d + "/assets/fonts", exist_ok=True)
    for f in ("hyperframes.json", "package.json"): shutil.copy(f"/home/claude/r5/hf/{f}", d)
    shutil.copy("/home/claude/r5/hf/assets/gsap.min.js", d + "/assets/")
    for f in os.listdir("/home/claude/r5/hf/assets/fonts"): shutil.copy("/home/claude/r5/hf/assets/fonts/" + f, d + "/assets/fonts/")
    open(d + "/index.html", "w").write(page(css, body, js))
json.dump({"back": B, "front": F, "twist": TW, "speech_end": SPEECH_END, "total": TOTAL}, open("events.json", "w"), indent=1)
print("ok", TOTAL, "twist", TW)
