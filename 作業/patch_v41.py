p="kintore-app/index.html";s=open(p,encoding="utf-8").read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:50];s=s.replace(a,b)
# 種目一覧：シーテッドロー（プレート式・共通の段階）を追加
rep('["シーテッドケーブルロウ","背中","回",1],["ディップチンアシスト","背中","回",1],',
    '["シーテッドロー","背中","回",1],["シーテッドケーブルロウ","背中","回",1],["ディップチンアシスト","背中","回",1],')
# 火曜：6種目に（5種目の枠は廃止）
rep('items:[["ラットプルダウン",32,"8-10",3],["シーテッドケーブルロウ",32,"8-10",3],',
    'items:[["ラットプルダウン",32,"8-10",3],["シーテッドロー",20,"10",3],["シーテッドケーブルロウ",32,"8-10",3],')
rep('name:"4週間プログラム",start:"2026-09-21",weeks:4,version:7,','name:"4週間プログラム",start:"2026-09-21",weeks:4,version:8,')
# 種目のコツ
rep(' "シーテッドケーブルロウ":["背すじを伸ばし',
    ' "シーテッドロー":["胸パッドを胸の中央に合わせ、腕をしっかり伸ばして始める","肩甲骨を寄せたまま、両腕が胴体に付くまで引く"],\n "シーテッドケーブルロウ":["背すじを伸ばし')
# プログラム入れ替え時に、足りない種目も設定へ追加（既存の種目・記録は消さない）
rep('st.program=JSON.parse(JSON.stringify(DEFAULT_PROGRAM));return true;}',
    'st.program=JSON.parse(JSON.stringify(DEFAULT_PROGRAM));\n    if(st.exercises){DEFAULT_EX.forEach(function(e){if(!st.exercises.some(function(x){return x.n===e.n;})) st.exercises.push({n:e.n,p:e.p,u:e.u,m:e.m});});}\n    return true;}')
open(p,"w",encoding="utf-8").write(s)
q="kintore-app/sw.js";t=open(q,encoding="utf-8").read();assert 'VERSION = "v40"' in t
open(q,"w",encoding="utf-8").write(t.replace('VERSION = "v40"','VERSION = "v41"'));print("ok")
