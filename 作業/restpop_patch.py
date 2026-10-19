import re,pathlib
p=pathlib.Path.home()/"筋トレジム管理/kintore-app/index.html"
s=p.read_text()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:60],s.count(a))
    s=s.replace(a,b)

# CSS
rep('body.resting main{padding-bottom:200px}',
'''body.resting main{padding-bottom:200px}
.restbar{cursor:pointer}
.restpop{position:fixed;inset:0;z-index:30;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:20px}
.restpop[hidden]{display:none}
.restpop .card{width:100%;max-width:340px;background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:20px 20px 18px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.35)}
.restpop .pl{font-size:13px;color:var(--mute);margin:0}
.restpop .pt{font-family:"Jost",sans-serif;font-size:76px;font-weight:300;line-height:1.05;letter-spacing:-.02em;margin:6px 0 2px}
.restpop .pt.end{color:var(--accent)}
.restpop .px{font-size:13px;color:var(--mute);line-height:1.5;min-height:2.9em;margin:0 0 14px}
.restpop .adj{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}
.restpop .adj div{border:1px solid var(--line);border-radius:12px;padding:8px 6px}
.restpop .adj span{display:block;font-size:12px;color:var(--mute);margin-bottom:6px}
.restpop .adj button{background:var(--panel);border:1px solid var(--line);border-radius:999px;width:52px;height:38px;font-size:15px;color:var(--ink);margin:0 2px}
.restpop .pa{display:flex;gap:10px;justify-content:center}
.rsedit{display:grid;grid-template-columns:1fr 78px 78px;gap:8px;align-items:center;font-size:14px}
.rsedit select{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:5px 6px;font-size:14px;width:100%}''')

# popup element
rep('<main id="app"></main>',
'<main id="app"></main>\n<div class="restpop" id="restpop" role="dialog" aria-modal="true" aria-label="休憩タイマー" hidden><div class="card" id="restcard"></div></div>')

# rest seconds from settings
rep('function restSec(name){var p=exInfo(name).p;return (p==="肩"||p==="腕"||p==="腹・体幹")?75:150;}',
'''var REST_DEF={main:150,light:75};
function restKind(name){var p=exInfo(name).p;return (p==="肩"||p==="腕"||p==="腹・体幹")?"light":"main";}
function restDef(k){var st=settings(),r=st&&st.rest;var v=r&&Number(r[k]);return v>0?v:REST_DEF[k];}
function restSec(name){return restDef(restKind(name));}''')

rep('clearInterval(rest.iv);rest.iv=setInterval(drawRest,250);drawRest();\n}',
'clearInterval(rest.iv);rest.iv=setInterval(drawRest,250);rest.pop=true;drawRest();\n}')
rep('function stopRest(){clearInterval(rest.iv);rest.iv=null;rest.end=0;drawRest();}',
'''function stopRest(){clearInterval(rest.iv);rest.iv=null;rest.end=0;rest.pop=false;drawRest();}
function restAdj(sec){if(!rest.end) return;var now=Date.now();rest.end=Math.max(now+1000,Math.max(rest.end,now)+sec*1000);rest.buzz=false;drawRest();}
function fmtMS(s){return Math.floor(s/60)+":"+pad(s%60);}''')

# drawRest: hide popup when no rest
rep('if(!rest.end){el.hidden=true;document.body.classList.remove("resting");return;}',
'''var pp=document.getElementById("restpop");
  if(!rest.end){el.hidden=true;if(pp) pp.hidden=true;document.body.classList.remove("resting");return;}''')
