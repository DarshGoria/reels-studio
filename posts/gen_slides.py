import json, html
E = html.escape
def slide(fname, title, label, kicker, page, accent, big, big_size, line, box=None, body=None, source="", last=False):
    arrow = '<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#121212" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path></svg>'
    plus = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#121212" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14"></path><path d="M5 12h14"></path></svg>'
    right = (f'Follow for more {plus}' if last else f'Swipe {arrow}')
    boxh = (f'<div style="display: flex; align-items: center; gap: 24px; margin-top: 16px; padding: 30px 34px; background: #121212; color: #F3EFE6; border-radius: 18px">'
            f'<div style="width: 18px; height: 18px; flex-shrink: 0; border-radius: 50%; background: {{{{accent}}}}"></div>'
            f'<div style="font-size: 42px; font-weight: 700; line-height: 1.22">{E(box)}</div></div>') if box else ""
    bodyh = f'<p style="margin: 0; font-size: 38px; line-height: 1.42; font-weight: 500; color: #3A3732; max-width: 900px">{E(body)}</p>' if body else ""
    bigh = (f'<div style="font-family: \'Archivo Black\', sans-serif; font-size: {big_size}px; line-height: 0.92; letter-spacing: -0.04em; color: {{{{accent}}}}">{E(big)}</div>') if big else ""
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{E(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&amp;family=Inter:wght@500;600;700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:#111111}}a:hover{{color:#444444}}
</style>
</helmet>
<div style="width: 1080px; height: 1350px; box-sizing: border-box; padding: 88px 80px 72px; background: #F3EFE6; color: #121212; font-family: Inter, sans-serif; display: flex; flex-direction: column; gap: 28px">
<div style="display: flex; align-items: center; justify-content: space-between">
<div style="font-size: 30px; font-weight: 700; letter-spacing: 0.14em">{E(label)}</div>
<div style="font-size: 28px; font-weight: 600; color: #5A5650">{E(kicker)} · {page}</div>
</div>
<div style="height: 4px; background: #121212"></div>
<div style="flex-grow: 1"></div>
{bigh}
<div style="font-size: 64px; line-height: 1.1; font-weight: 700; max-width: 920px">{E(line)}</div>
{bodyh}
{boxh}
<div style="flex-grow: 1"></div>
<div style="font-size: 24px; color: #5A5650">{E(source)}</div>
<div style="display: flex; align-items: center; justify-content: space-between; border-top: 2px solid #D6CFC1; padding-top: 32px">
<div style="display: flex; align-items: center; gap: 20px">
<div style="width: 76px; height: 76px; border-radius: 50%; background: #121212; color: #F3EFE6; display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: 700">DP</div>
<div style="display: flex; flex-direction: column; gap: 2px">
<div style="font-size: 30px; font-weight: 700">Darsh Patel</div>
<div style="font-size: 24px; color: #5A5650">AI news &amp; hacks</div>
</div>
</div>
<div style="display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 700">{right}</div>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"accent":{{"editor":"color","default":"{accent}","options":["{accent}","#E5481F","#1F5BE5","#0F8A5F"]}},"$preview":{{"width":1080,"height":1350}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{ accent: this.props.accent ?? '{accent}' }};
}}
}}
</script>
</body>
</html>
'''
    open(f"project/{fname}", "w").write(doc)

C = {
 "GPT": ("CHATGPT IN 2026", "#0F7A5C", [
   dict(big="900,000,000", big_size=150, line="people use ChatGPT every week.", box="That’s more than 1 in 10 humans on Earth."),
   dict(big="2", big_size=330, line="months to hit its first 100 million users.", body="ChatGPT launched on November 30, 2022. It became one of the fastest-growing apps ever."),
   dict(big="900M", big_size=300, line="weekly users by February 2026.", body="From a free research demo to one of the most-used apps in the world, in just over three years."),
   dict(big="#2", big_size=330, line="India is OpenAI’s second-largest market.", box="Indians even got ChatGPT Go free for a year in Nov 2025."),
   dict(big="", big_size=0, line="Are you one of the 900 million?", body="Comment what you use ChatGPT for the most, and save this post.", box="Follow for AI news that actually matters to you."),
 ], ["Source: OpenAI user figures via Wikipedia (Feb 2026)", "Source: ChatGPT launch Nov 30, 2022 · 100M users in 2 months", "Source: 900M weekly active users, Feb 2026", "Source: OpenAI via YourStory · ChatGPT Go offer, Nov 4, 2025", ""]),
 "EL": ("AI VOICE", "#6D3FE0", [
   dict(big="$22B", big_size=330, line="The AI voice company that doubled its value in 7 months.", box="It’s called ElevenLabs."),
   dict(big="$11B", big_size=330, line="February 2026", body="ElevenLabs raised $500 million at an $11 billion valuation."),
   dict(big="$22B", big_size=330, line="September 2026", body="A staff share sale valued it at $22 billion. Reuters says demand for AI voice agents drove the jump."),
   dict(big="", big_size=0, line="What it actually does", body="Turns text into a realistic human voice, clones your own voice from a short sample, dubs videos into other languages and powers AI phone agents."),
   dict(big="$1", big_size=330, line="to try it yourself.", body="The Starter plan is $1 for the first month until Nov 8, then $6/month.", box="Save this before the offer ends."),
 ], ["Source: Wikipedia · Reuters (Sep 30, 2026)", "Source: ElevenLabs funding announcement, Feb 4, 2026", "Source: Reuters, Sep 30, 2026", "Source: ElevenLabs product pages", "Source: ElevenLabs pricing (checked Nov 2026)"]),
 "DC": ("US MIDTERMS 2026", "#E5481F", [
   dict(big="56%", big_size=330, line="of US voters said AI and data centers shaped their vote.", box="AI just became an election issue."),
   dict(big="", big_size=0, line="It’s not about killer robots.", body="Voters cared about what a data center does to their own town: higher energy bills, noise, water use and the environment."),
   dict(big="Prison > AI", big_size=170, line="Americans would rather live near a prison than an AI data center.", body="Same for a methadone clinic or a nuclear power plant, according to Blue Rose Research polling."),
   dict(big="3%", big_size=330, line="India makes ~20% of the world’s data but has only ~3% of its data centres.", box="And India is building fast. Will we face this backlash too?"),
   dict(big="", big_size=0, line="Would you want an AI data center in your city?", box="Comment YES or NO", body="Share this with the friend who works in tech."),
 ], ["Source: NBC exit poll via TIME, Nov 4, 2026", "Source: TIME, Nov 4, 2026", "Source: Blue Rose Research via TIME", "Source: industry estimates as reported in Indian media", ""]),
}
names = []
for key, (label, acc, slides, srcs) in C.items():
    kick = {"GPT": "CHATGPT", "EL": "ELEVENLABS", "DC": "DATA CENTERS"}[key]
    for i, s in enumerate(slides):
        fn = f"{key}-{i+1}.dc.html"; names.append(fn)
        slide(fn, f"{kick} slide {i+1}", label, kick, f"{i+1}/5", acc, s["big"], s["big_size"], s["line"], s.get("box"), s.get("body"), srcs[i], last=(i == 4))
cj = json.load(open("project/canvas.json"))
for r, key in enumerate(["GPT", "EL", "DC"]):
    y = 3260 + r * 1690
    cj["notes"][f"t{key}"] = {"x": 0, "y": y - 300, "text": {"GPT": "Carousel A · 900M ChatGPT users", "EL": "Carousel B · ElevenLabs $22B", "DC": "Carousel C · 56% data centers"}[key], "kind": "title1", "maxW": 5720}
    for i in range(5):
        fn = f"{key}-{i+1}.dc.html"
        cj["boards"][fn] = {"x": i * 1160, "y": y, "w": 1080, "h": 1350, "title": f"{key} {i+1}/5"}
        if fn not in cj["order"]: cj["order"].append(fn)
json.dump(cj, open("project/canvas.json", "w"))
print(names)
