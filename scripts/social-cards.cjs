// Rebuild checked-in link-preview images using existing library images and a fresh Chrome profile.
const fs = require('fs'), path = require('path'), os = require('os');
const {spawn} = require('child_process');
const {WebSocket} = require('undici');
const root = path.resolve(__dirname, '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'data/catalog.json')));
const output = path.join(root, 'assets/social');
const escape = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dataImage = file => `data:image/${path.extname(file).slice(1)};base64,${fs.readFileSync(path.join(root,file)).toString('base64')}`;
const avatar = dataImage('assets/solarfren.png');
const css = `*{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden}body{font-family:Arial,sans-serif;background:#10151d;color:#edf3f9;display:grid;grid-template-columns:610px 590px}.copy{padding:48px 32px 36px 52px;display:flex;flex-direction:column}.brand{display:flex;align-items:center;gap:14px;font-size:20px;letter-spacing:2px;font-weight:700;color:#b8cbd5}.brand img{width:56px;height:56px;object-fit:cover;border-radius:12px;border:1px solid #405467}.category{color:#64e4c6;font-size:20px;margin-top:40px;line-height:1.35}h1{font-size:47px;line-height:1.13;letter-spacing:-1.4px;margin:15px 0 20px;max-height:230px;overflow:hidden}.description{font-size:23px;color:#aebfcd;line-height:1.5;margin:0;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.domain{font-size:18px;color:#64e4c6;margin-top:auto}.visual{margin:24px 24px 24px 0;background:#05090f;border:1px solid #2b3848;border-radius:18px;display:flex;align-items:center;justify-content:center;overflow:hidden;padding:14px}.visual img{max-width:100%;max-height:100%;object-fit:contain}.home{position:relative;display:block;padding:0;background:#000}.hero{height:390px;width:100%;object-fit:contain!important}.thumbs{display:flex;gap:10px;justify-content:center;height:178px;margin-top:-5px;padding:0 12px}.thumbs img{width:110px;height:165px;object-fit:contain;border:1px solid #2b3848;background:#080d14;border-radius:5px}.prompt{white-space:pre-wrap;color:#c6d8e3;font-size:23px;line-height:1.5;padding:26px;max-height:540px;overflow:hidden}.pill{display:inline-block;padding:8px 14px;border:1px solid #3c645e;background:#1a3434;color:#64e4c6;font-size:20px;border-radius:24px;margin-top:22px;align-self:flex-start}`;
function html(item) {
  const home = !item;
  const category = home ? 'SOLARFREN’S COLLECTION' : item.category;
  const title = home ? 'Infographic<br>Mega Library' : escape(item.title);
  const description = home ? 'Rust, game systems, reverse engineering, and game mashup concepts.' : escape(item.description);
  const visual = home ? `<div class="visual home"><img class="hero" src="${avatar}"><div class="thumbs">${catalog.slice(0,3).map(i=>`<img src="${dataImage(i.thumbnail)}">`).join('')}</div></div>` : item.thumbnail ? `<div class="visual"><img src="${dataImage(item.thumbnail)}"></div>` : `<div class="visual"><div class="prompt">${escape(fs.readFileSync(path.join(root,item.path),'utf8').slice(0,720))}</div></div>`;
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body><div class="copy"><div class="brand"><img src="${avatar}">INFOGRAPHIC MEGA LIBRARY</div><div class="category">${escape(category)}</div><h1>${title}</h1><p class="description">${description}</p>${home?'<span class="pill">32 infographics · 8 topics</span>':''}<div class="domain">solarfren69420.github.io/infographicmegalibrary</div></div>${visual}</body></html>`;
}
(async () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'infographic-social-'));
  const port = 19228;
  const chrome = spawn('google-chrome',['--headless=new','--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-first-run','--no-default-browser-check',`--user-data-dir=${temporary}/profile`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});
  let ws;
  try {
    let tabs;
    for(let n=0;n<60;n++) {
      try {tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json();break;} catch {await new Promise(r=>setTimeout(r,200));}
    }
    if(!tabs)throw new Error('Chrome did not start');
    ws = new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
    await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
    let serial=0;const pending=new Map();
    ws.addEventListener('message',event=>{const message=JSON.parse(event.data);if(message.id){const p=pending.get(message.id);pending.delete(message.id);message.error?p.reject(message.error):p.resolve(message.result);}});
    const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
    await send('Emulation.setDeviceMetricsOverride',{width:1200,height:630,deviceScaleFactor:1,mobile:false});
    fs.mkdirSync(output,{recursive:true});
    for(const item of [null,...catalog]) {
      const id=item?item.id:'library';const file=path.join(temporary,'card.html');fs.writeFileSync(file,html(item));
      await send('Page.navigate',{url:'file://'+file+'?card='+id});
      // Wait for this document, its images, and layout, rather than screenshotting the previous page.
      await send('Runtime.evaluate',{expression:`new Promise(resolve=>{const check=()=>{if(document.readyState==='complete'&&document.querySelector('h1'))Promise.all([...document.images].map(i=>i.decode())).then(()=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));else setTimeout(check,30);};check();})`,awaitPromise:true});
      const shot=await send('Page.captureScreenshot',{format:'jpeg',quality:90,clip:{x:0,y:0,width:1200,height:630,scale:1}});
      fs.writeFileSync(path.join(output,id+'.jpg'),Buffer.from(shot.data,'base64'));
    }
    console.log(`Rendered ${catalog.length+1} preview images at 1200 × 630.`);
  } finally {if(ws)ws.close();chrome.kill();}
})().catch(error=>{console.error(error);process.exitCode=1});
