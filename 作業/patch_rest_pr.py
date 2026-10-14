# 記録アプリ：休憩タイマー＋コツ、自己ベスト、完了表示を追加（UIは既存のまま）
import pathlib, sys
root = pathlib.Path.home() / "筋トレジム管理" / "kintore-app"
p = root / "index.html"
s = p.read_text(encoding="utf-8")

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("一致数が%dです: %r" % (n, old[:80]))
    s = s.replace(old, new)

# A. CSS
rep('@media (prefers-reduced-motion: reduce)', '''/* 休憩タイマー */
.restbar{max-width:520px;margin:0 auto;display:flex;align-items:center;gap:12px;padding:10px 22px;border-bottom:1px solid var(--line)}
.restbar[hidden]{display:none}
.restbar .rt{font-family:"Jost",sans-serif;font-size:24px;font-weight:400;min-width:60px;line-height:1}
.restbar .rt.end{color:var(--accent)}
.restbar .tip{flex:1;font-size:12.5px;color:var(--mute);line-height:1.45}
.restbar .tip b{display:block;color:var(--ink);font-weight:500;font-size:12px}
.restbar .rbtn{display:flex;gap:6px}
body.resting main{padding-bottom:200px}
@media (prefers-reduced-motion: reduce)''')

# B. タイマーの置き場所（下のタブの上）
rep('<nav class="tabs" aria-label="画面切り替え"><div class="inr">',
    '<nav class="tabs" aria-label="画面切り替え"><div class="restbar" id="restbar" role="timer" hidden></div><div class="inr">')

# C. 種目ごとの自己ベスト
rep("    if(e.prev) tgt+='<br>前回 '+esc(e.prev);\n",
    """    if(e.prev) tgt+='<br>前回 '+esc(e.prev);
    var pb=info.m?bestBefore(e.ex,curDate):null,nb=info.m?bestOf(e.ex,[e]):null;
    if(pb) tgt+='<br>自己ベスト '+pb.w+"kg × "+pb.r+"回";
    if(pb&&nb&&better(e.ex,nb,pb)) tgt+='<br><span class="upnote">★ 自己ベスト更新 '+nb.w+"kg × "+nb.r+"回</span>";
""")

# D. 全セット入力で完了表示
rep("  h+='<div class=\"actions\">';\n  if(plan&&!entries.length)",
    "  h+=doneHtml(day);\n  h+='<div class=\"actions\">';\n  if(plan&&!entries.length)")
rep("  h+='<p class=\"status\" id=\"status\">'+esc(statusText())+\"</p>\";\n  app.innerHTML=h;\n}\n\n/* ---------- カレンダー",
    "  h+='<p class=\"status\" id=\"status\">'+esc(statusText())+\"</p>\";\n  app.innerHTML=h;\n  recShown=recSig();\n}\n\n/* ---------- カレンダー")

