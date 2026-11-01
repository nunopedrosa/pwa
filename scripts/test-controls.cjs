const assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
const {chromium,executablePath}=require('./browser-test-tools.cjs');
(async()=>{const browser=await chromium.launch({headless:true,executablePath});try{
const page=await browser.newPage({viewport:{width:320,height:600}});
const file=path.join(__dirname,'../shared/controls/controls.css');const css=fs.existsSync(file)?fs.readFileSync(file,'utf8'):'';
await page.setContent(`<style>body{margin:8px}.box{width:100%}${css}</style><div class="pwa-actions"><button class="pwa-control" id="one">Save</button><select class="pwa-control" id="two"><option>🇬🇧</option></select><button class="pwa-control" hidden id="hidden">Hidden</button></div><div class="box"><button class="pwa-control" id="long">Exportar uma cópia de segurança completa das preferências deste dispositivo</button></div><button class="pwa-control" disabled id="disabled">Disabled</button>`);
const values=await page.evaluate(()=>{const r=id=>document.getElementById(id).getBoundingClientRect();return {one:r('one').height,two:r('two').height,top1:r('one').top,top2:r('two').top,long:r('long').height,hidden:r('hidden').height,overflow:document.documentElement.scrollWidth>innerWidth};});
assert.ok(values.one>=44,'ordinary button must be at least 44px');assert.ok(values.two>=44,'native select must match button');assert.equal(values.top1,values.top2);assert.equal(values.hidden,0);assert.ok(values.long>=44);assert.equal(values.overflow,false,'long labels must wrap');
await page.locator('#one').focus();assert.notEqual(await page.locator('#one').evaluate(e=>getComputedStyle(e).outlineStyle),'none');assert.equal(await page.locator('#disabled').isEnabled(),false);
await page.emulateMedia({media:'print'});assert.ok(await page.locator('#one').evaluate(e=>e.getBoundingClientRect().height)<44,'kit must not change print geometry');console.log('PASS controls: size, alignment, wrapping, hidden/disabled, focus and print isolation');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
