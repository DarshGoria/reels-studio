"""N2 'Free trillion-parameter AI' — CINEMATIC DEPTH edit. Two HyperFrames layers:
  hf_back : giant words that sit BEHIND the speaker (person cut-out goes on top of them in compose_depth.py)
  hf_front: name card, catch glitch, RAM meter, tag-a-friend, all clear of the face (faces.json)."""
import json, sys, os, shutil
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def E(w, n=1): return round(word_time(w, n)[1], 3)
def clip(id_, s, e, inner, z=10):
    return (f'<div id="{id_}" class="clip full" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')
FZ = json.load(open("faces.json"))
RED, YEL, CREAM = "#FF3D3D", "#FFD34D", "#FFF4E0"
BELOW = FZ["free_below"][0]                    # first y under the chin
B = {"free": (0.0, T("MISTRAL") - 0.12), "tril": (T("TRILLION") - 0.12, T("ANYONE") - 0.1),
     "gb": (T("500") - 0.12, T("YOUR") - 0.08), "tail": (SPEECH_END, TOTAL)}
F = {"tag0": (0.0, T("MISTRAL") - 0.12), "name": (T("MISTRAL") - 0.05, T("TRILLION") - 0.15),
     "biz": (T("ANYONE") - 0.05, T("CATCH") - 0.4), "catch": (T("CATCH") - 0.35, T("YOU'D") - 0.02),
     "ram": (T("YOU'D") - 0.02, T("TAG") - 0.1), "tag": (T("TAG") - 0.05, SPEECH_END)}
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

# ---------------- BACK: giant depth words (head/shoulders will cover their lower part)
back_css = f'''.dw{{position:absolute;left:0;right:0;text-align:center;line-height:.86;letter-spacing:-.04em;text-shadow:0 10px 50px rgba(0,0,0,.35)}}
#free .dw{{top:500px;font-size:400px;color:{CREAM}}}
#tril .a{{top:330px;font-size:330px;color:{CREAM}}} #tril .b{{top:650px;font-size:178px;color:{YEL}}}
#gb .dw{{top:540px;font-size:300px;color:{YEL}}}
#tail .dw{{top:500px;font-size:400px;color:{CREAM}}}'''
back_body = (clip("free", *B["free"], '<div class="dw" id="fw">FREE</div>') +
             clip("tril", *B["tril"], '<div class="dw a" id="t1">1</div><div class="dw b" id="t2">TRILLION</div>') +
             clip("gb", *B["gb"], '<div class="dw" id="gw">500GB</div>') +
             clip("tail", *B["tail"], '<div class="dw" id="tw">FREE</div>', 60))
back_js = f'''tl.fromTo("#fw",{{scale:1.0}},{{scale:1.08,duration:{B["free"][1]:.3f},ease:"sine.inOut"}},0)
  .to("#fw",{{opacity:0,y:-40,duration:0.2}},{B["free"][1] - 0.2:.3f});
tl.from("#t1",{{y:200,opacity:0,duration:0.3,ease:"power3.out"}},{B["tril"][0]:.3f})
  .from("#t2",{{scale:1.6,opacity:0,duration:0.3,ease:"power3.out"}},{T("TRILLION") + 0.05:.3f})
  .to(["#t1","#t2"],{{opacity:0,y:-40,duration:0.2}},{B["tril"][1] - 0.2:.3f});
tl.from("#gw",{{scale:0.6,opacity:0,duration:0.3,ease:"back.out(1.8)"}},{B["gb"][0]:.3f})
  .to("#gw",{{scale:1.06,duration:{B["gb"][1] - B["gb"][0] - 0.5:.3f},ease:"sine.inOut"}},{B["gb"][0] + 0.3:.3f})
  .to("#gw",{{opacity:0,duration:0.2}},{B["gb"][1] - 0.2:.3f});
tl.fromTo("#tw",{{opacity:0,scale:0.9}},{{opacity:1,scale:1.0,duration:{TOTAL - SPEECH_END - 0.03:.3f},ease:"back.out(1.6)"}},{SPEECH_END:.3f});'''

