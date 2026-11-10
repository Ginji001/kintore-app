import re
p="kintore-app/index.html";s=open(p,encoding="utf-8").read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
rep("""  if(HK_ON&&day&&day.hk)""","""  if(day&&day.t0) h+='<p class="target" style="margin:-8px 0 16px">総合タイム <b id="totT">'+totText(day)+'</b></p>';
  if(HK_ON&&day&&day.hk)""")
rep("""function doneHtml(day){""","""/* 総合タイム：1セット目の記録から最後のセットの記録まで（記録中は今まで） */
function fmtDur(ms){var s=Math.max(0,Math.floor(ms/1000)),h=Math.floor(s/3600),m=Math.floor(s%3600/60);s%=60;return h?h+":"+pad(m)+":"+pad(s):m+":"+pad(s);}
function totText(day){if(!day||!day.t0) return "";var live=curDate===today&&!dayDone(day);return fmtDur((live?Date.now():(day.t1||day.t0))-day.t0);}
setInterval(function(){
  var el=document.getElementById("totT");if(el){var t=totText(getDay(curDate,false));if(el.textContent!==t) el.textContent=t;}
  var pt=document.getElementById("ppTot");if(pt){var d=getDay(today,false);pt.textContent=d&&d.t0?"総合タイム "+fmtDur(Date.now()-d.t0):"";}
},1000);
function doneHtml(day){""")
rep("""  if(vol) t+="・総挙上量 \"""","""  if(day.t0&&day.t1&&day.t1>day.t0) t+="・総合タイム "+fmtDur(day.t1-day.t0);
  if(vol) t+="・総挙上量 \"""")
rep("""<p class="px" id="ppX"></p>'+""","""<p class="px" id="ppX"></p><p class="pl" id="ppTot" style="margin:-8px 0 12px"></p>'+""")
open(p,"w",encoding="utf-8").write(s)
q="kintore-app/sw.js";t=open(q,encoding="utf-8").read()
assert 'VERSION = "v37"' in t
open(q,"w",encoding="utf-8").write(t.replace('VERSION = "v37"','VERSION = "v38"'))
print("ok")