# E. 関数
rep("/* ---------- イベント ---------- */", r'''/* ---------- 自己ベスト・完了 ---------- */
var recShown="";
function setsOk(e){return doneSets(e).filter(function(s){return s.w!==""&&s.w!=null&&!isNaN(Number(s.w));});}
/* a が b より上か（アシスト系は軽いほど上） */
function better(name,a,b){
  if(!a) return false;if(!b) return true;
  if(a.w!==b.w) return ASSIST.indexOf(name)>=0?a.w<b.w:a.w>b.w;
  return a.r>b.r;
}
function bestOf(name,entries){
  var best=null;
  (entries||[]).forEach(function(e){if(e.ex!==name) return;setsOk(e).forEach(function(s){var c={w:Number(s.w),r:Number(s.r)};if(better(name,c,best)) best=c;});});
  return best;
}
function bestBefore(name,before){
  var best=null;
  Object.keys(docs).forEach(function(n){
    if(n.indexOf("m-")!==0||!docs[n]||!docs[n].days) return;
    var days=docs[n].days;
    Object.keys(days).forEach(function(k){if(k>=before) return;var b=bestOf(name,days[k].entries);if(better(name,b,best)) best=b;});
  });
  return best;
}
function dayDone(day){
  var es=(day&&day.entries)||[];
  return es.length>0&&es.every(function(e){return (e.sets||[]).length>0&&e.sets.every(function(s){return s.r!==""&&s.r!=null&&Number(s.r)>0;});});
}
function volOf(name,sets){
  if(ASSIST.indexOf(name)>=0||!exInfo(name).m) return 0;
  return sets.reduce(function(t,s){var w=Number(s.w),r=Number(s.r);return t+(isNaN(w)||isNaN(r)?0:w*r);},0);
}
function prList(day){
  return ((day&&day.entries)||[]).filter(function(e){
    if(!exInfo(e.ex).m) return false;
    var pb=bestBefore(e.ex,curDate),nb=bestOf(e.ex,[e]);return !!pb&&better(e.ex,nb,pb);
  });
}
function doneHtml(day){
  if(!dayDone(day)) return "";
  var sets=0,vol=0,pv=0,hasPrev=true;
  day.entries.forEach(function(e){
    var ds=doneSets(e),v=volOf(e.ex,ds);sets+=ds.length;vol+=v;
    if(v){var l=findLast(e.ex,curDate,true);if(l) pv+=volOf(e.ex,doneSets(l.entry)); else hasPrev=false;}
  });
  var t="<b>完了</b>　"+day.entries.length+"種目・"+sets+"セット";
  if(vol) t+="・総挙上量 "+vol.toLocaleString()+"kg";
  if(vol&&hasPrev&&pv){var df=vol-pv;t+="（前回比 "+(df>0?"+":df<0?"−":"±")+Math.abs(df).toLocaleString()+"kg）";}
  var prs=prList(day);
  if(prs.length) t+='<br><span class="upnote">★ 自己ベスト更新：'+prs.map(function(e){return esc(e.ex);}).join("、")+"</span>";
  return '<p class="phase">'+t+"</p>";
}
function recSig(){
  var day=getDay(curDate,false);if(!day) return "";
  return (dayDone(day)?"1":"0")+prList(day).map(function(e){var b=bestOf(e.ex,[e]);return e.ex+b.w+"x"+b.r;}).join("|");
}

/* ---------- 休憩タイマー（セットの回数を入れると始まる） ---------- */
var TIPS={
 "チェストプレス":["肩甲骨を寄せて下げたまま押す","グリップは胸の中央の高さに合わせる","押し切っても肘は伸ばしきらない"],
 "インクラインチェストプレス":["胸の上部を意識して斜め上へ押す","肩がすくまないよう首を長く保つ"],
 "ペックデッキフライ":["肘の角度は最後まで固定","胸の前で一瞬止めて絞る","戻すときもゆっくり"],
 "アシストディップス":["上体をやや前に倒すと胸に効く","肩が痛くならない深さまで下ろす"],
 "ラットプルダウン":["胸を張ってバーを鎖骨に向けて引く","腕ではなく肘を下へ引くイメージ","反動を使わず、戻しはゆっくり"],
 "シーテッドケーブルロウ":["背すじを伸ばし、肩甲骨を寄せてから引く","上体を後ろに倒して引かない"],
 "ディップチンアシスト":["肩を下げてから引き始める","胸をバーに近づけるつもりで引く"],
 "ショルダープレス":["腰を反らさず背もたれに付ける","耳の横を通るように真上へ押す"],
 "リアデルトフライ":["肩をすくめず、腕を横へ大きく開く","軽めの重さで肩の後ろを感じる"],
 "アームカール":["肘の位置を動かさない","下ろしきって伸ばしてから次の1回"],
 "レッグプレス":["膝はつま先と同じ向き","お尻が浮かない深さまで下ろす","膝を伸ばしきってロックしない"],
 "シーテッドレッグカール":["膝をマシンの回転軸に合わせる","曲げきったところで一瞬止める"],
 "ヒップスラスト":["あごを引き、腰を反らさずに上げる","上で1秒お尻を締める"],
 "レッグエクステンション":["膝をマシンの回転軸に合わせる","伸ばしきって太ももの前を締める"],
 "アブドミナルクランチ":["背中を丸めて、みぞおちを縮める","息を吐きながら縮める"],
 "ヒップアブダクション":["上体を少し前に倒すとお尻に効きやすい","開いたところで1秒止める"],
 "ヒップアダクション":["反動を使わず、閉じるときに内ももを締める"]
};
var TIPS_ANY=["休憩中に水を一口","次のセットも同じフォーム・同じテンポで"];
var rest={end:0,ex:"",tip:"",iv:null,buzz:false};
function restSec(name){var p=exInfo(name).p;return (p==="肩"||p==="腕"||p==="腹・体幹")?75:150;}
function startRest(name){
  var l=TIPS[name]||TIPS_ANY;
  rest.ex=name;rest.end=Date.now()+restSec(name)*1000;rest.tip=l[Math.floor(Math.random()*l.length)];rest.buzz=false;
  clearInterval(rest.iv);rest.iv=setInterval(drawRest,250);drawRest();
}
function stopRest(){clearInterval(rest.iv);rest.iv=null;rest.end=0;drawRest();}
function drawRest(){
  var el=document.getElementById("restbar");if(!el) return;
  if(!rest.end){el.hidden=true;document.body.classList.remove("resting");return;}
  var left=Math.ceil((rest.end-Date.now())/1000);
  if(left<=-20){stopRest();return;}
  if(left<=0&&!rest.buzz){rest.buzz=true;try{if(navigator.vibrate) navigator.vibrate([200,100,200]);}catch(e){}}
  if(!el.firstChild) el.innerHTML='<span class="rt" id="rtT"></span><span class="tip"><b id="rtL"></b><span id="rtX"></span></span>'+
    '<span class="rbtn"><button class="mini" data-act="restAdd" aria-label="休憩を30秒延ばす">+30</button><button class="mini" data-act="restStop" aria-label="休憩を終える">×</button></span>';
  var s=Math.max(0,left);
  document.getElementById("rtT").textContent=left>0?Math.floor(s/60)+":"+pad(s%60):"GO";
  document.getElementById("rtT").className="rt"+(left>0?"":" end");
  document.getElementById("rtL").textContent=left>0?"休憩中・"+rest.ex:"次のセットへ";
  document.getElementById("rtX").textContent=rest.tip;
  el.hidden=false;document.body.classList.add("resting");
}
document.addEventListener("visibilitychange",function(){if(document.visibilityState==="visible") drawRest();});

/* ---------- イベント ---------- */''')