rep('''if(!el.firstChild) el.innerHTML='<span class="rt" id="rtT"></span>''',
'''if(!el.firstChild) el.innerHTML='<span class="rt" id="rtT" data-act="restOpen"></span>''')
rep('''<span class="tip"><b id="rtL"></b><span id="rtX"></span></span>'+''',
'''<span class="tip" data-act="restOpen"><b id="rtL"></b><span id="rtX"></span></span>'+''')
rep('''  el.hidden=false;document.body.classList.add("resting");
}''',
'''  el.hidden=!!rest.pop;document.body.classList.toggle("resting",!rest.pop);
  if(pp){
    var cd=document.getElementById("restcard");
    if(!cd.firstChild) cd.innerHTML='<p class="pl" id="ppL"></p><div class="pt" id="ppT" role="timer" aria-live="off"></div><p class="px" id="ppX"></p>'+
      '<div class="adj"><div><span>分</span><button data-act="restAdj" data-n="-60" aria-label="1分減らす">−</button><button data-act="restAdj" data-n="60" aria-label="1分増やす">＋</button></div>'+
      '<div><span>秒</span><button data-act="restAdj" data-n="-10" aria-label="10秒減らす">−10</button><button data-act="restAdj" data-n="10" aria-label="10秒増やす">＋10</button></div></div>'+
      '<div class="pa"><button class="btn" data-act="restMin">小さくする</button><button class="btn solid" data-act="restStop">終了</button></div>';
    document.getElementById("ppT").textContent=left>0?fmtMS(s):"GO";
    document.getElementById("ppT").className="pt"+(left>0?"":" end");
    document.getElementById("ppL").textContent=left>0?"休憩中・"+rest.ex:"次のセットへ";
    document.getElementById("ppX").textContent=rest.tip;
    pp.hidden=!rest.pop;
  }
}
document.getElementById("restpop").addEventListener("click",function(ev){if(ev.target.id==="restpop"){rest.pop=false;drawRest();}});''')

# actions
rep('if(a==="restStop"){stopRest();return;}',
'''if(a==="restStop"){stopRest();return;}
  if(a==="restAdj"){restAdj(+b.dataset.n);return;}
  if(a==="restMin"){rest.pop=false;drawRest();return;}
  if(a==="restOpen"){if(rest.end){rest.pop=true;drawRest();}return;}''')
rep('document.addEventListener("keydown",function(ev){if(ev.key==="Escape") closeSheet();});',
'document.addEventListener("keydown",function(ev){if(ev.key==="Escape"){closeSheet();if(rest.pop){rest.pop=false;drawRest();}}});')

# settings UI
rep('''  h+='<section class="sec"><h2>種目と部位</h2>''',
'''  var rsRow=function(k,lb){var v=restDef(k),m=Math.floor(v/60),sc=v%60,o1="",o2="";
    for(var i=0;i<=10;i++) o1+='<option value="'+i+'"'+(i===m?" selected":"")+'>'+i+'分</option>';
    for(var j=0;j<60;j+=5) o2+='<option value="'+j+'"'+(j===sc?" selected":"")+'>'+j+'秒</option>';
    if(sc%5) o2+='<option value="'+sc+'" selected>'+sc+'秒</option>';
    return '<span>'+lb+'</span><select data-f="rsm" data-k="'+k+'" aria-label="'+lb+'の分">'+o1+'</select><select data-f="rss" data-k="'+k+'" aria-label="'+lb+'の秒">'+o2+'</select>';};
  h+='<section class="sec"><h2>休憩タイマー</h2><p>セットの回数を入れると、休憩タイマーが別窓で開きます。最初の時間をここで決めます。</p><div class="rsedit">'+
     rsRow("main","主要種目")+rsRow("light","肩・腕・腹")+'</div></section>';
  h+='<section class="sec"><h2>種目と部位</h2>''')

rep('''  if(f==="r"){
    var rd=getDay(curDate,false)''',
'''  if(f==="rsm"||f==="rss"){
    var st=settings(),k=t.dataset.k,cur=restDef(k);if(!st.rest) st.rest={};
    var m=f==="rsm"?Number(t.value):Math.floor(cur/60),sc=f==="rss"?Number(t.value):cur%60,tot=m*60+sc;
    if(tot<5){tot=5;}
    st.rest[k]=tot;markDirty("settings");return;
  }
  if(f==="r"){
    var rd=getDay(curDate,false)''')
p.write_text(s)
sw=p.with_name("sw.js");t=sw.read_text();assert 'const VERSION = "v31";' in t
sw.write_text(t.replace('const VERSION = "v31";','const VERSION = "v32";'))
print("ok")