# ---------------- FRONT: everything that must stay readable, kept under the chin / out of the face
y0 = 250                                 # face sits low in this clip: front cards live in the free space above the head
front_css = f'''.pill{{position:absolute;left:0;right:0;top:330px;text-align:center}}
.pill span{{display:inline-block;font-size:44px;background:rgba(10,10,12,.78);border:3px solid {CREAM};padding:10px 30px;border-radius:99px}}
.lt{{position:absolute;left:60px;top:{y0}px;display:flex;align-items:stretch}}
.lt .bar{{width:14px;background:{RED};border-radius:7px;margin-right:20px}}
.lt .n1{{font-size:70px;line-height:1}} .lt .n2{{font-family:PM;font-size:38px;color:#ffd9c9;margin-top:6px}}
.lt .box{{background:rgba(10,10,12,.72);padding:18px 30px;border-radius:20px}}
.biz{{position:absolute;left:0;right:0;top:{y0}px;text-align:center}}
.biz span{{display:inline-block;font-size:58px;background:#1fae5b;padding:14px 36px;border-radius:24px;box-shadow:0 14px 34px rgba(0,0,0,.45)}}
.ct{{position:absolute;left:0;right:0;top:{y0 + 150}px;text-align:center;font-size:150px;line-height:1}}
.ct .r,.ct .c{{position:absolute;left:0;right:0;mix-blend-mode:screen}} .ct .r{{color:#ff2a55}} .ct .c{{color:#00e5ff}} .ct .w{{position:relative;color:#fff}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.ram{{position:absolute;left:60px;right:60px;top:{y0 - 30}px;background:rgba(10,10,12,.82);border-radius:30px;padding:26px 32px;border:3px solid rgba(255,255,255,.2)}}
.rr{{display:flex;align-items:center;gap:18px;margin:10px 0;font-size:36px}} .rl{{width:270px}}
.tk{{flex:1;height:52px;background:#26262c;border-radius:14px;overflow:hidden}}
.fl{{height:100%;border-radius:14px;transform-origin:left center;display:flex;align-items:center;padding-left:16px;font-size:32px}}
.skull{{position:absolute;right:30px;top:-70px;font-size:66px;background:{RED};padding:6px 26px;border-radius:22px;transform:rotate(6deg)}}
.tag{{position:absolute;left:0;right:0;top:{y0}px;text-align:center}}
.tag span{{display:inline-block;font-size:56px;line-height:1.15;background:{YEL};color:#111;padding:16px 36px;border-radius:26px;box-shadow:0 14px 34px rgba(0,0,0,.45)}}'''
front_body = (clip("tag0", *F["tag0"], '<div class="pill" id="p0"><span>🤖 1-TRILLION-PARAMETER AI</span></div>') +
              clip("name", *F["name"], '<div class="lt" id="lt"><div class="bar"></div><div class="box"><div class="n1">MISTRAL AI</div><div class="n2">“Le Chonk” · Mistral Large 4</div></div></div>') +
              clip("biz", *F["biz"], '<div class="biz" id="bz"><span>✅ FREE · EVEN FOR BUSINESS</span></div>') +
              clip("catch", *F["catch"], '<div class="ct" id="ct"><div class="r">THE CATCH?</div><div class="c">THE CATCH?</div><div class="w">THE CATCH?</div></div><div class="flash" id="fl"></div>', 40) +
              clip("ram", *F["ram"], f'<div class="ram" id="rm"><div class="skull" id="sk">16GB 💀</div><div class="rr"><span class="rl">🧠 It needs</span><div class="tk"><div class="fl" id="f1" style="width:100%;background:{RED}">~500GB</div></div></div><div class="rr"><span class="rl">💻 Your laptop</span><div class="tk"><div class="fl" id="f2" style="width:3.2%;background:{YEL};color:#111"></div></div><span id="l16" style="font-size:34px">16GB</span></div></div>') +
              clip("tag", *F["tag"], '<div class="tag" id="tg"><span>🎮 TAG A FRIEND<br>WITH A GAMING PC</span></div>'))
front_js = f'''tl.from("#p0 span",{{y:-30,opacity:0,duration:0.3,ease:"power3.out"}},0.15).to("#p0",{{opacity:0,duration:0.2}},{F["tag0"][1] - 0.2:.3f});
tl.from("#lt",{{x:-500,duration:0.35,ease:"power3.out"}},{F["name"][0]:.3f}).to("#lt",{{x:-600,duration:0.25,ease:"power3.in"}},{F["name"][1] - 0.25:.3f});
tl.from("#bz span",{{scale:0.4,opacity:0,duration:0.3,ease:"back.out(2.2)"}},{F["biz"][0]:.3f}).to("#bz",{{opacity:0,duration:0.15}},{F["biz"][1] - 0.15:.3f});
const j=[[-18,8],[14,-6],[-8,12],[20,-10],[-12,6],[6,-14],[0,0]];
j.forEach(([a,b],i)=>{{ tl.set("#ct .r",{{x:a,y:b}},{F["catch"][0]:.3f}+i*0.07).set("#ct .c",{{x:-a,y:-b}},{F["catch"][0]:.3f}+i*0.07); }});
tl.from("#ct",{{scale:1.8,opacity:0,duration:0.18,ease:"power4.out"}},{T("CATCH") - 0.05:.3f})
  .to("#fl",{{opacity:0.55,duration:0.05}},{T("CATCH") - 0.05:.3f}).to("#fl",{{opacity:0,duration:0.2}},{T("CATCH"):.3f});
tl.from("#rm",{{y:80,opacity:0,duration:0.3,ease:"power3.out"}},{F["ram"][0]:.3f})
  .fromTo("#f1",{{scaleX:0}},{{scaleX:1,duration:0.9,ease:"power2.out"}},{T("500") - 0.1:.3f})
  .fromTo("#f2",{{scaleX:0}},{{scaleX:1,duration:0.3}},{T("LAPTOP"):.3f})
  .fromTo("#sk",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power3.in"}},{T("16"):.3f})
  .to("#rm",{{opacity:0,duration:0.15}},{F["ram"][1] - 0.15:.3f});
tl.from("#tg span",{{scale:0.5,opacity:0,rotation:-6,duration:0.3,ease:"back.out(2)"}},{F["tag"][0]:.3f});'''

exec(open("gen_extra.py").read())
for d, css, body, js in (("hf_back", back_css, back_body, back_js), ("hf_front", front_css, front_body, front_js)):
    os.makedirs(d + "/assets/fonts", exist_ok=True)
    for f in ("hyperframes.json", "package.json"): shutil.copy(f"/home/claude/r5/hf/{f}", d)
    shutil.copy("/home/claude/r5/hf/assets/gsap.min.js", d + "/assets/")
    for f in os.listdir("/home/claude/r5/hf/assets/fonts"): shutil.copy("/home/claude/r5/hf/assets/fonts/" + f, d + "/assets/fonts/")
    open(d + "/index.html", "w").write(page(css, body, js))
json.dump({"back": B, "front": F, "speech_end": SPEECH_END, "total": TOTAL,
           "depth_windows": [[0, TOTAL + 0.6]]}, open("events.json", "w"), indent=1)
print("ok", TOTAL, "below", BELOW)
