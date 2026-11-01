"""Reel 4 'Make AI interview you' — HyperFrames overlay composition, generated from word timings.
Look: dark-mode hacker/chat UI, neon green accent; split screen with a live chat mockup in the top half."""
import json, sys, html as H
sys.path.insert(0, ".")
from timeline import word_time, SPEECH_END, TOTAL

def T(w, n=1): return round(word_time(w, n)[0], 3)
def E(w, n=1): return round(word_time(w, n)[1], 3)
def clip(id_, s, e, inner, cls="", z=10):
    return (f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="{z}" style="z-index:{z}">{inner}</div>')

NEON, RED, BG = "#39FF88", "#FF4D5E", "#0A0E0C"
P0, P1 = T("STOP") - 0.15, T("TRY") - 0.08          # split-screen window (top panel)
CARD1 = (T("TRY") - 0.02, T("FOLLOW") - 0.06)
CARD2 = (T("FOLLOW") - 0.04, SPEECH_END)
PROMPT = "Before you answer, ask me 5 questions."
TY0, TY1 = T("BEFORE"), E("QUESTIONS")
LONG = ("Act as a world-class copywriter with 10+ years of experience. Write a LinkedIn post about my startup. "
        "Make it engaging but professional, fun but not cringe, under 200 words, add emojis, a strong hook, a CTA, "
        "mention all our features, target founders AND students, keep it short but detailed, sound human, "
        "avoid buzzwords, add hashtags, make it go viral…")
QS = ["Who is this post for?", "What's the one goal?", "What tone do you want?", "How long should it be?", "Any post you love as an example?"]
chars = "".join(f'<span class="ch">{H.escape(c) if c != " " else "&nbsp;"}</span>' for c in PROMPT)

hook = f'''<div class="hk"><div class="hk-l1">YOU'RE USING</div>
<div class="hk-gl"><div class="g r">CHATGPT</div><div class="g c">CHATGPT</div><div class="g w">CHATGPT</div></div>
<div class="hk-l3">WRONG ❌</div><div class="scan"></div></div>'''

panel = f'''<div class="pn" id="pn">
 <div class="bar"><span class="dot"></span><span>AI Chat</span><span class="mdl">● online</span></div>
 <div class="ub" id="long"><div class="lt">{H.escape(LONG)}</div><div class="cnt">📜 120-word prompt</div></div>
 <div class="stamp" id="stop">✋ STOP</div>
 <div class="one" id="one">+ JUST ONE LINE ☝️</div>
 <div class="inp" id="inp"><div class="typed">{chars}<span class="caret" id="caret"></span></div><div class="send" id="send">➤</div></div>
 <div class="ub mine" id="sent">{H.escape(PROMPT)}</div>
 <div class="ai" id="ai"><div class="aih">🤖 Sure! First, 5 quick questions:</div>{"".join(f'<div class="q" id="q{i}">{i + 1}. {H.escape(q)}</div>' for i, q in enumerate(QS))}</div>
 <div class="meter" id="meter"><div class="mt">ANSWER QUALITY</div><div class="track"><div class="fill" id="fill"></div><div class="needle" id="needle"></div></div>
  <div class="ml"><span id="lg">😐 GENERIC</span><span id="ls">🎯 SCARY ACCURATE</span></div></div>
 <div class="div"></div>
</div>'''

doc = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:PB;src:url(assets/fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:PM;src:url(assets/fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:MO;src:url(assets/fonts/DejaVuSansMono.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
#root{{width:1080px;height:1920px;position:relative;font-family:PB;color:#fff}}
.full{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}}
.hk{{position:absolute;inset:0;background:{BG};display:flex;flex-direction:column;align-items:center;justify-content:center}}
.hk-l1{{font-size:70px;letter-spacing:.06em;color:#cfd8d3}}
.hk-gl{{position:relative;width:1000px;height:200px;margin:14px 0}}
.g{{position:absolute;inset:0;text-align:center;font-size:172px;line-height:200px;letter-spacing:-.02em}}
.g.r{{color:#ff2a55;mix-blend-mode:screen}} .g.c{{color:#00e5ff;mix-blend-mode:screen}} .g.w{{color:#fff}}
.hk-l3{{font-size:120px;color:{RED}}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.04) 0 2px,transparent 2px 6px)}}
.pnwrap{{position:absolute;left:0;top:0;width:1080px;height:960px}}
.pn{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 0%,#12201a 0%,{BG} 70%);overflow:hidden}}
.pn::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(57,255,136,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(57,255,136,.05) 1px,transparent 1px);background-size:60px 60px}}
.bar{{position:absolute;left:0;right:0;top:0;height:120px;display:flex;align-items:center;gap:18px;padding:40px 50px 0;font-size:40px;border-bottom:2px solid #1b2a22}}
.dot{{width:22px;height:22px;border-radius:50%;background:{NEON};box-shadow:0 0 18px {NEON}}}
.mdl{{margin-left:auto;font-family:PM;font-size:28px;color:{NEON}}}
.ub{{position:absolute;right:50px;top:160px;width:780px;background:#1c2a23;border-radius:34px 34px 8px 34px;padding:26px 30px}}
.lt{{font-family:PM;font-size:31px;line-height:1.35;color:#d8e6dd}}
.cnt{{margin-top:12px;font-size:28px;color:#8fb59f}}
.mine{{background:{NEON};color:#04140b;font-size:40px;top:150px;width:auto;left:auto;max-width:820px}}
.stamp{{position:absolute;left:300px;top:330px;font-size:120px;color:{RED};border:10px solid {RED};border-radius:28px;padding:4px 36px;background:rgba(10,14,12,.85)}}
.one{{position:absolute;left:50px;top:470px;font-size:58px;color:{NEON}}}
.inp{{position:absolute;left:50px;right:50px;top:640px;height:150px;border-radius:40px;background:#121a16;border:4px solid #2c3d33;display:flex;align-items:center;padding:0 30px}}
.typed{{flex:1;font-family:MO;font-size:33px;color:#fff;white-space:nowrap;overflow:hidden;display:flex;align-items:center}}
.caret{{display:inline-block;width:4px;height:52px;background:{NEON};margin-left:4px}}
.send{{width:96px;height:96px;border-radius:50%;background:#26352d;color:#7f9b8b;font-size:46px;display:flex;align-items:center;justify-content:center}}
.ai{{position:absolute;left:50px;top:300px;width:900px;background:#141d18;border:3px solid #22362b;border-radius:34px 34px 34px 8px;padding:26px 32px}}
.aih{{font-size:40px;color:{NEON};margin-bottom:10px}}
.q{{font-family:PM;font-size:38px;line-height:1.45;color:#e9f3ed}}
.meter{{position:absolute;left:60px;right:60px;top:250px;background:rgba(8,12,10,.96);border:3px solid {NEON};border-radius:36px;padding:40px 44px 46px}}
.mt{{font-size:44px;letter-spacing:.06em;color:#cfe9da}}
.track{{position:relative;height:56px;border-radius:28px;background:#1d2a23;margin-top:34px;overflow:visible}}
.fill{{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:28px;background:linear-gradient(90deg,{RED},#ffc23d 50%,{NEON});transform-origin:left center}}
.needle{{position:absolute;top:-22px;width:16px;height:100px;border-radius:8px;background:#fff;left:0;box-shadow:0 0 0 6px rgba(0,0,0,.4)}}
.ml{{display:flex;justify-content:space-between;margin-top:28px;font-size:40px}}
#lg{{color:#ffb3bb}} #ls{{color:{NEON}}}
.div{{position:absolute;left:0;right:0;bottom:0;height:8px;background:{NEON}}}
.top{{position:absolute;left:70px;top:270px;width:940px}}
.gcard{{background:rgba(10,14,12,.94);border:3px solid {NEON};border-radius:38px;padding:34px 40px;box-shadow:0 24px 60px rgba(0,0,0,.4)}}
.ct{{font-size:44px;color:{NEON};letter-spacing:.04em}}
.code{{margin-top:18px;font-family:MO;font-size:40px;background:#16211b;border-radius:22px;padding:24px 26px;color:#fff;line-height:1.35}}
.save{{margin-top:18px;font-family:PM;font-size:34px;color:#b9d6c5}}
.fol{{text-align:center;font-size:60px;line-height:1.15}}
.fol b{{color:{NEON}}}
.bell{{display:inline-block;font-size:90px;margin-bottom:8px}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{clip("hook", 0, 0.5, f'<div class="full" id="hkz">{hook}</div>', "full", 50)}
{clip("panel", P0, P1, f'<div class="pnwrap" id="pw">{panel}</div>', "full", 20)}
{clip("card1", *CARD1, f'<div class="top"><div class="gcard in"><div class="ct">📋 COPY THIS LINE</div><div class="code">{H.escape(PROMPT)}</div><div class="save">Save this reel so you don\'t forget 🔖</div></div></div>', "full", 30)}
{clip("card2", *CARD2, f'<div class="top"><div class="gcard in fol"><div class="bell" id="bell">🔔</div><div>FOLLOW FOR<br><b>DAILY AI HACKS ⚡</b></div></div></div>', "full", 30)}
{clip("tail", SPEECH_END, TOTAL, f'<div class="full" id="tlz">{hook}</div>', "full", 60)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
// hook: glitch jitter (deterministic), zoom 1.1 -> 1.0
tl.fromTo("#hkz",{{scale:1.10}},{{scale:1.0,duration:0.5,ease:"power2.out"}},0);
const jit = [[-14,6],[10,-4],[-6,10],[16,-8],[-10,4],[6,-12],[-16,8],[0,0]];
jit.forEach(([a,b],i)=>{{ tl.set("#hkz .g.r",{{x:a,y:b}},i*0.06).set("#hkz .g.c",{{x:-a,y:-b}},i*0.06); }});
// tail: same frame as the hook's first frame at the end
tl.fromTo("#tlz",{{opacity:0,scale:1.0}},{{opacity:1,duration:0.12,ease:"none"}},{SPEECH_END:.3f})
  .to("#tlz",{{scale:1.10,duration:{TOTAL - SPEECH_END - 0.02:.3f},ease:"power2.in"}},{SPEECH_END:.3f})
  .set("#tlz .g.r",{{x:-14,y:6}},{SPEECH_END:.3f}).set("#tlz .g.c",{{x:14,y:-6}},{SPEECH_END:.3f});
// panel slides down (matches the video shrink in ffmpeg: 0.25 s in, 0.22 s out, cubic)
tl.fromTo("#pw",{{y:-960}},{{y:0,duration:0.25,ease:"power3.out"}},{P0:.3f})
  .to("#pw",{{y:-960,duration:0.22,ease:"power3.in"}},{P1 - 0.22:.3f});
// S1 long prompt -> STOP
tl.from("#long",{{y:60,opacity:0,duration:0.3,ease:"power3.out"}},{P0 + 0.1:.3f})
  .fromTo("#stop",{{scale:2.4,opacity:0,rotation:-12}},{{scale:1,opacity:1,rotation:-8,duration:0.2,ease:"power3.in"}},{T("PROMPTS"):.3f})
  .to(["#long","#stop"],{{opacity:0,y:-40,duration:0.25}},{T("JUST") - 0.2:.3f});
// S2 one line + input box
tl.set(["#stop","#one","#inp","#sent","#ai","#meter"],{{opacity:0}},0)
  .to("#inp",{{opacity:1,duration:0.25}},{T("JUST") - 0.05:.3f})
  .fromTo("#one",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.28,ease:"back.out(2)"}},{T("ONE"):.3f})
  .fromTo("#inp",{{borderColor:"#2c3d33"}},{{borderColor:"{NEON}",duration:0.2}},{T("END"):.3f});
// caret blink (finite, deterministic) and typing synced to the spoken line
tl.set(".ch",{{opacity:0,display:"none"}},0);
const n = {len(PROMPT)}, ty0 = {TY0:.3f}, ty1 = {TY1:.3f};
for (let i=0;i<n;i++) tl.set(`.ch:nth-child(${{i+1}})`,{{opacity:1,display:"inline"}}, ty0 + (ty1-ty0)*i/n);
for (let k=0;k<12;k++) tl.set("#caret",{{opacity:k%2?0:1}}, {T("JUST"):.3f} + k*0.35);
tl.set("#caret",{{opacity:1}},ty0)
  .to("#send",{{background:"{NEON}",color:"#04140b",duration:0.15}},ty1)
  .to("#one",{{opacity:0,duration:0.2}},ty1)
  .fromTo("#sent",{{opacity:0,y:520,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"power3.out"}},ty1 + 0.15)
  .to("#inp",{{opacity:0,duration:0.2}},ty1 + 0.15);
// S4 AI interviews you
tl.fromTo("#ai",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{T("NOW") - 0.05:.3f});
for (let i=0;i<5;i++) tl.from(`#q${{i}}`,{{opacity:0,x:-40,duration:0.22,ease:"power2.out"}}, {T("INTERVIEWS"):.3f} + i*0.32);
// S5 meter generic -> scary accurate
tl.to(["#ai","#sent"],{{opacity:0.15,duration:0.25}},{T("GENERIC") - 0.3:.3f})
  .fromTo("#meter",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)"}},{T("GENERIC") - 0.3:.3f})
  .fromTo("#fill",{{scaleX:0.12}},{{scaleX:0.12,duration:0.01}},0)
  .fromTo("#needle",{{x:40}},{{x:40,duration:0.01}},0)
  .to("#fill",{{scaleX:1,duration:0.7,ease:"power3.inOut"}},{T("SCARY"):.3f})
  .to("#needle",{{x:{1080 - 120 - 88 - 30},duration:0.7,ease:"power3.inOut"}},{T("SCARY"):.3f})
  .from("#ls",{{scale:0.5,duration:0.3,ease:"back.out(3)"}},{T("ACCURATE"):.3f});
// copy card + follow card above the head
for (const [id,s,e] of [["card1",{CARD1[0]:.3f},{CARD1[1]:.3f}],["card2",{CARD2[0]:.3f},{CARD2[1]:.3f}]]) {{
  tl.fromTo(`#${{id}} .in`,{{y:-50,scale:0.9,opacity:0}},{{y:0,scale:1,opacity:1,duration:0.32,ease:"back.out(1.5)"}},s)
    .to(`#${{id}} .in`,{{opacity:0,scale:0.96,duration:0.2,ease:"power2.in"}},e-0.22);
}}
for (let k=0;k<8;k++) tl.to("#bell",{{rotation:k%2?-16:16,duration:0.08}}, {CARD2[0] + 0.3:.3f} + k*0.08);
tl.to("#bell",{{rotation:0,duration:0.1}}, {CARD2[0] + 0.3 + 0.64:.3f});
window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>'''
open("hf/index.html", "w").write(doc)
json.dump({"split": [P0, P1], "card1": CARD1, "card2": CARD2, "speech_end": SPEECH_END, "total": TOTAL}, open("hf/events.json", "w"), indent=1)
print("ok", TOTAL, "split", P0, P1)
