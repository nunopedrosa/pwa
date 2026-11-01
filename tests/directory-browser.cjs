/* Local, isolated rendering tests; remote artwork is mocked, no app data accessed. */
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,executablePath}=require('../scripts/browser-test-tools.cjs');
const root=path.resolve(__dirname,'..');
const expected=fs.readFileSync(path.join(root,'apps.txt'),'utf8').split('\n').filter(line=>line.split('#')[0].trim()).length;
const watchdog=setTimeout(()=>{console.error('Directory browser check timed out');process.exit(1);},60000);
const server=http.createServer((req,res)=>{let pathname=new URL(req.url,'http://local').pathname;const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));if(!file.startsWith(root+'/')||!fs.existsSync(file)){res.writeHead(404);return res.end();}const type=file.endsWith('.css')?'text/css':file.endsWith('.svg')?'image/svg+xml':file.endsWith('.jpg')?'image/jpeg':'text/html';res.writeHead(200,{'Content-Type':type,'Cache-Control':'no-store'});fs.createReadStream(file).pipe(res);});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const browser=await chromium.launch({headless:true,executablePath});try{
const context=await browser.newContext({javaScriptEnabled:false});const page=await context.newPage();let remote=[];
await page.route('https://**',route=>{remote.push(route.request().url());assert.equal(route.request().headers()['referer'],undefined);route.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48"><rect width="48" height="48" rx="4" fill="#c4d8e8"/><path d="M14 24h20M24 14v20" stroke="#32546b" stroke-width="3"/></svg>'});});
await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'domcontentloaded'});const links=page.locator('.app-link');assert.equal(await links.count(),expected);
for(const width of [320,700,1280]){await page.setViewportSize({width,height:900});const layout=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,small:Array.from(document.querySelectorAll('.app-link')).some(e=>e.getBoundingClientRect().height<44)}));assert.equal(layout.overflow,false,'page must fit '+width);assert.equal(layout.small,false);}
await page.setViewportSize({width:1280,height:1050});await page.screenshot({path:'/tmp/basecentral-directory-desktop.png',fullPage:true});
await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/basecentral-directory-mobile.png',fullPage:true});
console.log('Layout and screenshots passed');await page.keyboard.press('Tab');assert.match(await page.locator(':focus').textContent(),/Skip to apps/);await page.keyboard.press('Enter');if(expected){await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('class'),'app-link');}
// Blocking all artwork must preserve every named, usable link and page width.
await page.unroute('https://**');await page.route('https://**',r=>r.abort());await page.reload({waitUntil:'domcontentloaded'});assert.equal(await links.count(),expected);if(expected)assert.equal(await links.first().isVisible(),true);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
await page.evaluate(()=>document.documentElement.style.fontSize='200%');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
console.log('PASS directory: '+expected+' links without JS, 320/700/1280 layouts, keyboard, enlarged text, artwork failure and referrer suppression');
}finally{await browser.close();server.closeAllConnections();await new Promise(r=>server.close(r));clearTimeout(watchdog);}})().catch(e=>{console.error(e);server.closeAllConnections();server.close();clearTimeout(watchdog);process.exitCode=1});
