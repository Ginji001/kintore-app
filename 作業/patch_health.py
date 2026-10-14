# 記録アプリ：ヘルスケア連携（ショートカット経由）
import pathlib, sys
root = pathlib.Path.home() / "筋トレジム管理" / "kintore-app"
p = root / "index.html"
s = p.read_text(encoding="utf-8")
def rep(old, new):
    global s
    n = s.count(old)
    if n != 1: sys.exit("一致数%d: %r" % (n, old[:80]))
    s = s.replace(old, new)

# 1. 記録画面：その日のヘルスケアの数値
rep("  h+='<p class=\"phase\">'+ph.join(\"　\")+\"</p>\";\n",
    "  h+='<p class=\"phase\">'+ph.join(\"　\")+\"</p>\";\n  if(day&&day.hk) h+='<p class=\"target\" style=\"margin:-8px 0 16px\">'+esc(hkText(day.hk))+\"</p>\";\n")

# 2. ボタン
rep("  h+='<button class=\"btn\" data-act=\"openAdd\">種目を追加</button>';\n",
    "  h+='<button class=\"btn\" data-act=\"openAdd\">種目を追加</button>';\n"
    "  if(curDate===today){\n"
    "    if(hkPending()) h+='<button class=\"btn solid\" data-act=\"hkPaste\">ヘルスケアの数値を取り込む</button>';\n"
    "    h+='<button class=\"btn\" data-act=\"hkRun\">'+(dayHasLift(day)&&!day.hkSent?\"ヘルスケアに記録\":\"ヘルスケアから読み込む\")+'</button>';\n"
    "  }\n")

# 3. カレンダー：体重の変化
rep("  h+='<p class=\"sub\">'+(SHOW_RUN?\"活動日 \"+st.active+\"日\":\"今月のセット数 \"+st.sets)+\"</p>\";\n",
    "  h+='<p class=\"sub\">'+(SHOW_RUN?\"活動日 \"+st.active+\"日\":\"今月のセット数 \"+st.sets)+weightTrend(statYm)+\"</p>\";\n")

