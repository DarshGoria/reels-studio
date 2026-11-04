"""ElevenLabs $1 — CLASSIC SPLIT + rules: 0.2 s logo sting, face-first hook, slide split after 3 s, one panel scene per beat
(price slash, Nov 8 deadline, feature checklist, voice-clone waveforms, auto-renew warning, save/send), loop to frame 0."""
import json, sys, re, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="{z}" style="z-index:{z}">{inner}</div>')
def svg(n, cls):
    s = re.sub(r'<title>.*?</title>|(height|width)="1em"|style="[^"]*"', '', open(f"hf/assets/img/{n}.svg").read())
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)
EL, ELT = svg("elevenlabs", "el"), svg("elevenlabs-text", "elt")
FZ = json.load(open("faces.json")); r = random.Random(11)
VIO, DK, CRM, RED, YEL, GRN = "#8B5CF6", "#0A0A0C", "#F7F7F5", "#FF3B3B", "#FFD34D", "#22C55E"
PANEL_H = 760; SLIDE = PANEL_H + 20 - FZ["top"]
SPLIT = (T("ELEVEN") - 0.1, SPEECH_END)
S = {"price": (SPLIT[0], T("NORMALLY") - 0.1), "date": (T("NORMALLY") - 0.1, T("FOR", 3) - 0.1), "feat": (T("FOR", 3) - 0.1, T("UPLOAD") - 0.1),
     "clone": (T("UPLOAD") - 0.1, T("JUST", 2) - 0.1), "renew": (T("JUST", 2) - 0.1, T("SAVE") - 0.1), "send": (T("SAVE") - 0.1, SPLIT[1])}
