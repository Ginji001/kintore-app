const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/Users/sasamorimasahiro/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell'});
const errs=[];const p=await b.newPage({viewport:{width:390,height:844}});p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
p.on('dialog',d=>{errs.push('dialog:'+d.message());d.accept();});
await p.goto('http://localhost:8765/');await p.waitForTimeout(1200);
const body=JSON.parse(fs.readFileSync('/tmp/body_live.json','utf8'));delete body.days['2026-10-13'];
await p.evaluate(bd=>localStorage.setItem('kintore:body',JSON.stringify(bd)),body);await p.reload();await p.waitForTimeout(1200);
await p.click('button[data-tab="body"]');await p.waitForTimeout(300);
await p.screenshot({path:'/tmp/pwt/e2e0.png'});
await p.setInputFiles('#bfile',['IMG_0324','IMG_0325','IMG_0326','IMG_0327','IMG_0328'].map(n=>'/tmp/pwt/www/img/'+n+'.jpg'));
await p.waitForSelector('#bd_date',{timeout:180000});
const vals=await p.evaluate(()=>{const o={};document.querySelectorAll('.bform input,.bform select').forEach(e=>o[e.id]=e.value);o.note=(document.querySelector('.bform .hint')||{}).textContent;return o;});
console.log(JSON.stringify(vals));
await p.screenshot({path:'/tmp/pwt/e2e1.png',fullPage:true});
await p.fill('#bd_date','2026-10-13');await p.fill('#bd_time','10:11');
await p.click('button[data-act="bsave"]');await p.waitForTimeout(1600);
const saved=await p.evaluate(()=>JSON.parse(localStorage.getItem('kintore:body')||'null'));
console.log('msg',await p.textContent('#bmsg'));
await p.screenshot({path:'/tmp/pwt/e2e2.png'});
// re-open from idb after reload
await p.reload();await p.waitForTimeout(1200);await p.click('button[data-tab="body"]');await p.waitForTimeout(400);
console.log('after reload has 10/13:',(await p.textContent('#app')).includes('2026/10/13'));
// edit flow
await p.click('.brow[data-d="2026-10-13"]');await p.waitForTimeout(300);console.log('edit w=',await p.inputValue('#bd_w'));
await p.fill('#bd_date','2026-10-14');await p.click('button[data-act="bsave"]');await p.waitForTimeout(1600);
let t=await p.textContent('#app');console.log('moved: has10/14',t.includes('2026/10/14'),'has10/13',t.includes('2026/10/13'));
await p.click('.brow[data-d="2026-10-14"]');await p.waitForTimeout(300);await p.click('button[data-act="bdel"]');await p.waitForTimeout(1600);
await p.reload();await p.waitForTimeout(1200);await p.click('button[data-tab="body"]');await p.waitForTimeout(400);
t=await p.textContent('#app');console.log('deleted: has10/14',t.includes('2026/10/14'),'count',(t.match(/回目/)||[''])[0],t.match(/（\d+回目）/)[0]);
await p.click('button[data-act="bmanual"]');await p.waitForTimeout(300);console.log('manual date',await p.inputValue('#bd_date'),'w',await p.inputValue('#bd_w'));
for(const t2 of ['rec','cal','parts','ex','more','body']){await p.click(`button[data-tab="${t2}"]`);await p.waitForTimeout(300);}
console.log('ERR',JSON.stringify(errs));await b.close();})();