# 4. 関数
rep("/* ---------- 休憩タイマー", r'''/* ---------- ヘルスケア連携（iPhoneのショートカット「筋トレ連携」経由） ----------
   送る：その日の筋トレを {"start","min"} にしてショートカットへ渡し、ワークアウトとして記録してもらう
   受け取る：ショートカットが体重・体脂肪率・歩数・アクティブエネルギーをクリップボードにコピー → 「取り込む」で読む */
var HK_SHORTCUT="筋トレ連携";
function hkPending(){try{return !!localStorage.getItem("kintore:hkPending");}catch(e){return false;}}
function hkSetPending(v){try{if(v) localStorage.setItem("kintore:hkPending","1"); else localStorage.removeItem("kintore:hkPending");}catch(e){}}
function hkNum(v){
  if(v==null) return null;
  var m=String(v).replace(/[,，]/g,"").match(/-?\d+(\.\d+)?/);
  return m?Number(m[0]):null;
}
function hkText(hk){
  var a=[];
  if(hk.w!=null) a.push("体重 "+hk.w+"kg");
  if(hk.bf!=null) a.push("体脂肪率 "+hk.bf+"%");
  if(hk.st!=null) a.push("歩数 "+Math.round(hk.st).toLocaleString()+"歩");
  if(hk.kcal!=null) a.push("活動 "+Math.round(hk.kcal).toLocaleString()+"kcal");
  return a.join("・");
}
function hkParse(txt){
  var j=JSON.parse(String(txt).trim()),o={};
  var w=hkNum(j.w),bf=hkNum(j.bf),st=hkNum(j.st),kc=hkNum(j.kcal);
  if(w!=null&&w>0) o.w=Math.round(w*10)/10;
  if(bf!=null&&bf>0){if(bf<=1) bf=bf*100;o.bf=Math.round(bf*10)/10;}
  if(st!=null&&st>=0) o.st=Math.round(st);
  if(kc!=null&&kc>=0) o.kcal=Math.round(kc);
  if(!Object.keys(o).length) throw new Error("数値が見つかりません");
  return o;
}
function hkRun(){
  var day=getDay(today,true),payload={};
  if(dayHasLift(day)&&!day.hkSent){
    var t1=day.t1||Date.now(),t0=day.t0||(t1-60*60000);
    var min=Math.max(10,Math.round((t1-t0)/60000)+3),st=new Date(t0);
    payload={start:st.getFullYear()+"/"+pad(st.getMonth()+1)+"/"+pad(st.getDate())+" "+pad(st.getHours())+":"+pad(st.getMinutes()),min:min};
    day.hkSent=Date.now();saveDay(today);
  }
  hkSetPending(true);renderRec();
  location.href="shortcuts://run-shortcut?name="+encodeURIComponent(HK_SHORTCUT)+"&input=text&text="+encodeURIComponent(JSON.stringify(payload));
}
function hkApply(txt){
  var o;
  try{o=hkParse(txt);}catch(e){alert("ヘルスケアの数値を読み取れませんでした。ショートカット「"+HK_SHORTCUT+"」を実行してから、もう一度押してください。");return;}
  var day=getDay(today,true);o.at=Date.now();day.hk=o;saveDay(today);hkSetPending(false);renderRec();
}
function hkPaste(){
  var fallback=function(){var t=prompt("ショートカットがコピーした内容を貼り付けてください","");if(t) hkApply(t);};
  if(navigator.clipboard&&navigator.clipboard.readText) navigator.clipboard.readText().then(hkApply,fallback);
  else fallback();
}
function weightTrend(ym){
  var m=monthDoc(ym),ks=Object.keys(m.days||{}).filter(function(k){return ymOf(k)===ym&&m.days[k].hk&&m.days[k].hk.w!=null;}).sort();
  if(!ks.length) return "";
  var a=m.days[ks[0]].hk.w,b=m.days[ks[ks.length-1]].hk.w,df=Math.round((b-a)*10)/10;
  return "　体重 "+b+"kg"+(ks.length>1?"（月初から "+(df>0?"+":df<0?"−":"±")+Math.abs(df)+"kg）":"");
}

/* ---------- 休憩タイマー''')

# 5. 操作
rep("  if(a===\"restStop\"){stopRest();return;}\n",
    "  if(a===\"restStop\"){stopRest();return;}\n  if(a===\"hkRun\"){hkRun();return;}\n  if(a===\"hkPaste\"){hkPaste();return;}\n")

# 6. 筋トレの開始・終了時刻（今日の回数入力から）
rep("  if(f===\"r\"){var day=getDay(curDate,true);day.entries[+t.dataset.i].sets[+t.dataset.j].r=t.value===\"\"?\"\":Number(t.value);saveDay(curDate);}",
    "  if(f===\"r\"){var day=getDay(curDate,true);day.entries[+t.dataset.i].sets[+t.dataset.j].r=t.value===\"\"?\"\":Number(t.value);\n"
    "    if(curDate===today&&Number(t.value)>0){var nw=Date.now();if(!day.t0) day.t0=nw;day.t1=nw;}\n"
    "    saveDay(curDate);}")

p.write_text(s, encoding="utf-8")
sw = root / "sw.js"; t = sw.read_text(encoding="utf-8")
assert 'const VERSION = "v20";' in t
sw.write_text(t.replace('const VERSION = "v20";','const VERSION = "v21";'), encoding="utf-8")
rd = root / "README.md"; r = rd.read_text(encoding="utf-8")
old = "- カレンダー：月の筋トレ日・ラン日・活動日数\n"
r = r.replace(old, "- ヘルスケア連携：iPhoneのショートカット「筋トレ連携」経由。記録画面の「ヘルスケアに記録」で今日の筋トレ（最初と最後の回数入力の時刻から開始時刻と分数）をワークアウトとして記録し、体重・体脂肪率・歩数・アクティブエネルギーをクリップボード経由で取り込む（「ヘルスケアの数値を取り込む」）。取り込んだ数値は日ごとに保存し、カレンダーに月の体重の変化を出す\n" + old)
rd.write_text(r, encoding="utf-8")
print("OK")
