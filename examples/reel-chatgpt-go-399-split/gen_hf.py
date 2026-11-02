"""'₹399 auto-debit' — CLASSIC SPLIT (early-reel style) + Darsh's rules: face-first hook (never covered), 0.2 s intro sting,
slide-mode split after ~5 s (no blur bars), animated top panel per beat, real OpenAI mark, dense stickers, loop to frame 0."""
import json, sys, re, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="{z}" style="z-index:{z}">{inner}</div>')
OA = re.sub(r'<title>.*?</title>|(height|width)="1em"|style="[^"]*"', '', open("hf/assets/img/openai.svg").read()).replace("<svg ", '<svg class="oa" ', 1)
FZ = json.load(open("faces.json")); r = random.Random(3)
GRN, DK, CRM, RED, YEL, BLU = "#10A37F", "#0B0F0E", "#F5F5F0", "#FF3B3B", "#FFD34D", "#3BA8FF"
PANEL_H = 760; SLIDE = PANEL_H + 20 - FZ["top"]
SPLIT = (T("THE") - 0.1, SPEECH_END)
S = {"year": (SPLIT[0], T("FIRST") - 0.12), "nov": (T("FIRST") - 0.12, T("₹399") - 0.35), "debit": (T("₹399") - 0.35, T("SETTINGS") - 0.25),
     "steps": (T("SETTINGS") - 0.25, T("CANCEL") - 0.08), "cancel": (T("CANCEL") - 0.08, T("SEND") - 0.1), "send": (T("SEND") - 0.1, SPLIT[1])}
