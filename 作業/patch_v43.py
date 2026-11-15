# v43（2026-11-16）：トレーニング開始ボタン
# - 記録画面の今日（トレーニング日・未開始のときだけ）に「トレーニング開始」ボタン（btn solid）を表示
# - 押すと day.t0 に現在時刻を記録し保存。総合タイムは t0 から数える（従来は1セット目入力で自動記録、それも予備として残す）
# - 開始後は総合タイムの横に開始時刻（H:MM）を表示。「行けなかった」の日はボタンを出さない
# - sw.js の VERSION を v42 から v43 へ
# 検証：Chromiumでボタンの表示、クリックで総合タイム表示に切り替わること、再読み込み後も保持されることを確認済み
p="kintore-app/index.html";s=open(p,encoding="utf-8").read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:50];s=s.replace(a,b)
rep('''  if(day&&day.t0) h+='<p class="target" style="margin:-8px 0 16px">総合タイム <b id="totT">'+totText(day)+'</b></p>';''',
'''  if(day&&day.t0){var st0=new Date(day.t0);h+='<p class="target" style="margin:-8px 0 16px">総合タイム <b id="totT">'+totText(day)+'</b>（開始 '+st0.getHours()+":"+pad(st0.getMinutes())+'）</p>';}
  else if(curDate===today&&plan&&!(day&&day.rest)) h+='<p style="margin:-8px 0 16px"><button class="btn solid" data-act="start">トレーニング開始</button></p>';''')
rep('''  if(a==="run"||a==="rest"){''',
'''  if(a==="start"){
    day=getDay(curDate,true);
    if(!day.t0) day.t0=Date.now();
    saveDay(curDate);renderRec();return;
  }
  if(a==="run"||a==="rest"){''')
open(p,"w",encoding="utf-8").write(s)
q="kintore-app/sw.js";t=open(q,encoding="utf-8").read();assert 'VERSION = "v42"' in t
open(q,"w",encoding="utf-8").write(t.replace('VERSION = "v42"','VERSION = "v43"'));print("ok")
