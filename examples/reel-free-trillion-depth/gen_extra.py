# ===== EXTRA ASSETS (v2): more images + animation. Appended into back_* / front_* before render.
import random
rnd = random.Random(7)
GRN, ORG, CYN = "#3DFF8A", "#FF8A1E", "#3BE8FF"
Tn = lambda w, n=1: T(w, n)

# ---------- BACK (behind the person, whole reel thanks to full matte)
bokeh = "".join(f'<div class="bk" style="left:{rnd.randint(0,1040)}px;top:{rnd.randint(80,1500)}px;width:{(d:=rnd.randint(14,60))}px;height:{d}px;'
                f'background:{rnd.choice([YEL,ORG,CREAM,RED])};opacity:{rnd.uniform(.15,.4):.2f}"></div>' for _ in range(34))
cols = "".join(f'<div class="bc" style="left:{x}px">' + "<br>".join(rnd.choice("01") for _ in range(40)) + '</div>' for x in range(30, 1080, 74))
# neural net behind TRILLION
L = [[(120 + i * 210, 160 + j * (620 // (n - 1))) for j in range(n)] for i, n in enumerate([4, 6, 6, 6, 4])]
edges = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for l1, l2 in zip(L, L[1:]) for a in l1 for b in l2)
nodes = "".join(f'<circle class="nn" cx="{x}" cy="{y}" r="16"/>' for l in L for (x, y) in l)
net = f'<svg class="net" id="net" width="1080" height="900" viewBox="0 0 1080 900"><g stroke="{YEL}" stroke-opacity=".28" stroke-width="2">{edges}</g><g fill="{YEL}">{nodes}</g></svg>'
def rack(x, flip=""):
    u = "".join(f'<div class="ru"><i class="led" style="animation-delay:{rnd.random():.2f}s"></i><i class="led g"></i><span></span></div>' for _ in range(9))
    return f'<div class="rack" style="left:{x}px">{u}</div>'
back_css += f'''
.bk{{position:absolute;border-radius:50%;filter:blur(6px)}}
.bc{{position:absolute;top:-200px;font-family:PM;font-size:26px;line-height:34px;color:{YEL};opacity:.12;text-align:center}}
.net{{position:absolute;left:0;top:120px}}
.chonk{{position:absolute;left:0;right:0;top:560px;text-align:center;font-size:250px;line-height:.86;letter-spacing:-.04em;color:{ORG};text-shadow:0 10px 50px rgba(0,0,0,.4)}}
.zero{{position:absolute;left:0;right:0;top:420px;text-align:center;font-size:420px;line-height:.86;color:{GRN};text-shadow:0 0 80px rgba(61,255,138,.45)}}
.rack{{position:absolute;top:640px;width:250px;padding:14px;background:#15161b;border:4px solid #2b2d36;border-radius:16px;box-shadow:0 0 60px rgba(255,61,61,.25)}}
.ru{{height:62px;margin:8px 0;background:#22242c;border-radius:8px;display:flex;align-items:center;padding:0 14px;gap:10px}}
.ru span{{flex:1;height:10px;background:#31343f;border-radius:5px}}
.led{{width:14px;height:14px;border-radius:50%;background:{RED};box-shadow:0 0 12px {RED};animation:bl .5s steps(2) infinite}} .led.g{{background:{GRN};box-shadow:0 0 12px {GRN}}}
@keyframes bl{{50%{{opacity:.2}}}}
.halo{{position:absolute;left:140px;top:380px;width:800px;height:800px;border-radius:50%;
 background:conic-gradient(#ff3d3d,#ffd34d,#3dff8a,#3be8ff,#a64dff,#ff3d3d);filter:blur(40px);opacity:.75}}
.warn{{position:absolute;left:-200px;right:-200px;top:0;bottom:0;background:radial-gradient(circle at 50% 50%,rgba(255,61,61,.55),transparent 60%)}}'''
back_body = (clip("bokeh", 0, TOTAL, f'<div id="bkw">{bokeh}</div>', 1) + clip("bin", 0, TOTAL, f'<div id="bnc">{cols}</div>', 2) + back_body +
             clip("chonkb", Tn("CHONK") - 0.3, T("TRILLION") - 0.15, '<div class="chonk" id="ck">LE CHONK</div>', 12) +
             clip("netb", B["tril"][0], B["tril"][1], net, 5) +
             clip("zerob", Tn("ANYONE") - 0.05, T("CATCH") - 0.4, '<div class="zero" id="zr">₹0</div>', 12) +
             clip("warnb", T("CATCH") - 0.35, T("YOU'D"), '<div class="warn" id="wn"></div>', 5) +
             clip("rackb", T("YOU'D"), B["gb"][1], rack(-20) + rack(850), 6) +
             clip("halob", T("TAG") - 0.1, SPEECH_END, '<div class="halo" id="hl"></div>', 6))
back_js += f'''
tl.to("#bkw .bk",{{y:"-=160",x:"+=30",duration:{TOTAL:.3f},ease:"none",stagger:{{each:0.0,from:"random"}}}},0);
tl.fromTo("#bnc",{{y:0}},{{y:420,duration:{TOTAL:.3f},ease:"none"}},0);
tl.from("#ck",{{x:-1100,duration:0.35,ease:"power4.out"}},{Tn("CHONK") - 0.3:.3f}).to("#ck",{{x:1100,duration:0.25,ease:"power3.in"}},{T("TRILLION") - 0.4:.3f});
tl.from("#net line",{{opacity:0,duration:0.5,stagger:0.004}},{B["tril"][0]:.3f}).from("#net .nn",{{scale:0,transformOrigin:"center",duration:0.3,stagger:0.02,ease:"back.out(3)"}},{B["tril"][0]:.3f});
tl.from("#zr",{{scale:0.3,opacity:0,rotation:-12,duration:0.35,ease:"back.out(2)"}},{Tn("ANYONE") - 0.05:.3f}).to("#zr",{{scale:1.1,duration:2,ease:"sine.inOut"}},{Tn("ANYONE") + 0.3:.3f});
tl.fromTo("#wn",{{opacity:0}},{{opacity:1,duration:0.12,repeat:5,yoyo:true}},{T("CATCH") - 0.35:.3f});
tl.from(".rack",{{y:600,duration:0.45,ease:"power3.out",stagger:0.1}},{T("YOU'D"):.3f});
tl.from("#hl",{{scale:0.3,opacity:0,duration:0.4,ease:"power3.out"}},{T("TAG") - 0.1:.3f}).to("#hl",{{rotation:540,duration:{SPEECH_END - T("TAG"):.3f},ease:"none"}},{T("TAG") - 0.1:.3f});'''

# ---------- FRONT (stickers, icons, bursts; kept off the face: top band 200-740, side edges, bottom corners)
def stk(id_, txt, x, y, sz=130, cls="st"):
    return f'<div class="{cls}" id="{id_}" style="left:{x}px;top:{y}px;font-size:{sz}px">{txt}</div>'
conf = "".join(f'<i class="cf" style="left:540px;top:520px;background:{rnd.choice([YEL,GRN,RED,CYN,CREAM])}"></i>' for _ in range(40))
ats = "".join(f'<div class="at" style="left:{x}px;top:{y}px">{t}</div>' for x, y, t in ((40, 1640, "@rahul 🎮"), (700, 1700, "@priya 💻"), (40, 1760, "@your_gamer_bro")))
front_css += f'''
.st{{position:absolute;line-height:1;filter:drop-shadow(0 12px 18px rgba(0,0,0,.45))}}
.chip{{position:absolute;font-size:40px;background:{CREAM};color:#111;padding:8px 24px;border-radius:99px}}
.cnt{{position:absolute;left:0;right:0;top:215px;text-align:center;font-size:66px;color:{YEL};font-variant-numeric:tabular-nums;text-shadow:0 6px 24px rgba(0,0,0,.6)}}
.cf{{position:absolute;width:18px;height:30px;border-radius:4px}}
.tape{{position:absolute;left:-100px;width:1300px;height:86px;background:repeating-linear-gradient(45deg,#FFD34D 0 50px,#111 50px 100px);
 display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.5)}}
.tape b{{background:#111;color:{YEL};font-size:46px;padding:0 24px;letter-spacing:.08em}}
.at{{position:absolute;font-family:PB;font-size:44px;background:rgba(10,10,12,.85);border:3px solid {CYN};padding:10px 26px;border-radius:99px;white-space:nowrap}}
.leak{{position:absolute;left:-300px;top:-200px;width:700px;height:2400px;background:linear-gradient(90deg,transparent,rgba(255,170,60,.55),rgba(255,80,60,.35),transparent);filter:blur(30px);transform:rotate(14deg)}}
.sv{{position:absolute;left:330px;top:640px;font-size:44px;background:{CREAM};color:#111;padding:14px 26px;border-radius:22px}}'''
leaks = [Tn("MISTRAL") - 0.15, B["tril"][0] - 0.1, Tn("ANYONE") - 0.15, T("YOU'D") - 0.1, T("TAG") - 0.15]
front_body += (
    clip("s_open", 0.0, Tn("MISTRAL") - 0.12, stk("s1", "🤖", 40, 1420) + stk("s2", "💸", 880, 1440) + stk("s3", "✨", 60, 560, 90) + stk("s4", "🆓", 900, 520, 110), 20) +
    clip("s_name", Tn("MISTRAL") - 0.05, T("TRILLION") - 0.15, '<div class="chip" id="fr" style="left:80px;top:470px">🇫🇷 Made in Paris</div>' + stk("s5", "🧠", 880, 460, 120), 20) +
    clip("s_cnt", B["tril"][0], B["tril"][1], '<div class="cnt"><span id="cn">0</span> params</div>', 20) +
    clip("s_biz", Tn("ANYONE") - 0.05, T("CATCH") - 0.4, conf + stk("s6", "💼", 50, 1430, 120) + stk("s7", "🏢", 890, 1430, 120) + stk("s8", "🎉", 870, 500, 110), 20) +
    clip("s_tape", T("CATCH") - 0.35, T("YOU'D") + 0.4, '<div class="tape" id="tp1" style="top:200px"><b>⚠ CATCH ⚠</b></div><div class="tape" id="tp2" style="top:640px;transform:rotate(-4deg)"><b>⚠ WARNING ⚠</b></div>', 30) +
    clip("s_lap", T("LAPTOP") - 0.1, T("TAG") - 0.1, stk("s9", "💻", 860, 520, 130) + stk("s10", "🔥", 905, 445, 80) + stk("s11", "😰", 60, 520, 110), 20) +
    clip("s_tag", T("TAG") - 0.05, SPEECH_END, ats + stk("s12", "🎮", 40, 480, 120) + stk("s13", "🕹️", 900, 480, 110) + '<div class="sv" id="sv">🔖 Save for later</div>', 20) +
    "".join(clip(f"lk{i}", t, t + 0.45, f'<div class="leak" id="lk{i}x"></div>', 70) for i, t in enumerate(leaks)))
front_js += f'''
tl.from(["#s1","#s2"],{{scale:0,rotation:-30,duration:0.35,ease:"back.out(2.5)",stagger:0.2}},0.5).from(["#s3","#s4"],{{scale:0,duration:0.3,ease:"back.out(3)",stagger:0.25}},{Tn("FREE"):.3f})
  .to(["#s1","#s2","#s3","#s4"],{{y:"-=24",duration:0.6,yoyo:true,repeat:5,ease:"sine.inOut"}},1.0)
  .to(["#s1","#s2","#s3","#s4"],{{scale:0,duration:0.15}},{Tn("MISTRAL") - 0.3:.3f});
tl.from("#fr",{{x:-500,duration:0.35,ease:"power3.out"}},{Tn("MISTRAL") + 0.25:.3f}).from("#s5",{{scale:0,rotation:40,duration:0.35,ease:"back.out(2.5)"}},{Tn("CHONK") - 0.1:.3f});
const CX={[rnd.randint(-520,520) for _ in range(40)]},CY={[rnd.randint(-320,900) for _ in range(40)]},CR={[rnd.randint(-720,720) for _ in range(40)]};
const cn={{v:0}}; tl.to(cn,{{v:1e12,duration:0.8,ease:"power2.out",onUpdate:()=>{{document.getElementById("cn").textContent=Math.round(cn.v).toLocaleString("en-US")}}}},{B["tril"][0] + 0.05:.3f});
tl.fromTo(".cf",{{x:0,y:0,rotation:0,opacity:1}},{{x:(i)=>CX[i],y:(i)=>CY[i],rotation:(i)=>CR[i],opacity:0,duration:1.6,ease:"power2.out"}},{Tn("BUSINESS") - 0.05:.3f});
tl.from(["#s6","#s7","#s8"],{{scale:0,y:60,duration:0.35,ease:"back.out(2.5)",stagger:0.15}},{Tn("ANYONE") + 0.2:.3f});
tl.from("#tp1",{{x:-1300,duration:0.25,ease:"power4.out"}},{T("CATCH") - 0.35:.3f}).from("#tp2",{{x:1300,duration:0.25,ease:"power4.out"}},{T("CATCH") - 0.25:.3f})
  .to(["#tp1","#tp2"],{{opacity:0,duration:0.2}},{T("YOU'D") + 0.2:.3f});
tl.from("#s9",{{scale:0,duration:0.3,ease:"back.out(3)"}},{T("LAPTOP") - 0.1:.3f}).fromTo("#s9",{{x:-8}},{{x:8,duration:0.05,repeat:15,yoyo:true}},{T("16"):.3f})
  .from("#s10",{{scale:0,y:30,duration:0.25}},{T("16") + 0.05:.3f}).to("#s10",{{y:-20,scale:1.2,duration:0.3,repeat:3,yoyo:true}},{T("16") + 0.3:.3f})
  .from("#s11",{{scale:0,rotation:-30,duration:0.3,ease:"back.out(2.5)"}},{T("16"):.3f});
tl.fromTo(".at",{{y:0,opacity:0}},{{y:-260,opacity:1,duration:0.7,ease:"power3.out",stagger:0.25}},{T("TAG") + 0.1:.3f});
tl.from(["#s12","#s13"],{{scale:0,rotation:20,duration:0.3,ease:"back.out(2.5)",stagger:0.12}},{T("TAG"):.3f}).to(["#s12","#s13"],{{rotation:-12,duration:0.18,yoyo:true,repeat:7}},{T("TAG") + 0.4:.3f})
  .from("#sv",{{y:-200,opacity:0,duration:0.35,ease:"power3.out"}},{T("TAG") + 0.6:.3f});
{"".join(f'tl.fromTo("#lk{i}x",{{x:-200,opacity:0}},{{x:1400,opacity:1,duration:0.45,ease:"power1.inOut"}},{t:.3f});' for i, t in enumerate(leaks))}'''
