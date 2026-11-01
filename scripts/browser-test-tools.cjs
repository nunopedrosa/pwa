/* Optional development tools only; never shipped as application runtime. */
const fs=require('fs'),path=require('path'),os=require('os');
let playwright;
if(process.env.PLAYWRIGHT_PATH)playwright=require(process.env.PLAYWRIGHT_PATH);
else{try{playwright=require('playwright');}catch{playwright=require(path.resolve(__dirname,'../../doctools/node_modules/playwright'));}}
let executablePath=process.env.CHROMIUM_PATH;
if(!executablePath){
 const cache=path.join(os.homedir(),process.platform==='darwin'?'Library/Caches/ms-playwright':'.cache/ms-playwright');
 if(fs.existsSync(cache)){
  const releases=fs.readdirSync(cache).filter(n=>/^chromium-\d+$/.test(n)).sort((a,b)=>Number(b.split('-')[1])-Number(a.split('-')[1]));
  for(const release of releases){
   for(const suffix of ['chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing','chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing','chrome-linux64/chrome','chrome-linux/chrome']){
    const candidate=path.join(cache,release,suffix);if(fs.existsSync(candidate)){executablePath=candidate;break;}
   }
   if(executablePath)break;
  }
 }
}
module.exports={chromium:playwright.chromium,executablePath};