# F. 操作
rep("  var a=b.dataset.act,i=+b.dataset.i,j=+b.dataset.j,day;\n",
    "  var a=b.dataset.act,i=+b.dataset.i,j=+b.dataset.j,day;\n"
    "  if(a===\"restAdd\"){rest.end=Math.max(rest.end,Date.now())+30000;rest.buzz=false;drawRest();return;}\n"
    "  if(a===\"restStop\"){stopRest();return;}\n")
rep("app.addEventListener(\"change\",function(ev){\n  var t=ev.target,f=t.dataset.f;if(!f) return;\n",
    "app.addEventListener(\"change\",function(ev){\n  var t=ev.target,f=t.dataset.f;if(!f) return;\n"
    "  if(f===\"r\"){\n"
    "    var rd=getDay(curDate,false),re=rd&&rd.entries[+t.dataset.i];\n"
    "    if(re&&curDate===today&&t.value!==\"\"&&Number(t.value)>0) startRest(re.ex);\n"
    "    if(recSig()!==recShown) sync.repaint();\n"
    "    return;\n"
    "  }\n")

# G. 自己ベスト用に全月を読み込む
rep("  if(view===\"rec\") need.push(loadMonth(ymOf(curDate)),loadMonth(addMonths(ymOf(curDate),-1)),loadMonth(addMonths(ymOf(curDate),-2)));",
    "  if(view===\"rec\") need=need.concat(allMonthKeys().concat([ymOf(curDate),addMonths(ymOf(curDate),-1),addMonths(ymOf(curDate),-2)]).filter(function(k,i,a){return a.indexOf(k)===i;}).map(loadMonth));")

p.write_text(s, encoding="utf-8")

sw = root / "sw.js"
t = sw.read_text(encoding="utf-8")
assert 'const VERSION = "v19";' in t
sw.write_text(t.replace('const VERSION = "v19";', 'const VERSION = "v20";'), encoding="utf-8")

rd = root / "README.md"
r = rd.read_text(encoding="utf-8")
old = "- カレンダー：月の筋トレ日・ラン日・活動日数\n"
assert r.count(old) == 1
r = r.replace(old, "- 休憩タイマー：今日の記録でセットの回数を入れると休憩タイマー（主要種目2分30秒、肩・腕・腹は75秒）が始まり、種目ごとのコツを1つ表示する。＋30で延長、×で終了\n- 自己ベスト：種目ごとに過去の最高（重量→回数の順。アシスト系は軽いほど上）を表示し、更新したら★で知らせる\n- 完了表示：その日の全セットを入れると、種目数・セット数・総挙上量（前回の同じメニューとの差）・自己ベスト更新をまとめて表示する\n" + old)
rd.write_text(r, encoding="utf-8")
print("OK")
