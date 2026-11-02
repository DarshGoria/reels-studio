"""NN3 'India's AI paradox' — classic split style (Genie 4 / India shopping look): face-first hook,
slide-mode split with an animated 'India AI dashboard' panel, plot-twist glitch, live comment poll; loops to frame 0."""
import json, sys, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')
FZ = json.load(open("faces.json")); r = random.Random(5)
SAF, GRN, NAVY, CREAM, RED, YEL = "#FF9933", "#22C55E", "#0A1033", "#FFF6EA", "#FF3D3D", "#FFD34D"
PANEL_H = 760
SPLIT = (T("BUT") - 0.1, SPEECH_END)
TW = T("BUT", 2)
S = {"cmp": (SPLIT[0], T("$300") - 0.15), "money": (T("$300") - 0.15, TW - 0.05), "twist": (TW - 0.05, T("REPORT") - 0.1),
     "news": (T("REPORT") - 0.1, T("CHIPS") - 0.2), "chip": (T("CHIPS") - 0.2, T("REAL") - 0.12),
     "edge": (T("REAL") - 0.12, T("SHOULD") - 0.08), "poll": (T("SHOULD") - 0.08, SPLIT[1])}
HOOK_TOP = FZ["free_above"][0] + 10
cash = "".join(f'<div class="cs" style="left:{r.randint(0,1000)}px;top:{r.randint(-500,-80)}px;font-size:{r.randint(60,100)}px">💵</div>' for _ in range(26))
CY = [r.randint(900, 1300) for _ in range(26)]
blds = "".join(f'<div class="bd" style="left:{60 + i*165}px;height:{h}px"><i></i><i></i><i></i><i></i></div>' for i, h in enumerate([210, 300, 250, 340, 230, 280]))
chips = "".join(f'<div class="ch{" on" if i in (2, 7) else ""}"><b>AI</b>{"" if i in (2, 7) else "<s>💤</s>"}</div>' for i in range(10))
pnl = f'''<div class="pnl" id="pnl"><div class="tri"><i style="background:{SAF}"></i><i style="background:{CREAM}"></i><i style="background:{GRN}"></i></div><div class="grid"></div>
 <div class="sc" id="cmp"><div class="hd">🇮🇳 INDIA · DATA CHECK</div>
   <div class="cols"><div class="col"><div class="lb">🌍 World’s data</div><div class="big" style="color:{SAF}"><span id="n20">0</span>%</div><div class="bar"><div id="b20" style="width:100%;background:{SAF}"></div></div></div>
   <div class="col"><div class="lb">🏢 Data centres</div><div class="big" style="color:{GRN}"><span id="n3">0</span>%</div><div class="bar"><div id="b3" style="width:15%;background:{GRN}"></div></div></div></div>
   <div class="stamp" id="mm">MISMATCH 😬</div></div>
 <div class="sc" id="money"><div class="cash">{cash}</div><div class="city">{blds}</div>
   <div class="mtop"><div class="m1">$<span id="n300">0</span> BILLION</div><div class="m2">🏗️ PROMISE TO FIX IT</div></div></div>
 <div class="sc" id="twist"><div class="tw"><div class="r">PLOT TWIST</div><div class="c">PLOT TWIST</div><div class="w">PLOT TWIST</div></div></div>
 <div class="sc" id="news"><div class="paper" id="pp"><div class="mast">THE AI DAILY</div><div class="hl">India’s AI chips are only<br>about <u>20% used</u></div><div class="sub">New report · compute utilisation</div><div class="nr" id="nr">NEW REPORT</div></div></div>
 <div class="sc" id="chip"><div class="hd">🖥️ INDIA’S AI CHIPS RIGHT NOW</div><div class="chips">{chips}</div>
   <div class="ut">USED: <span id="u20" style="color:{YEL}">0</span>%</div><div class="stamp" id="idle" style="top:620px">80% IDLE 😴</div></div>
 <div class="sc" id="edge"><div class="hd">💪 OUR REAL EDGE</div><div class="sv" id="sv">AI SERVICES</div>
   {"".join(f'<div class="ic" id="ic{i}" style="left:{x}px;top:{y}px">{e}</div>' for i, (e, x, y) in enumerate((("👩‍💻", 80, 420), ("🤝", 300, 560), ("🌍", 640, 560), ("💼", 880, 420))))}</div>
 <div class="sc" id="poll"><div class="pq">SHOULD INDIA… 🇮🇳</div>
   <div class="op"><div class="ob" id="o1"></div><span>1️⃣ Build its own AI</span><em id="p1">0%</em></div>
   <div class="op"><div class="ob g" id="o2"></div><span>2️⃣ Be the world’s AI workforce</span><em id="p2">0%</em></div>
   <div class="cm" id="cm">💬 COMMENT 1 OR 2 👇</div></div>
</div>'''
hook = '<div class="hz" id="hz"><div class="hk0">🇮🇳 INDIA\'S AI PARADOX</div><div class="hk1"><b>20%</b> OF THE WORLD\'S DATA 🤯</div></div>'
tail = hook.replace('id="hz"', 'id="tz"')
css = f'''@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}} @font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}} .full{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.hz{{position:absolute;left:30px;right:30px;top:{HOOK_TOP}px;text-align:center}}
.hk0{{display:inline-block;font-size:44px;background:{NAVY};border:4px solid {SAF};padding:8px 28px;border-radius:99px;margin-bottom:22px}}
.hk1{{font-size:76px;line-height:1.08;background:{CREAM};color:#111;padding:18px 30px;border-radius:28px;box-shadow:0 18px 40px rgba(0,0,0,.5)}} .hk1 b{{color:{SAF};font-size:96px}}
.pnl{{position:absolute;left:0;top:0;width:1080px;height:{PANEL_H}px;overflow:hidden;background:radial-gradient(circle at 50% 30%,#1b2a7a,{NAVY} 70%);border-bottom:10px solid {SAF}}}
.tri{{position:absolute;left:0;right:0;top:0;height:12px;display:flex}} .tri i{{flex:1}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:60px 60px}}
.sc{{position:absolute;inset:0;opacity:0}}
.hd{{position:absolute;left:0;right:0;top:60px;text-align:center;font-size:50px;letter-spacing:.02em}}
.cols{{position:absolute;left:50px;right:50px;top:170px;display:flex;gap:40px}} .col{{flex:1;background:rgba(255,255,255,.06);border:3px solid rgba(255,255,255,.15);border-radius:30px;padding:24px 26px}}
.lb{{font-family:PM;font-size:40px;color:#cfd6ff}} .big{{font-size:190px;line-height:1.05}}
.bar{{height:30px;background:rgba(255,255,255,.12);border-radius:15px;overflow:hidden}} .bar div{{height:100%;transform-origin:left}}
.stamp{{position:absolute;left:0;right:0;top:600px;margin:auto;width:max-content;font-size:62px;color:{RED};border:8px solid {RED};padding:0 30px;border-radius:18px;transform:rotate(-5deg);background:rgba(10,16,51,.85)}}
.cash{{position:absolute;inset:0}} .cs{{position:absolute}}
.city{{position:absolute;left:0;right:0;bottom:0;height:360px}} .bd{{position:absolute;bottom:0;width:140px;background:linear-gradient(180deg,#2c3b8f,#151d52);border:3px solid #4256c8;border-bottom:none;border-radius:10px 10px 0 0;transform-origin:bottom;display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:18px}}
.bd i{{height:22px;background:{YEL};opacity:.8;border-radius:4px}}
.mtop{{position:absolute;left:0;right:0;top:90px;text-align:center}} .m1{{font-size:120px;color:{GRN};text-shadow:0 0 40px rgba(34,197,94,.5)}} .m2{{display:inline-block;font-size:50px;background:{CREAM};color:#111;padding:8px 26px;border-radius:18px;margin-top:10px}}
#twist{{background:#2a0000}} .tw{{position:absolute;left:0;right:0;top:270px;text-align:center;font-size:170px;line-height:1}} .tw div{{position:absolute;left:0;right:0}} .tw .r{{color:#ff0040;mix-blend-mode:screen}} .tw .c{{color:#00e5ff;mix-blend-mode:screen}} .tw .w{{color:#fff}}
.paper{{position:absolute;left:90px;right:90px;top:120px;background:#f3ead8;color:#151515;border-radius:12px;padding:30px 40px;box-shadow:0 30px 60px rgba(0,0,0,.6);transform:rotate(-2deg)}}
.mast{{font-size:38px;letter-spacing:.3em;text-align:center;border-bottom:4px double #151515;padding-bottom:12px}} .hl{{font-size:70px;line-height:1.1;margin-top:20px}} .hl u{{text-decoration-color:{RED};text-decoration-thickness:10px}}
.sub{{font-family:PM;font-size:32px;color:#555;margin-top:14px}} .nr{{position:absolute;right:-30px;top:-40px;font-size:44px;background:{RED};color:#fff;padding:8px 22px;border-radius:12px;transform:rotate(8deg)}}
.chips{{position:absolute;left:110px;right:110px;top:160px;display:grid;grid-template-columns:repeat(5,1fr);gap:26px}}
.ch{{position:relative;height:140px;border-radius:18px;background:#20264d;border:4px solid #3a4280;display:flex;align-items:center;justify-content:center;font-size:44px;color:#59608f}}
.ch.on{{background:#3b3410;border-color:{YEL};color:{YEL};box-shadow:0 0 40px rgba(255,211,77,.7)}} .ch s{{position:absolute;right:6px;top:2px;font-size:36px;text-decoration:none}}
.ut{{position:absolute;left:0;right:0;top:480px;text-align:center;font-size:70px}}
.sv{{position:absolute;left:0;right:0;top:200px;text-align:center;font-size:150px;color:{SAF};text-shadow:0 0 50px rgba(255,153,51,.5)}} .ic{{position:absolute;font-size:110px}}
.pq{{position:absolute;left:0;right:0;top:60px;text-align:center;font-size:66px}}
.op{{position:absolute;left:60px;right:60px;height:120px;border-radius:26px;background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.2);overflow:hidden;display:flex;align-items:center;padding:0 30px;font-size:46px}}
.op:nth-of-type(2){{top:200px}} .op:nth-of-type(3){{top:350px}} .ob{{position:absolute;left:0;top:0;bottom:0;width:100%;background:{SAF};opacity:.75;transform-origin:left;transform:scaleX(0)}} .ob.g{{background:{GRN}}}
.op span{{position:relative;flex:1}} .op em{{position:relative;font-style:normal;font-size:52px}}
.cm{{position:absolute;left:0;right:0;top:540px;margin:auto;width:max-content;font-size:56px;background:{CREAM};color:#111;padding:14px 36px;border-radius:24px}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.stk{{position:absolute;font-size:120px;filter:drop-shadow(0 10px 16px rgba(0,0,0,.5))}}'''
def sc(id_): s, e = S[id_]; return f'tl.set("#{id_}",{{opacity:1}},{s:.3f}).set("#{id_}",{{opacity:0}},{e:.3f});'
cy = ",".join(map(str, CY))
js = "\n".join(sc(k) for k in S) + f'''
tl.to("#hz",{{scale:1.04,duration:{SPLIT[0]-0.4:.3f},ease:"sine.inOut"}},0.0).to("#hz",{{opacity:0,y:-30,duration:0.2}},{SPLIT[0]-0.15:.3f});
tl.fromTo("#tz",{{opacity:0,scale:0.9}},{{opacity:1,scale:1.0,duration:{TOTAL-SPEECH_END-0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});
tl.fromTo("#pnl",{{y:-{PANEL_H+20}}},{{y:0,duration:0.25,ease:"power3.out"}},{SPLIT[0]:.3f}).to("#pnl",{{y:-{PANEL_H+20},duration:0.22,ease:"power3.in"}},{SPLIT[1]-0.22:.3f});
const N=(id,to,d,at,sf="")=>{{const o={{v:0}};tl.to(o,{{v:to,duration:d,ease:"power2.out",onUpdate:()=>{{document.getElementById(id).textContent=Math.round(o.v)+sf}}}},at);}};
tl.from(".col",{{y:300,opacity:0,duration:0.35,stagger:0.12,ease:"power3.out"}},{S["cmp"][0]+0.15:.3f});
N("n20",20,0.6,{S["cmp"][0]+0.25:.3f}); tl.fromTo("#b20",{{scaleX:0}},{{scaleX:1,duration:0.6}},{S["cmp"][0]+0.25:.3f});
N("n3",3,0.5,{T("3%"):.3f}); tl.fromTo("#b3",{{scaleX:0}},{{scaleX:1,duration:0.5}},{T("3%"):.3f});
tl.fromTo("#mm",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{T("CENTERS"):.3f});
tl.from(".mtop",{{y:-200,opacity:0,duration:0.3,ease:"back.out(1.8)"}},{S["money"][0]:.3f}); N("n300",300,0.8,{S["money"][0]+0.1:.3f});
const CY=[{cy}]; document.querySelectorAll(".cs").forEach((d,i)=>{{tl.fromTo(d,{{y:0,rotation:-20}},{{y:CY[i],rotation:20,duration:1.6,ease:"none"}},{S["money"][0]:.3f}+(i%8)*0.12);}});
tl.from(".bd",{{scaleY:0,duration:0.4,stagger:0.08,ease:"back.out(1.6)"}},{T("FIX")-0.2:.3f});
const J=[[-22,10],[16,-8],[-10,14],[24,-12],[-14,8],[8,-16],[0,0]]; J.forEach(([a,b],i)=>{{tl.set(".tw .r",{{x:a,y:b}},{TW:.3f}+i*0.08).set(".tw .c",{{x:-a,y:-b}},{TW:.3f}+i*0.08);}});
tl.from(".tw",{{scale:2,duration:0.18,ease:"power4.out"}},{TW:.3f}).set("#fl",{{opacity:0.8}},{TW:.3f}).to("#fl",{{opacity:0,duration:0.3}},{TW + 0.01:.3f});
tl.from("#pp",{{y:-700,rotation:-20,duration:0.4,ease:"power3.out"}},{S["news"][0]:.3f}).fromTo("#nr",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{S["news"][0]+0.5:.3f});
tl.from(".ch",{{scale:0,duration:0.25,stagger:0.04,ease:"back.out(2)"}},{S["chip"][0]+0.05:.3f});
N("u20",20,0.6,{T("20%",2):.3f}); tl.fromTo("#idle",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{T("USED"):.3f});
tl.from("#sv",{{scale:0.3,opacity:0,duration:0.35,ease:"back.out(2)"}},{T("SERVICES")-0.1:.3f}).from("#edge .hd",{{y:-120,opacity:0,duration:0.3}},{S["edge"][0]+0.05:.3f});
tl.from(["#ic0","#ic1","#ic2","#ic3"],{{scale:0,rotation:30,duration:0.3,stagger:0.12,ease:"back.out(2.5)"}},{T("EDGE"):.3f}).to(["#ic0","#ic1","#ic2","#ic3"],{{y:"-=20",duration:0.4,yoyo:true,repeat:3}},{T("SERVICES")+0.3:.3f});
tl.from(".pq",{{y:-100,opacity:0,duration:0.3}},{S["poll"][0]+0.05:.3f}).from(".op",{{x:-1100,duration:0.35,stagger:0.15,ease:"power3.out"}},{S["poll"][0]+0.25:.3f});
tl.to("#o1",{{scaleX:0.52,duration:0.8,ease:"power2.out"}},{T("BUILD"):.3f}); N("p1",52,0.8,{T("BUILD"):.3f},"%");
tl.to("#o2",{{scaleX:0.48,duration:0.8,ease:"power2.out"}},{T("WORKFORCE")-0.7:.3f}); N("p2",48,0.8,{T("WORKFORCE")-0.7:.3f},"%");
tl.from("#cm",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{T("OR")+0.2:.3f}).to("#cm",{{scale:1.08,duration:0.3,yoyo:true,repeat:3}},{T("OR")+0.6:.3f});
tl.from(["#k1","#k2"],{{scale:0,rotation:-25,duration:0.3,stagger:0.15,ease:"back.out(2.5)"}},{T("20%")-0.05:.3f}).to(["#k1","#k2"],{{scale:0,duration:0.15}},{SPLIT[0]-0.15:.3f});'''
st = '<div class="stk" id="k1" style="left:40px;top:1400px">📊</div><div class="stk" id="k2" style="left:900px;top:1420px">🌍</div>'
body = (clip("panel", *SPLIT, pnl + '<div class="flash" id="fl"></div>', 5) + clip("hook", 0, SPLIT[0] + 0.05, hook + st, 30) + clip("tail", SPEECH_END, TOTAL, tail, 30))
doc = (f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body>'
       f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">{body}</div>'
       f'<script>const tl = gsap.timeline({{paused:true}});\n{js}\nwindow.__timelines["main"] = tl; tl.seek(0);</script></body></html>')
open("hf/index.html", "w").write(doc)
json.dump({"split": SPLIT, "scenes": S, "twist": TW, "panel_h": PANEL_H, "speech_end": SPEECH_END, "total": TOTAL}, open("events.json", "w"), indent=1)
print("ok", SPLIT, "slide", PANEL_H + 20 - FZ["top"])