CUTS = [S[k][0] for k in ("date", "feat", "clone", "renew", "send")]
HOOK_TOP = FZ["free_above"][0] + 10
bars = lambda n, cls: "".join(f'<i class="{cls}" style="height:{r.randint(20,150)}px"></i>' for _ in range(n))
W1, W2 = bars(34, "wb"), bars(34, "wb c")
conf = "".join(f'<i class="cf" style="left:540px;top:380px;background:{r.choice([VIO,YEL,CRM,GRN])}"></i>' for _ in range(30))
CX, CY, CR = [r.randint(-520, 520) for _ in range(30)], [r.randint(-380, 420) for _ in range(30)], [r.randint(-600, 600) for _ in range(30)]
pnl = f'''<div class="pnl" id="pnl"><div class="glow"></div>
 <div class="sc" id="price"><div class="brand">{ELT}</div><div class="card" id="card"><div class="pl">STARTER PLAN</div>
   <div class="pr"><span class="old" id="old">$6</span><span class="new" id="new">$1</span></div><div class="fm">FIRST MONTH</div><div class="off" id="off">-83%</div></div></div>
 <div class="sc" id="date"><div class="calp" id="calp"><div class="ct">NOVEMBER</div><div class="cd">8</div><div class="cw">OFFER ENDS</div></div>
   <div class="side"><div class="s1">Normally <s>$6</s>/mo</div><div class="tm" id="tm">⏳ ENDS NOV 8</div></div></div>
 <div class="sc" id="feat"><div class="hd">FOR <b>$1</b> YOU GET</div>
   <div class="ck" id="c1">🎙️ 30 min of AI voice <em>✓</em></div><div class="ck" id="c2">📄 Commercial license <em>✓</em></div><div class="ck" id="c3">🧬 Instant voice cloning <em>✓</em></div></div>
 <div class="sc" id="clone"><div class="hd">UPLOAD <b>1 MIN</b> OF YOUR VOICE</div>
   <div class="wv"><div class="wl">🎤 YOU</div><div class="wf" id="wf1">{W1}</div></div><div class="arr" id="arr">⬇ AI</div>
   <div class="wv"><div class="wl">🤖 CLONE</div><div class="wf" id="wf2">{W2}</div></div><div class="tk" id="tk">TALKS LIKE YOU</div></div>
 <div class="sc" id="renew"><div class="hd">⚠️ IT AUTO-RENEWS</div><div class="mos"><div class="mo"><b>MONTH 1</b><span style="color:{GRN}">$1</span></div><div class="ar2">→</div>
   <div class="mo m2" id="m2"><b>MONTH 2</b><span style="color:{RED}">$6 🔁</span></div></div><div class="cbtn" id="cb">Cancel before month 2</div>{conf}</div>
 <div class="sc" id="send"><div class="row2"><div class="sv" id="sv">🔖<b>SAVE</b></div><div class="sv" id="sd">✈️<b>SEND</b></div></div><div class="yt" id="yt">to your friend who makes<br><b>YouTube videos 🎥</b></div></div>
</div>'''
hook = f'<div class="hz" id="hz"><div class="hk0">{EL}<span>AI VOICE CLONING</span></div><div class="hk1">CLONE YOUR VOICE<br>FOR JUST <b>$1</b> 🎙️</div></div>'
side = '<i class="stk" id="k_a" style="left:50px;top:1250px">🎙️</i><i class="stk" id="k_b" style="left:900px;top:1230px">💵</i><i class="stk" id="k_c" style="left:70px;top:620px;font-size:90px">🧬</i><i class="stk" id="k_d" style="left:920px;top:620px;font-size:90px">🤯</i>'
css = f'''@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}} @font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}} .full{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.el{{width:56px;height:56px;fill:currentColor;color:#fff}} .elt{{height:60px;width:auto;fill:currentColor;color:#fff}}
.hz{{position:absolute;left:30px;right:30px;top:{HOOK_TOP}px;text-align:center}}
.hk0{{display:inline-flex;align-items:center;gap:12px;font-size:42px;background:{DK};border:4px solid {VIO};padding:8px 28px;border-radius:99px;margin-bottom:20px}} .hk0 .el{{width:44px;height:44px}}
.hk1{{font-size:84px;line-height:1.08;background:{CRM};color:#111;padding:20px 30px;border-radius:30px;box-shadow:0 18px 40px rgba(0,0,0,.35)}} .hk1 b{{color:{VIO};font-size:110px}}
.stk{{position:absolute;font-size:120px;font-style:normal;filter:drop-shadow(0 10px 16px rgba(0,0,0,.35))}}
.pnl{{position:absolute;left:0;top:0;width:1080px;height:{PANEL_H}px;overflow:hidden;background:radial-gradient(circle at 50% 0%,#241a3d,{DK} 70%);border-bottom:10px solid {VIO}}}
.glow{{position:absolute;left:290px;top:-260px;width:500px;height:500px;border-radius:50%;background:{VIO};opacity:.3;filter:blur(120px)}}
.sc{{position:absolute;inset:0;opacity:0}} .brand{{position:absolute;left:0;right:0;top:50px;display:flex;justify-content:center;align-items:center;gap:18px}}
.card{{position:absolute;left:250px;right:250px;top:170px;height:520px;background:#141418;border:4px solid #33303f;border-radius:40px;text-align:center;box-shadow:0 30px 70px rgba(0,0,0,.6)}}
.pl{{margin-top:40px;font-size:44px;letter-spacing:.12em;color:#c9c2e8}} .pr{{position:relative;height:250px;margin-top:20px}}
.old{{position:absolute;left:0;right:0;font-size:220px;color:#777;line-height:1}} .old::after{{content:"";position:absolute;left:150px;right:150px;top:110px;height:16px;background:{RED};border-radius:8px;transform:rotate(-12deg) scaleX(var(--s,0));transform-origin:left}}
.new{{position:absolute;left:0;right:0;font-size:240px;color:#fff;line-height:1;text-shadow:0 0 60px rgba(139,92,246,.8)}} .fm{{font-family:PM;font-size:40px;color:#c9c2e8}}
.off{{position:absolute;right:-60px;top:-40px;font-size:60px;background:{YEL};color:#111;padding:10px 26px;border-radius:20px;transform:rotate(10deg)}}
.calp{{position:absolute;left:90px;top:90px;width:400px;height:560px;background:#fff;border-radius:30px;overflow:hidden;color:#111;text-align:center;box-shadow:0 30px 60px rgba(0,0,0,.6);transform:rotate(-4deg)}}
.ct{{background:{VIO};color:#fff;font-size:54px;padding:20px 0}} .cd{{font-size:300px;line-height:1.15}} .cw{{font-family:PB;font-size:40px;color:{RED}}}
.side{{position:absolute;left:560px;right:40px;top:200px}} .s1{{font-size:60px}} .s1 s{{color:{RED}}}
.tm{{margin-top:50px;font-size:58px;background:{YEL};color:#111;padding:14px 24px;border-radius:20px;display:inline-block;transform:rotate(3deg)}}
.hd{{position:absolute;left:0;right:0;top:50px;text-align:center;font-size:58px}} .hd b{{color:{VIO}}}
.ck{{position:absolute;left:110px;right:110px;height:130px;border-radius:30px;background:rgba(255,255,255,.07);border:3px solid rgba(255,255,255,.15);display:flex;align-items:center;justify-content:space-between;padding:0 40px;font-size:52px}}
#c1{{top:170px}} #c2{{top:330px}} #c3{{top:490px}} .ck em{{font-style:normal;width:80px;height:80px;border-radius:50%;background:{GRN};display:flex;align-items:center;justify-content:center}}
.wv{{position:absolute;left:60px;right:60px;height:190px;display:flex;align-items:center;gap:24px}} .wv:nth-of-type(2){{top:150px}} .wv:nth-of-type(4){{top:420px}}
.wl{{width:220px;font-size:42px}} .wf{{flex:1;height:170px;display:flex;align-items:center;gap:8px}} .wb{{flex:1;background:#fff;border-radius:8px;font-style:normal;transform-origin:center}} .wb.c{{background:{VIO}}}
.arr{{position:absolute;left:0;right:0;top:345px;text-align:center;font-size:52px;color:{YEL}}} .tk{{position:absolute;left:0;right:0;top:640px;text-align:center;font-size:56px;color:{GRN}}}
.mos{{position:absolute;left:80px;right:80px;top:140px;display:flex;align-items:center;justify-content:center;gap:40px}} .mo{{width:340px;padding:30px;border-radius:30px;background:rgba(255,255,255,.07);border:3px solid rgba(255,255,255,.15);text-align:center}}
.mo b{{display:block;font-size:40px;color:#c9c2e8}} .mo span{{font-size:96px}} .m2{{border-color:{RED}}} .ar2{{font-size:90px}}
.cbtn{{position:absolute;left:0;right:0;top:600px;margin:auto;width:max-content;font-size:60px;background:{RED};padding:20px 50px;border-radius:30px}}
.cf{{position:absolute;width:20px;height:32px;border-radius:4px}}
.row2{{position:absolute;left:0;right:0;top:120px;display:flex;justify-content:center;gap:80px}} .sv{{width:300px;height:300px;border-radius:50px;background:rgba(255,255,255,.08);border:4px solid {VIO};display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:140px}} .sv b{{font-size:50px}}
.yt{{position:absolute;left:0;right:0;top:500px;text-align:center;font-size:50px;line-height:1.25}} .yt b{{color:{RED};font-size:64px}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.leak{{position:absolute;left:-400px;top:-300px;width:700px;height:2600px;background:linear-gradient(90deg,transparent,rgba(139,92,246,.55),rgba(255,211,77,.3),transparent);filter:blur(34px);transform:rotate(16deg)}}
.sh{{position:absolute;left:0;right:0;height:960px;background:{DK}}} .sh.t{{top:0;border-bottom:6px solid {VIO}}} .sh.b{{top:960px;border-top:6px solid {VIO}}}
.shl{{position:absolute;left:0;right:0;top:860px;display:flex;justify-content:center}} .shl .el{{width:200px;height:200px}}'''
def sc(k): s, e = S[k]; return f'tl.set("#{k}",{{opacity:1}},{s:.3f}).set("#{k}",{{opacity:0}},{e:.3f});'
cx, cy, cr = ",".join(map(str, CX)), ",".join(map(str, CY)), ",".join(map(str, CR))
js = "\n".join(sc(k) for k in S) + f'''
tl.fromTo("#shl",{{scale:1.6,rotation:-90}},{{scale:0.3,rotation:120,opacity:0,duration:0.16,ease:"power2.in"}},0)
  .to("#sht",{{y:-980,duration:0.2,ease:"power3.in"}},0.08).to("#shb",{{y:980,duration:0.2,ease:"power3.in"}},0.08).set("#f0",{{opacity:0.7}},0.2).to("#f0",{{opacity:0,duration:0.1}},0.21);
tl.to("#hz",{{scale:1.04,duration:{SPLIT[0]-0.4:.3f},ease:"sine.inOut"}},0).to("#hz",{{opacity:0,y:-30,duration:0.2}},{SPLIT[0]-0.15:.3f});
tl.from(["#k_c","#k_d","#k_a","#k_b"],{{scale:0,rotation:-30,duration:0.3,stagger:0.25,ease:"back.out(2.5)"}},{T("CLONE"):.3f}).to(["#k_a","#k_b","#k_c","#k_d"],{{scale:0,duration:0.15}},{SPLIT[0]-0.15:.3f});
tl.fromTo("#tz",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:{TOTAL-SPEECH_END-0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});
tl.fromTo("#pnl",{{y:-{PANEL_H+20}}},{{y:0,duration:0.25,ease:"power3.out"}},{SPLIT[0]:.3f}).to("#pnl",{{y:-{PANEL_H+20},duration:0.22,ease:"power3.in"}},{SPLIT[1]-0.22:.3f});
tl.from("#card",{{y:600,duration:0.4,ease:"back.out(1.4)"}},{S["price"][0] + 0.1:.3f}).set("#new",{{opacity:0}},0)
  .fromTo("#old",{{"--s":0}},{{"--s":1,duration:0.25}},{T("$1", 2) - 0.25:.3f}).to("#old",{{x:190,y:-60,scale:0.4,duration:0.3}},{T("$1", 2):.3f})
  .fromTo("#new",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,y:40,duration:0.25,ease:"power4.in"}},{T("$1", 2):.3f}).fromTo("#off",{{scale:0,rotation:-40}},{{scale:1,rotation:10,duration:0.3,ease:"back.out(3)"}},{T("FIRST"):.3f});
tl.from("#calp",{{y:-800,rotation:-30,duration:0.4,ease:"back.out(1.4)"}},{S["date"][0]:.3f}).from(".s1",{{x:500,opacity:0,duration:0.3}},{S["date"][0] + 0.15:.3f})
  .fromTo("#tm",{{scale:0,rotation:-20}},{{scale:1,rotation:3,duration:0.3,ease:"back.out(2.5)"}},{T("ENDS"):.3f}).to("#calp",{{rotation:4,duration:0.08,yoyo:true,repeat:5}},{T("8"):.3f});
tl.from("#feat .hd",{{y:-100,opacity:0,duration:0.3}},{S["feat"][0] + 0.05:.3f});
[["c1","{T("30") - 0.1}"],["c2","{T("COMMERCIAL") - 0.1}"],["c3","{T("INSTANT") - 0.1}"]].forEach(([id,t])=>tl.from("#"+id,{{x:-1100,duration:0.3,ease:"power3.out"}},+t).from("#"+id+" em",{{scale:0,duration:0.25,ease:"back.out(3)"}},+t+0.25));
tl.from("#clone .hd",{{y:-100,opacity:0,duration:0.3}},{S["clone"][0] + 0.05:.3f});
const wb1=document.querySelectorAll("#wf1 .wb"), wb2=document.querySelectorAll("#wf2 .wb");
tl.fromTo(wb1,{{scaleY:0.1}},{{scaleY:1,duration:0.25,stagger:0.02,ease:"power2.out"}},{T("MINUTE") - 0.1:.3f});
tl.to(wb1,{{scaleY:0.35,duration:0.18,yoyo:true,repeat:9,stagger:{{each:0.03,from:"random"}}}},{T("MINUTE") + 0.6:.3f});
tl.from("#arr",{{y:-40,opacity:0,duration:0.25}},{T("AND", 2) - 0.1:.3f}).fromTo(wb2,{{scaleY:0.1}},{{scaleY:1,duration:0.25,stagger:0.02,ease:"power2.out"}},{T("TALKS") - 0.15:.3f})
  .to(wb2,{{scaleY:0.35,duration:0.18,yoyo:true,repeat:7,stagger:{{each:0.03,from:"random"}}}},{T("TALKS") + 0.5:.3f}).from("#tk",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{T("EXACTLY"):.3f});
tl.from("#renew .hd",{{y:-100,opacity:0,duration:0.3}},{S["renew"][0] + 0.05:.3f}).from(".mo",{{y:300,opacity:0,duration:0.35,stagger:0.25}},{T("AUTO") - 0.2:.3f})
  .to("#m2",{{scale:1.08,duration:0.15,yoyo:true,repeat:3}},{T("$6", 2):.3f}).from("#cb",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{T("CANCEL") - 0.1:.3f}).to("#cb",{{scale:0.92,duration:0.08,yoyo:true,repeat:1}},{T("MONTH", 2):.3f});
const CX=[{cx}],CY=[{cy}],CR=[{cr}];
tl.fromTo("#renew .cf",{{x:0,y:0,opacity:1}},{{x:(i)=>CX[i],y:(i)=>CY[i],rotation:(i)=>CR[i],opacity:0,duration:1.3,ease:"power2.out"}},{T("2") + 0.1:.3f});
tl.from("#sv",{{scale:0,rotation:-20,duration:0.3,ease:"back.out(2.5)"}},{T("SAVE"):.3f}).from("#sd",{{scale:0,rotation:20,duration:0.3,ease:"back.out(2.5)"}},{T("SEND"):.3f})
  .from("#yt",{{y:80,opacity:0,duration:0.3}},{T("FRIEND") - 0.2:.3f}).to("#sd",{{x:600,y:-300,rotation:30,opacity:0,duration:0.5,ease:"power2.in"}},{T("YOUTUBE") + 0.3:.3f});
{"".join(f'tl.set("#fl{i}",{{opacity:0.5}},{t:.3f}).to("#fl{i}",{{opacity:0,duration:0.15}},{t + 0.02:.3f}).fromTo("#lk{i}",{{x:-300}},{{x:1500,duration:0.5,ease:"power1.inOut"}},{t - 0.12:.3f});' for i, t in enumerate(CUTS))}'''
body = (clip("panel", *SPLIT, pnl, 5) + clip("hook", 0, SPLIT[0] + 0.05, hook + side, 30) + clip("tail", SPEECH_END, TOTAL, hook.replace('id="hz"', 'id="tz"'), 30) +
        clip("intro", 0, 0.32, f'<div class="sh t" id="sht"></div><div class="sh b" id="shb"></div><div class="shl" id="shl">{EL}</div><div class="flash" id="f0"></div>', 80) +
        "".join(clip(f"tr{i}", t - 0.12, t + 0.4, f'<div class="flash" id="fl{i}"></div><div class="leak" id="lk{i}"></div>', 60) for i, t in enumerate(CUTS)))
doc = (f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body>'
       f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">{body}</div>'
       f'<script>const tl = gsap.timeline({{paused:true}});\n{js}\nwindow.__timelines["main"] = tl; tl.seek(0);</script></body></html>')
open("hf/index.html", "w").write(doc)
json.dump({"split": SPLIT, "scenes": S, "cuts": CUTS, "slide": SLIDE, "panel_h": PANEL_H, "speech_end": SPEECH_END, "total": TOTAL}, open("events.json", "w"), indent=1)
print("ok", SPLIT, "slide", SLIDE)