CUTS = [S[k][0] for k in ("nov", "debit", "steps", "cancel", "send")]
HOOK_TOP = FZ["free_above"][0] + 30
months = "".join(f'<div class="mo" id="m{i}"><b>{m}</b></div>' for i, m in enumerate("NDJFMAMJJASO"))
sms = "".join(f'<div class="sms" id="sm{i}"><div class="si">🏦</div><div class="st"><b>Debited ₹399.00</b><span>OpenAI · ChatGPT Go · UPI AutoPay · {d}</span></div></div>' for i, d in enumerate(["4 Dec", "4 Jan", "4 Feb"]))
conf = "".join(f'<i class="cf" style="left:540px;top:380px;background:{r.choice([GRN,YEL,CRM,BLU,RED])}"></i>' for _ in range(36))
CX, CY, CR = [r.randint(-520, 520) for _ in range(36)], [r.randint(-380, 420) for _ in range(36)], [r.randint(-600, 600) for _ in range(36)]
pnl = f'''<div class="pnl" id="pnl"><div class="glow"></div>
 <div class="sc" id="year"><div class="hd">{OA}<span>YOUR FREE YEAR</span></div><div class="tlx"><div class="lb l">CLAIMED<br><b>Nov 2025</b></div>{months}<div class="lb r">ENDS<br><b>Nov 2026</b></div></div>
   <div class="prog"><div id="pf"></div></div><div class="big" id="y12"><span id="n12">0</span> MONTHS FREE</div><div class="stamp" id="over">⏳ ENDING NOW</div></div>
 <div class="sc" id="nov"><div class="calp" id="calp"><div class="ct">NOVEMBER</div><div class="cd">4</div><div class="cw">WEDNESDAY</div><div class="ring" id="ring"></div></div>
   <div class="side"><div class="s1">🚨 FIRST FREE YEARS<br>RUN OUT</div><div class="tm" id="tm">THAT’S TOMORROW 😱</div></div></div>
 <div class="sc" id="debit"><div class="phone"><div class="nt">{sms}</div></div><div class="yr" id="yr">= ₹<span id="n4788">0</span> / year 💸</div><div class="au" id="au">🔁 AUTOMATICALLY</div></div>
 <div class="sc" id="steps"><div class="app"><div class="ah">{OA}ChatGPT</div>
   <div class="row" id="r1">⚙️ Settings <em>›</em></div><div class="row" id="r2">👤 Account <em>›</em></div><div class="row" id="r3">💳 Manage plan <em>›</em></div>
   <div class="ren" id="ren">Your plan renews on <b>Nov 4, 2026</b></div></div><div class="cur" id="cur">👆</div>
   <div class="nums"><i id="k1">1</i><i id="k2">2</i><i id="k3">3</i></div></div>
 <div class="sc" id="cancel"><div class="cbtn" id="cb">Cancel plan</div><div class="ok" id="ok">✅ CANCELLED</div><div class="sav" id="sav">₹4,788 / year saved 💰</div>{conf}</div>
 <div class="sc" id="send"><div class="plane" id="pl">✈️</div><div class="sd">📤 SEND THIS TO THE FRIEND<br>WHO CLAIMED IT WITH YOU</div><div class="av"><i id="a1">🙋‍♂️</i><i id="a2">🙋‍♀️</i><i id="a3">🙋</i></div></div>
</div>'''
hook = f'<div class="hz" id="hz"><div class="hk0">{OA}<span>ChatGPT Go · FREE YEAR</span></div><div class="hk1">IT’S ABOUT TO CHARGE YOU <b>₹399</b> ⏰</div></div>'
side = '<i class="stk" id="k_a" style="left:40px;top:1400px">💳</i><i class="stk" id="k_b" style="left:910px;top:1420px">⏰</i><i class="stk" id="k_c" style="left:60px;top:760px;font-size:90px">⚠️</i><i class="stk" id="k_d" style="left:920px;top:740px;font-size:90px">💸</i>'
css = f'''@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}} @font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}} @font-face{{font-family:MO;src:url(assets/fonts/DejaVuSansMono.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}} .full{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.oa{{width:54px;height:54px;color:#fff;fill:currentColor}}
.hz{{position:absolute;left:30px;right:30px;top:{HOOK_TOP}px;text-align:center}}
.hk0{{display:inline-flex;align-items:center;gap:14px;font-size:44px;background:{GRN};padding:10px 30px;border-radius:99px;margin-bottom:22px}}
.hk1{{font-size:78px;line-height:1.1;background:{CRM};color:#111;padding:20px 30px;border-radius:30px;box-shadow:0 18px 40px rgba(0,0,0,.5)}} .hk1 b{{color:{RED}}}
.stk{{position:absolute;font-size:120px;font-style:normal;filter:drop-shadow(0 10px 16px rgba(0,0,0,.5))}}
.pnl{{position:absolute;left:0;top:0;width:1080px;height:{PANEL_H}px;overflow:hidden;background:linear-gradient(180deg,#0E1A16,{DK});border-bottom:10px solid {GRN}}}
.glow{{position:absolute;left:240px;top:-200px;width:600px;height:600px;border-radius:50%;background:{GRN};opacity:.18;filter:blur(120px)}}
.sc{{position:absolute;inset:0;opacity:0}} .hd{{position:absolute;left:0;right:0;top:50px;display:flex;justify-content:center;align-items:center;gap:16px;font-size:52px}}
.tlx{{position:absolute;left:40px;right:40px;top:180px;display:flex;align-items:center;gap:8px}} .mo{{flex:1;height:110px;border-radius:14px;background:rgba(255,255,255,.07);display:flex;align-items:center;justify-content:center;font-size:36px;color:#9fb}}
.mo.on{{background:{GRN};color:#fff}} .lb{{width:150px;font-family:PM;font-size:26px;text-align:center;color:#cde}} .lb b{{font-family:PB;font-size:30px;color:#fff}}
.prog{{position:absolute;left:190px;right:190px;top:320px;height:24px;border-radius:12px;background:rgba(255,255,255,.1);overflow:hidden}} #pf{{height:100%;background:linear-gradient(90deg,{GRN},{YEL},{RED});transform-origin:left}}
.big{{position:absolute;left:0;right:0;top:390px;text-align:center;font-size:110px}}
.stamp{{position:absolute;left:0;right:0;top:570px;margin:auto;width:max-content;font-size:70px;color:{RED};border:9px solid {RED};padding:0 30px;border-radius:18px;transform:rotate(-5deg);background:rgba(11,15,14,.85)}}
.calp{{position:absolute;left:80px;top:90px;width:420px;height:560px;background:#fff;border-radius:30px;overflow:hidden;color:#111;text-align:center;box-shadow:0 30px 60px rgba(0,0,0,.6);transform:rotate(-4deg)}}
.ct{{background:{RED};color:#fff;font-size:56px;padding:20px 0}} .cd{{font-size:300px;line-height:1.15}} .cw{{font-family:PM;font-size:38px;color:#555}}
.ring{{position:absolute;left:70px;top:120px;width:280px;height:330px;border:12px solid {RED};border-radius:50%;transform:rotate(-8deg)}}
.side{{position:absolute;left:540px;right:40px;top:170px;text-align:left}} .s1{{font-size:56px;line-height:1.15}}
.tm{{margin-top:40px;font-size:60px;background:{YEL};color:#111;padding:14px 24px;border-radius:20px;display:inline-block;transform:rotate(3deg)}}
.phone{{position:absolute;left:70px;right:70px;top:40px;height:520px}} .nt{{position:absolute;inset:0}}
.sms{{position:absolute;left:0;right:0;height:150px;border-radius:34px;background:rgba(245,245,240,.96);color:#111;display:flex;align-items:center;gap:24px;padding:0 30px;box-shadow:0 20px 40px rgba(0,0,0,.5)}}
.sms:nth-child(1){{top:0}} .sms:nth-child(2){{top:170px}} .sms:nth-child(3){{top:340px}} .si{{font-size:70px}} .st b{{display:block;font-size:52px;color:{RED}}} .st span{{font-family:PM;font-size:28px;color:#444}}
.yr{{position:absolute;left:0;right:0;top:560px;text-align:center;font-size:80px;color:{YEL}}} .au{{position:absolute;right:50px;top:30px;font-size:34px;background:{RED};padding:6px 18px;border-radius:12px;transform:rotate(5deg)}}
.app{{position:absolute;left:120px;right:300px;top:40px;height:660px;background:#171717;border:4px solid #333;border-radius:40px;padding:30px}}
.ah{{display:flex;align-items:center;gap:14px;font-size:44px;margin-bottom:30px}} .row{{font-family:PM;font-size:44px;padding:26px 24px;border-radius:20px;margin:10px 0;background:#222;display:flex;justify-content:space-between}}
.row.on{{background:{GRN};font-family:PB}} .row em{{font-style:normal;color:#888}} .ren{{margin-top:30px;font-family:PM;font-size:32px;color:#ccc;background:#2a2a1a;border:3px solid {YEL};border-radius:18px;padding:16px}} .ren b{{color:{YEL}}}
.cur{{position:absolute;left:600px;top:600px;font-size:110px}} .nums{{position:absolute;right:60px;top:180px;display:flex;flex-direction:column;gap:40px}}
.nums i{{font-style:normal;width:110px;height:110px;border-radius:50%;background:rgba(255,255,255,.1);font-size:60px;display:flex;align-items:center;justify-content:center}} .nums i.on{{background:{GRN}}}
.cbtn{{position:absolute;left:0;right:0;top:120px;margin:auto;width:max-content;font-size:90px;background:{RED};padding:30px 80px;border-radius:40px;box-shadow:0 20px 50px rgba(255,59,59,.4)}}
.ok{{position:absolute;left:0;right:0;top:340px;text-align:center;font-size:110px;color:{GRN}}} .sav{{position:absolute;left:0;right:0;top:520px;text-align:center;font-size:64px;color:{YEL}}}
.cf{{position:absolute;width:20px;height:32px;border-radius:4px}}
.plane{{position:absolute;left:100px;top:200px;font-size:170px}} .sd{{position:absolute;left:0;right:0;top:120px;text-align:center;font-size:64px;line-height:1.2}}
.av{{position:absolute;left:0;right:0;top:420px;display:flex;justify-content:center;gap:60px;font-size:170px}} .av i{{font-style:normal}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.leak{{position:absolute;left:-400px;top:-300px;width:700px;height:2600px;background:linear-gradient(90deg,transparent,rgba(16,163,127,.55),rgba(255,211,77,.35),transparent);filter:blur(34px);transform:rotate(16deg)}}
.sh{{position:absolute;left:0;right:0;height:960px;background:{DK}}} .sh.t{{top:0;border-bottom:6px solid {GRN}}} .sh.b{{top:960px;border-top:6px solid {GRN}}}
.shl{{position:absolute;left:0;right:0;top:860px;display:flex;justify-content:center}} .shl .oa{{width:200px;height:200px}}'''
def sc(k): s, e = S[k]; return f'tl.set("#{k}",{{opacity:1}},{s:.3f}).set("#{k}",{{opacity:0}},{e:.3f});'
cx, cy, cr = ",".join(map(str, CX)), ",".join(map(str, CY)), ",".join(map(str, CR))
js = "\n".join(sc(k) for k in S) + f'''
tl.fromTo("#shl",{{scale:1.6,rotation:-90}},{{scale:0.3,rotation:120,opacity:0,duration:0.16,ease:"power2.in"}},0)
  .to("#sht",{{y:-980,duration:0.2,ease:"power3.in"}},0.08).to("#shb",{{y:980,duration:0.2,ease:"power3.in"}},0.08).set("#f0",{{opacity:0.7}},0.2).to("#f0",{{opacity:0,duration:0.1}},0.21);
tl.to("#hz",{{scale:1.04,duration:{SPLIT[0]-0.4:.3f},ease:"sine.inOut"}},0).to("#hz",{{opacity:0,y:-30,duration:0.2}},{SPLIT[0]-0.15:.3f});
tl.from(["#k_a","#k_b","#k_c","#k_d"],{{scale:0,rotation:-30,duration:0.3,stagger:0.25,ease:"back.out(2.5)"}},{T("CHARGING") - 0.6:.3f}).to(["#k_a","#k_b","#k_c","#k_d"],{{scale:0,duration:0.15}},{SPLIT[0]-0.15:.3f});
tl.fromTo("#tz",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:{TOTAL-SPEECH_END-0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});
tl.fromTo("#pnl",{{y:-{PANEL_H+20}}},{{y:0,duration:0.25,ease:"power3.out"}},{SPLIT[0]:.3f}).to("#pnl",{{y:-{PANEL_H+20},duration:0.22,ease:"power3.in"}},{SPLIT[1]-0.22:.3f});
const N=(id,to,d,at,f=(v)=>Math.round(v))=>{{const o={{v:0}};tl.to(o,{{v:to,duration:d,ease:"power2.out",onUpdate:()=>{{document.getElementById(id).textContent=f(o.v)}}}},at);}};
for(let i=0;i<12;i++) tl.set("#m"+i,{{className:"mo on"}},{S["year"][0] + 0.3:.3f}+i*0.1);
tl.fromTo("#pf",{{scaleX:0}},{{scaleX:1,duration:1.2,ease:"none"}},{S["year"][0] + 0.3:.3f}); N("n12",12,1.2,{S["year"][0] + 0.3:.3f});
tl.fromTo("#over",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.in"}},{T("CLAIMED") - 0.1:.3f});
tl.from("#calp",{{y:-800,rotation:-30,duration:0.4,ease:"back.out(1.4)"}},{S["nov"][0]:.3f}).from(".s1",{{x:500,opacity:0,duration:0.3}},{S["nov"][0] + 0.2:.3f})
  .fromTo("#ring",{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2)"}},{T("NOVEMBER"):.3f})
  .fromTo("#tm",{{scale:0,rotation:-20}},{{scale:1,rotation:3,duration:0.3,ease:"back.out(2.5)"}},{T("4TH") + 0.2:.3f});
[0,1,2].forEach(i=>tl.from("#sm"+i,{{x:-1100,duration:0.3,ease:"power3.out"}},{S["debit"][0] + 0.25:.3f}+i*0.45));
tl.from("#au",{{scale:0,duration:0.25,ease:"back.out(3)"}},{T("AUTOMATICALLY"):.3f}); N("n4788",4788,0.8,{T("MONTH"):.3f},(v)=>Math.round(v).toLocaleString("en-IN"));
tl.from(".app",{{y:700,duration:0.35,ease:"power3.out"}},{S["steps"][0]:.3f});
tl.set("#r1",{{className:"row on"}},{T("SETTINGS"):.3f}).set("#k1",{{className:"on"}},{T("SETTINGS"):.3f}).to("#cur",{{x:-300,y:-420,duration:0.3}},{T("SETTINGS") - 0.3:.3f})
  .set("#r2",{{className:"row on"}},{T("ACCOUNT"):.3f}).set("#k2",{{className:"on"}},{T("ACCOUNT"):.3f}).to("#cur",{{y:-290,duration:0.25}},{T("ACCOUNT") - 0.25:.3f})
  .set("#r3",{{className:"row on"}},{T("MANAGE"):.3f}).set("#k3",{{className:"on"}},{T("MANAGE"):.3f}).to("#cur",{{y:-160,duration:0.25}},{T("MANAGE") - 0.25:.3f})
  .from("#ren",{{scale:0.5,opacity:0,duration:0.3,ease:"back.out(2)"}},{T("CHECK"):.3f}).to("#cur",{{y:-20,duration:0.25}},{T("CHECK"):.3f});
tl.from("#cb",{{scale:0.4,opacity:0,duration:0.25,ease:"back.out(2)"}},{S["cancel"][0]:.3f}).to("#cb",{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},{T("CANCEL") + 0.25:.3f})
  .from("#ok",{{scale:2,opacity:0,duration:0.2,ease:"power4.in"}},{T("CANCEL") + 0.4:.3f}).from("#sav",{{y:60,opacity:0,duration:0.3}},{T("CANCEL") + 0.7:.3f});
const CX=[{cx}],CY=[{cy}],CR=[{cr}];
tl.fromTo("#cancel .cf",{{x:0,y:0,opacity:1}},{{x:(i)=>CX[i],y:(i)=>CY[i],rotation:(i)=>CR[i],opacity:0,duration:1.4,ease:"power2.out"}},{T("CANCEL") + 0.4:.3f});
tl.fromTo("#pl",{{x:-300,y:200,rotation:0}},{{x:1100,y:-300,rotation:20,duration:1.0,ease:"power1.in"}},{S["send"][0]:.3f})
  .from(".sd",{{scale:0.5,opacity:0,duration:0.3,ease:"back.out(2)"}},{S["send"][0] + 0.2:.3f})
  .from(["#a1","#a2","#a3"],{{y:200,opacity:0,duration:0.3,stagger:0.15,ease:"back.out(2)"}},{T("FRIEND") - 0.1:.3f});
{"".join(f'tl.set("#fl{i}",{{opacity:0.5}},{t:.3f}).to("#fl{i}",{{opacity:0,duration:0.15}},{t + 0.02:.3f}).fromTo("#lk{i}",{{x:-300}},{{x:1500,duration:0.5,ease:"power1.inOut"}},{t - 0.12:.3f});' for i, t in enumerate(CUTS))}'''
body = (clip("panel", *SPLIT, pnl, 5) + clip("hook", 0, SPLIT[0] + 0.05, hook + side, 30) + clip("tail", SPEECH_END, TOTAL, hook.replace('id="hz"', 'id="tz"'), 30) +
        clip("intro", 0, 0.32, f'<div class="sh t" id="sht"></div><div class="sh b" id="shb"></div><div class="shl" id="shl">{OA}</div><div class="flash" id="f0"></div>', 80) +
        "".join(clip(f"tr{i}", t - 0.12, t + 0.4, f'<div class="flash" id="fl{i}"></div><div class="leak" id="lk{i}"></div>', 60) for i, t in enumerate(CUTS)))
doc = (f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body>'
       f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">{body}</div>'
       f'<script>const tl = gsap.timeline({{paused:true}});\n{js}\nwindow.__timelines["main"] = tl; tl.seek(0);</script></body></html>')
open("hf/index.html", "w").write(doc)
json.dump({"split": SPLIT, "scenes": S, "cuts": CUTS, "slide": SLIDE, "panel_h": PANEL_H, "speech_end": SPEECH_END, "total": TOTAL}, open("events.json", "w"), indent=1)
print("ok", SPLIT, "slide", SLIDE)
