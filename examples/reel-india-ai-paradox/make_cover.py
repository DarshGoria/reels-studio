import numpy as np, onnxruntime as ort, subprocess
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
F='hf_front/assets/fonts/'; W,H=1080,1920
VF="colorbalance=rs=-0.08:gs=0.10:bs=-0.06:rm=-0.12:gm=0.12:bm=-0.10:rh=-0.04:gh=0.05:bh=-0.04,hue=s=0.72,eq=brightness=0.04:gamma=1.06:contrast=1.08"
raw=subprocess.run(["ffmpeg","-v","error","-ss","3.0","-i","joined3.mkv","-frames:v","1","-vf",VF,"-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
rgb=Image.fromarray(np.frombuffer(raw,np.uint8).reshape(H,W,3))
s=ort.InferenceSession('/home/claude/tools/models/seg/u2net_human_seg.onnx',providers=['CPUExecutionProvider'])
x=(np.asarray(rgb.resize((320,320)),np.float32)/255-[0.485,0.456,0.406])/[0.229,0.224,0.225]
m=s.run(None,{s.get_inputs()[0].name:x.transpose(2,0,1)[None].astype(np.float32)})[0][0,0]; m=(m-m.min())/(m.max()-m.min()+1e-6)
M=Image.fromarray((m*255).astype(np.uint8)).resize((W,H)).filter(ImageFilter.GaussianBlur(2))
bg=ImageEnhance.Brightness(rgb).enhance(0.5).convert('RGBA')
glow=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(glow); g.ellipse((60,150,560,900),fill=(255,153,51,150)); g.ellipse((520,150,1020,900),fill=(34,197,94,140)); bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(140)))
fnt=lambda n,z: ImageFont.truetype(F+n,z)
def st(layer,xy,t,f,fill):
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((xy[0],xy[1]+14),t,font=f,fill=(0,0,0,170)); layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18))); ImageDraw.Draw(layer).text(xy,t,font=f,fill=fill)
back=Image.new('RGBA',(W,H),(0,0,0,0)); f=fnt('Poppins-Bold.ttf',250); d=ImageDraw.Draw(back)
st(back,(30,360),"20%",f,(255,153,51)); st(back,(W-30-d.textlength("3%",font=f),360),"3%",f,(34,197,94))
bg.alpha_composite(back); p=rgb.convert('RGBA'); p.putalpha(M); bg.alpha_composite(p)
fr=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(fr)
pf=fnt('Poppins-Bold.ttf',54); t="INDIA'S AI PARADOX"; w=d.textlength(t,font=pf); x0=(W-w)/2+50
d.rounded_rectangle((x0-140,236,x0+w+40,340),radius=52,fill=(12,12,14,235),outline=(255,153,51),width=5); d.text((x0,248),t,font=pf,fill=(255,246,234))
lf=fnt('Poppins-Bold.ttf',40)
for txt,xx,c in (("OF WORLD'S DATA",40,(255,153,51)),("OF DATA CENTRES",W-40-d.textlength("OF DATA CENTRES",font=lf),(34,197,94))):
    d.rounded_rectangle((xx-16,650,xx+d.textlength(txt,font=lf)+16,712),radius=14,fill=(12,12,14,220)); d.text((xx,654),txt,font=lf,fill=c)
for i,(t,c,bc,z) in enumerate((("BUILD OUR OWN AI",(17,17,17),(255,211,77),86),("OR BE THE WORKFORCE?",(255,255,255),(255,61,61),72))):
    bf=fnt('Poppins-Bold.ttf',z); w=d.textlength(t,font=bf); y=1400+i*132; d.rounded_rectangle(((W-w)/2-32,y,(W+w)/2+32,y+120),radius=22,fill=bc); d.text(((W-w)/2,y+(86-z)//2),t,font=bf,fill=c)
bg.alpha_composite(fr)
ef=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)
def emo(ch,x,y,sz,rot=0):
    e=Image.new('RGBA',(160,160),(0,0,0,0)); ImageDraw.Draw(e).text((10,10),ch,font=ef,embedded_color=True)
    e=e.resize((int(160*sz/109),)*2,Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC); bg.alpha_composite(e,(x,y))
emo("🇮🇳",int(x0-120),246,80); emo("🤔",40,1200,140,10); emo("🔥",900,1220,130,-10)
bg.convert('RGB').save('cover_nn3.jpg',quality=95)
a=bg.convert('RGB').resize((405,720)); b=bg.convert('RGB').crop((0,240,1080,1680)).resize((540,720)); c=Image.new('RGB',(965,720),'white'); c.paste(a,(0,0)); c.paste(b,(425,0)); c.save('cover_check.png')
