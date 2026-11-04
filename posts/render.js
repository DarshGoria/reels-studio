const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const P = '/home/claude/carousel/project', F = path.resolve('node_modules/@fontsource');
const faces = `@font-face{font-family:'Archivo Black';src:url(file://${F}/archivo-black/files/archivo-black-latin-400-normal.woff2)}
@font-face{font-family:Inter;font-weight:500;src:url(file://${F}/inter/files/inter-latin-500-normal.woff2)}
@font-face{font-family:Inter;font-weight:600;src:url(file://${F}/inter/files/inter-latin-600-normal.woff2)}
@font-face{font-family:Inter;font-weight:700;src:url(file://${F}/inter/files/inter-latin-700-normal.woff2)}
body{margin:0}`;
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  fs.mkdirSync('out', { recursive: true });
  for (const k of ['GPT', 'EL', 'DC']) for (let i = 1; i <= 5; i++) {
    let s = fs.readFileSync(`${P}/${k}-${i}.dc.html`, 'utf8');
    const acc = s.match(/"default":"(#[0-9A-Fa-f]{6})"/)[1];
    const root = s.match(/<x-dc>[\s\S]*?<\/helmet>\s*([\s\S]*)<\/x-dc>/)[1].replace(/\{\{accent\}\}/g, acc);
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>${faces}</style></head><body>${root}</body></html>`;
    const f = path.resolve(`out/_${k}${i}.html`); fs.writeFileSync(f, html);
    await pg.goto('file://' + f); await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot({ path: `out/${{GPT:'A_chatgpt',EL:'B_elevenlabs',DC:'C_datacenters'}[k]}_${i}.png` });
  }
  await b.close();
})();
