const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/Users/sasamorimasahiro/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell'});
const p=await b.newPage();p.on('pageerror',e=>console.log('PE',e));
await p.goto('http://localhost:8766/test.html');
const names=fs.readdirSync('/tmp/pwt/www/img').filter(f=>f.endsWith('.jpg')).sort();
const r=await p.evaluate(n=>run(n),names);fs.writeFileSync('/tmp/pwt/ocr_out.json',JSON.stringify(r,null,0).replace(/\},"/g,'},\n"'));await b.close();console.log('done');})();
