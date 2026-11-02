"""NN4 'Claude's company may go public' — VIRTUAL STUDIO edit. Real background replaced (person matte over the full reel):
hf_back = opaque newsroom set (video wall with per-beat scenes, rising chart, ticker band, bokeh);
hf_front = breaking pill, floating reactions, flash/leak transitions, tap-to-follow. Speaker shifted 150px down."""
import json, sys, os, random
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL
def T(w, n=1): return round(word_time(w, n)[0], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')
r = random.Random(16)
COR, CRM, INK, GRN, RED, GLD = "#E8875F", "#F4EEE3", "#120C0B", "#3DFF8A", "#FF4D4D", "#FFD34D"
SC = {"s0": (0.0, T("TWO") - 0.12), "s1": (T("TWO") - 0.12, T("ANTHROPIC") - 0.1), "s2": (T("ANTHROPIC") - 0.1, T("REPORTS") - 0.08),
      "s3": (T("REPORTS") - 0.08, T("ONE") - 0.1), "s4": (T("ONE") - 0.1, T("FOLLOW") - 0.08), "s5": (T("FOLLOW") - 0.08, SPEECH_END)}
CUTS = [SC[k][0] for k in ("s1", "s2", "s3", "s4", "s5")]
HEAD = '''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script><style>
@font-face{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)} @font-face{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}
@font-face{font-family:MO;src:url(assets/fonts/DejaVuSansMono.ttf)}
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}
#root{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff} .full{position:absolute;left:0;top:0;width:1080px;height:1920px}
'''
def page(css, body, js):
    return (HEAD + css + f'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">'
            f'{body}</div><script>const tl = gsap.timeline({{paused:true}});\n{js}\nwindow.__timelines["main"] = tl; tl.seek(0);</script></body></html>')

# ================= BACK: the studio set
bokeh = "".join(f'<i class="bk" style="left:{r.randint(0,1060)}px;top:{r.randint(60,1700)}px;width:{(d:=r.randint(10,46))}px;height:{d}px;opacity:{r.uniform(.12,.4):.2f};background:{r.choice([COR,CRM,GLD])}"></i>' for _ in range(36))
pts = []; y = 300
for i in range(19): y = max(40, min(330, y + r.randint(-60, 25) - 8)); pts.append(f"{i*60},{y}")
chart = f'<svg class="chart" width="1080" height="380" viewBox="0 0 1080 380"><polyline id="cl" points="{" ".join(pts)}" fill="none" stroke="{GRN}" stroke-width="8" stroke-linejoin="round" stroke-dasharray="2600" stroke-dashoffset="2600"/></svg>'
tick = " · ".join(["🔴 LIVE", "ANT ▲ NASDAQ", "CLAUDE MAKER GOING PUBLIC", "S-1 FILED · OCT 26", "BIGGEST AI IPO EVER?", "WEEK OF NOV 16"]) + " · "
cal = "".join(f'<b class="{"hi" if 15 <= d <= 21 else ""}{" d16" if d == 16 else ""}">{d}</b>' for d in range(1, 31))
bars = [("SpaceX · 2026", 86, "#9aa3b5", "$86B"), ("Saudi Aramco · 2019", 29, "#6b7385", "$29B"), ("Alibaba · 2014", 25, "#6b7385", "$25B")]
barh = "".join(f'<div class="br"><span class="bn">{n}</span><div class="bt"><div class="bf" style="width:{v/100*100:.0f}%;background:{c}"></div></div><em>{l}</em></div>' for n, v, c, l in bars)
wall = f'''<div class="wall" id="wall"><div class="scan"></div>
 <div class="sc" id="s0"><div class="k0">THE COMPANY BEHIND <u>CLAUDE</u></div><div class="ipo" id="ipo">IPO</div><div class="bell" id="bell">🔔</div><div class="k1" id="gp">GOING PUBLIC?</div></div>
 <div class="sc" id="s1"><div class="k0">COUNTDOWN</div><div class="flip"><div class="fd" id="fd">14</div><div class="fu">DAYS</div></div><div class="k1">≈ 2 WEEKS</div></div>
 <div class="sc" id="s2"><div class="doc" id="doc"><div class="dh">UNITED STATES SECURITIES AND EXCHANGE COMMISSION</div><div class="dt">FORM S-1</div><div class="dl"></div><div class="dl" style="width:70%"></div><div class="dl" style="width:85%"></div><div class="dn">Anthropic, PBC · Nasdaq: ANT</div></div>
   <div class="stmp" id="stmp">FILED · OCT 26</div></div>
 <div class="sc" id="s3"><div class="cal"><div class="ch">NOVEMBER 2026</div><div class="cg">{"".join(f"<i>{d}</i>" for d in "SMTWTFS")}{cal}</div></div><div class="wk" id="wk">👀 WEEK OF NOV 16</div></div>
 <div class="sc" id="s4"><div class="k0">BIGGEST IPOs EVER (RAISED)</div><div class="race"><div class="br me"><span class="bn">Anthropic · 2026?</span><div class="bt"><div class="bf" id="af" style="width:100%;background:{COR}"></div></div><em id="al">$75–100B?</em></div>{barh}</div></div>
 <div class="sc" id="s5"><div class="tk" id="tk"><span>ANT</span><em>▲</em></div><div class="fol" id="fol">FOLLOW 🔔</div><div class="k1">I’LL POST THE DAY IT HAPPENS</div></div>
</div>'''
back_css = f'''
.bg{{position:absolute;inset:-60px;background:radial-gradient(ellipse at 50% 28%,#3a1d12 0%,#1b0f0c 45%,#09080a 100%)}}
.wg{{position:absolute;inset:0;background-image:linear-gradient(rgba(232,135,95,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(232,135,95,.07) 2px,transparent 2px);background-size:90px 90px;
 -webkit-mask-image:radial-gradient(ellipse at 50% 40%,#000 30%,transparent 75%)}}
.bk{{position:absolute;border-radius:50%;filter:blur(7px)}}
.chart{{position:absolute;left:0;top:760px;filter:drop-shadow(0 0 18px rgba(61,255,138,.7));opacity:.55}}
.tband{{position:absolute;left:0;right:0;top:1190px;height:84px;background:{COR};overflow:hidden;box-shadow:0 0 60px rgba(232,135,95,.5)}}
.tband div{{position:absolute;left:0;top:14px;white-space:nowrap;font-size:42px;color:{INK}}}
.wall{{position:absolute;left:40px;right:40px;top:140px;height:440px;border-radius:34px;overflow:hidden;background:linear-gradient(160deg,#25140f,#120b0a);
 border:4px solid rgba(244,238,227,.35);box-shadow:0 0 80px rgba(232,135,95,.35),inset 0 0 80px rgba(0,0,0,.6)}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 2px,transparent 2px 6px);z-index:5}}
.sc{{position:absolute;inset:0;opacity:0;text-align:center}}
.k0{{position:absolute;left:0;right:0;top:24px;font-family:PM;font-size:36px;letter-spacing:.12em;color:{CRM};opacity:.85}} .k0 u{{color:{COR};text-decoration:none}}
.k1{{position:absolute;left:0;right:0;top:318px;font-size:56px;color:{CRM}}}
.ipo{{position:absolute;left:0;right:0;top:62px;font-size:250px;line-height:1;color:{COR};letter-spacing:-.03em;text-shadow:0 0 70px rgba(232,135,95,.55)}}
.bell{{position:absolute;right:70px;top:100px;font-size:120px;transform-origin:50% 10%}}
.flip{{position:absolute;left:0;right:0;top:80px;display:flex;justify-content:center;align-items:flex-end;gap:24px}}
.fd{{font-family:MO;font-size:180px;line-height:1;background:#0b0807;border:4px solid #3a2a24;border-radius:24px;padding:0 30px;color:{GLD}}} .fu{{font-size:80px;color:{CRM};margin-bottom:20px}}
.doc{{position:absolute;left:250px;top:30px;width:580px;height:460px;background:{CRM};border-radius:10px;color:#222;padding:30px;transform:rotate(-3deg);text-align:left;box-shadow:0 30px 60px rgba(0,0,0,.6)}}
.dh{{font-family:PM;font-size:19px;letter-spacing:.06em;text-align:center}} .dt{{font-size:74px;text-align:center;margin:18px 0}} .dl{{height:16px;background:#cfc7b8;border-radius:8px;margin:16px 0;width:95%}}
.dn{{font-family:PM;font-size:28px;margin-top:30px;text-align:center}}
.stmp{{position:absolute;left:0;right:0;top:220px;margin:auto;width:max-content;font-size:72px;color:{RED};border:10px solid {RED};padding:0 34px;border-radius:20px;transform:rotate(-9deg);background:rgba(18,12,11,.25)}}
.cal{{position:absolute;left:200px;right:200px;top:18px}} .ch{{font-size:36px;color:{COR};margin-bottom:10px}}
.cg{{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;font-size:23px}} .cg i{{font-style:normal;font-family:PM;color:#a99}}
.cg b{{padding:2px 0;border-radius:10px;background:rgba(255,255,255,.05);color:{CRM}}} .cg b:first-of-type{{grid-column:1}} .cg b.hi{{background:rgba(232,135,95,.35)}}
.ring{{position:absolute;left:285px;top:252px;width:110px;height:72px;border:7px solid {GLD};border-radius:40px;opacity:0}}
.wk{{position:absolute;left:0;right:0;top:340px;font-size:50px;color:{GLD}}}
.race{{position:absolute;left:60px;right:60px;top:80px}} .br{{display:flex;align-items:center;gap:20px;margin:14px 0;font-size:34px}}
.bn{{width:360px;text-align:left;font-family:PM;font-size:30px;white-space:nowrap;color:{CRM}}} .bt{{flex:1;height:58px;background:rgba(255,255,255,.07);border-radius:14px;overflow:hidden}} .bf{{height:100%;border-radius:14px;transform-origin:left}}
.br em{{width:190px;font-style:normal;text-align:right;font-size:30px;white-space:nowrap}} .me .bn{{color:{COR};font-family:PB}} .me em{{color:{COR}}}
.tk{{position:absolute;left:0;right:0;top:14px;font-size:190px;line-height:1;color:{GRN};text-shadow:0 0 60px rgba(61,255,138,.5)}} .tk em{{font-style:normal;font-size:150px}}
.fol{{position:absolute;left:0;right:0;top:232px;margin:auto;width:max-content;font-size:64px;background:{COR};color:{INK};padding:12px 46px;border-radius:99px}}
.fol + .k1{{top:345px;font-size:36px}}'''
def show(k): s, e = SC[k]; return f'tl.set("#{k}",{{opacity:1}},{s:.3f}).set("#{k}",{{opacity:0}},{e:.3f});'
back_body = (clip("set", 0, TOTAL, f'<div class="bg" id="bg"></div><div class="wg"></div><div id="bkw">{bokeh}</div>{chart}'
                  f'<div class="tband"><div id="tkr">{tick * 4}</div></div>{wall}', 1))
back_js = "\n".join(show(k) for k in SC) + f'''
tl.set("#s0",{{opacity:1}},{SPEECH_END:.3f});
tl.fromTo("#bg",{{scale:1}},{{scale:1.08,duration:{TOTAL:.3f},ease:"none"}},0);
tl.to("#bkw .bk",{{y:"-=140",duration:{TOTAL:.3f},ease:"none"}},0);
tl.fromTo("#tkr",{{x:0}},{{x:-2600,duration:{TOTAL:.3f},ease:"none"}},0);
tl.to("#cl",{{strokeDashoffset:0,duration:{TOTAL - 1:.3f},ease:"power1.inOut"}},0.2);
tl.fromTo("#ipo",{{scale:1.15}},{{scale:1,duration:0.35,ease:"power3.out"}},0).to("#ipo",{{scale:1.06,duration:3,ease:"sine.inOut"}},0.35);
tl.fromTo("#bell",{{rotation:-18}},{{rotation:18,duration:0.12,repeat:9,yoyo:true,ease:"sine.inOut"}},{T("PUBLIC") - 0.2:.3f});
tl.from("#gp",{{y:60,opacity:0,duration:0.25}},{T("GOING") - 0.1:.3f});
const fd={{v:14}}; tl.to(fd,{{v:0,duration:1.4,ease:"power1.in",onUpdate:()=>{{document.getElementById("fd").textContent=String(Math.round(fd.v)).padStart(2,"0")}}}},{T("WEEKS") + 0.2:.3f});
tl.set(fd,{{v:14}},{SC["s1"][0]:.3f});
tl.from("#doc",{{y:600,rotation:12,duration:0.45,ease:"power3.out"}},{SC["s2"][0]:.3f}).fromTo("#stmp",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"power4.in"}},{T("OCTOBER") - 0.05:.3f});
tl.from(".cg b",{{opacity:0,scale:0.4,duration:0.18,stagger:0.012}},{SC["s3"][0] + 0.05:.3f})
  .fromTo(".d16",{{scale:1}},{{scale:1.35,backgroundColor:"{GLD}",color:"{INK}",boxShadow:"0 0 30px {GLD}",duration:0.25,ease:"back.out(3)"}},{T("16") - 0.05:.3f})
  .from("#wk",{{y:50,opacity:0,duration:0.25}},{T("WEEK") - 0.05:.3f});
tl.from(".race .bf",{{scaleX:0,duration:0.6,stagger:0.08,ease:"power3.out"}},{SC["s4"][0] + 0.1:.3f})
  .fromTo("#af",{{scaleX:0.2}},{{scaleX:1,duration:1.0,ease:"power2.inOut"}},{T("BIGGEST"):.3f}).from("#al",{{opacity:0,duration:0.2}},{T("BIGGEST") + 0.8:.3f});
tl.from("#tk",{{scale:0.4,opacity:0,duration:0.35,ease:"back.out(2)"}},{SC["s5"][0]:.3f}).from("#fol",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{T("FOLLOW") + 0.1:.3f})
  .to("#fol",{{scale:0.92,duration:0.08,yoyo:true,repeat:1}},{T("POST"):.3f}).to("#fol",{{backgroundColor:"{GRN}",duration:0.05}},{T("POST") + 0.08:.3f});
tl.fromTo("#s0",{{opacity:0}},{{opacity:1,duration:{TOTAL - SPEECH_END:.3f}}},{SPEECH_END:.3f});'''

# ================= FRONT
reacts = "".join(f'<i class="rx" style="left:{x}px">{e}</i>' for x, e in [(30, "🚀"), (950, "💰"), (60, "📈"), (920, "🔥"), (20, "🤯"), (960, "🚀"), (70, "💸"), (930, "📈")])
front_css = f'''.brk{{position:absolute;left:60px;top:118px;font-size:38px;background:{RED};padding:6px 22px;border-radius:12px;display:flex;gap:12px;align-items:center;box-shadow:0 10px 30px rgba(0,0,0,.4)}}
.brk i{{width:16px;height:16px;border-radius:50%;background:#fff}}
.chipx{{position:absolute;right:60px;top:118px;font-size:38px;background:{CRM};color:{INK};padding:6px 22px;border-radius:12px}}
.rx{{position:absolute;top:1900px;font-size:90px;font-style:normal;filter:drop-shadow(0 8px 14px rgba(0,0,0,.5))}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.leak{{position:absolute;left:-400px;top:-300px;width:700px;height:2600px;background:linear-gradient(90deg,transparent,rgba(255,170,100,.6),rgba(232,135,95,.4),transparent);filter:blur(34px);transform:rotate(16deg)}}
.tap{{position:absolute;left:620px;top:410px;font-size:110px}}'''
front_body = (clip("brk", 0, SC["s1"][0], f'<div class="brk" id="bk"><i id="dot"></i>BREAKING · AI NEWS</div>', 30) +
              clip("ant", SC["s2"][0], SC["s3"][1], '<div class="chipx" id="ax">NASDAQ: ANT 📈</div>', 30) +
              clip("rx", SC["s4"][0], SC["s4"][1] + 0.4, reacts, 25) +
              clip("tap", T("FOLLOW") + 0.25, SPEECH_END, '<div class="tap" id="tp">👆</div>', 30) +
              clip("tail", SPEECH_END, TOTAL, f'<div class="brk" id="bk2"><i></i>BREAKING · AI NEWS</div>', 30) +
              "".join(clip(f"tr{i}", t - 0.12, t + 0.4, f'<div class="flash" id="fl{i}"></div><div class="leak" id="lk{i}"></div>', 60) for i, t in enumerate(CUTS)))
RX = [round(SC["s4"][0] + 0.2 + i * 0.3, 2) for i in range(8)]
front_js = f'''tl.to("#dot",{{opacity:0.2,duration:0.3,repeat:9,yoyo:true}},0);
tl.from("#ax",{{x:500,duration:0.35,ease:"power3.out"}},{SC["s2"][0] + 0.3:.3f});
const RX={RX}; document.querySelectorAll(".rx").forEach((e,i)=>{{tl.fromTo(e,{{y:0,opacity:1,scale:0.6}},{{y:-760,opacity:0,scale:1.2,duration:1.6,ease:"power1.out"}},RX[i]);}});
tl.from("#tp",{{x:200,y:200,opacity:0,duration:0.35,ease:"power2.out"}},{T("FOLLOW") + 0.25:.3f}).to("#tp",{{scale:0.8,duration:0.08,yoyo:true,repeat:1}},{T("POST") - 0.05:.3f});
{"".join(f'tl.set("#fl{i}",{{opacity:0.6}},{t:.3f}).to("#fl{i}",{{opacity:0,duration:0.15}},{t + 0.02:.3f}).fromTo("#lk{i}",{{x:-300}},{{x:1500,duration:0.5,ease:"power1.inOut"}},{t - 0.12:.3f});' for i, t in enumerate(CUTS))}'''

for d, css, body, js in (("hf_back", back_css, back_body, back_js), ("hf_front", front_css, front_body, front_js)):
    open(d + "/index.html", "w").write(page(css, body, js))
json.dump({"scenes": SC, "cuts": CUTS, "speech_end": SPEECH_END, "total": TOTAL}, open("events.json", "w"), indent=1)
print("ok", TOTAL)
