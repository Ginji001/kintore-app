# v42 / プログラム版9（2026-11-16）：実績ベースの組み直し＋Epley換算の増量ルール
# 変更内容は 筋トレジム管理_引き継ぎ.md の現行プログラム（2026/11/16〜12/13）を参照。
# - DEFAULT_PROGRAM を version:9 / start:"2026-11-16" にし、全種目の重量を直近実績へ更新
# - 全セット上限達成で増量した種目はEpley換算（四捨五入＋1回）の目標回数から始める
#   金インクライン 25kg×10×3達成→32kg×2回、土ヒップアブダクション 47kg×10×3達成→55kg×5回
# - sw.js の VERSION を v41 から v42 へ
# このパッチはGitHub側で適用済みの内容をMac側へ写すための記録用。
p="kintore-app/index.html";s=open(p,encoding="utf-8").read()
assert 'version:8' in s
s=s.replace('name:"4週間プログラム",start:"2026-09-21",weeks:4,version:8,','name:"4週間プログラム",start:"2026-11-16",weeks:4,version:9,')
open(p,"w",encoding="utf-8").write(s)
q="kintore-app/sw.js";t=open(q,encoding="utf-8").read();assert 'VERSION = "v41"' in t
open(q,"w",encoding="utf-8").write(t.replace('VERSION = "v41"','VERSION = "v42"'));print("ok（重量の差し替えは引き継ぎの現行プログラム表どおりに手で合わせること）")
