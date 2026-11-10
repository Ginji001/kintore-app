p="kintore-app/index.html";s=open(p,encoding="utf-8").read()
import re
def rep(a,b):
    global s
    assert s.count(a)==1,a[:50];s=s.replace(a,b)
rep("""  try{var au=auEl();if(!au.dataset.ok&&!trackOn()){au.dataset.ok="1";au.src=makeTrack(50);au.muted=true;var pr=au.play();
    var un=function(){au.muted=false;};if(pr&&pr.then) pr.then(function(){au.pause();un();},function(){au.dataset.ok="";un();});else{au.pause();un();}}}catch(e){}
""","")
i=s.index("function playTrack(){");j=s.index("function stopTrack(){")
s=s[:i]+"/* ロック画面の再生表示を出さないため、音声ファイルの再生はしない（2026-11-10、v40）。音は画面がついているときのWeb Audioのみ */\nfunction playTrack(){}\n"+s[j:]
open(p,"w",encoding="utf-8").write(s)
q="kintore-app/sw.js";t=open(q,encoding="utf-8").read();assert 'VERSION = "v39"' in t
open(q,"w",encoding="utf-8").write(t.replace('VERSION = "v39"','VERSION = "v40"'));print("ok")
