import fitz, os
base = os.path.expanduser('~/筋トレジム管理')
src = f'{base}/冊子/筋トレ_A5冊子_両面印刷_白地_2026-09-24.pdf'
dst = f'{base}/冊子/筋トレ_A5冊子_両面印刷_白地_2026-09-30.pdf'
FONT = '/tmp/NotoR_sub.otf'
fnt = fitz.Font(fontfile=FONT)

def find_span(page, text):
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                if s['text'] == text:
                    return s
    raise SystemExit(f'not found: {text}')

def c(v):
    return ((v >> 16) & 255) / 255, ((v >> 8) & 255) / 255, (v & 255) / 255

d = fitz.open(src)
jobs = []
# 表紙（page0）の改訂表記：中央そろえで差し替え
old_cover = '週5日 ｜ 休養日 木曜・日曜 ｜ 作成日 2026年9月18日（9月24日 セット数追記）'
new_cover = '週5日 ｜ 休養日 木曜・日曜 ｜ 作成日 2026年9月18日（9月30日 レッグプレス重量修正）'
jobs.append((0, old_cover, new_cover, True))
# 水曜レッグプレス（page3）
jobs.append((3, '47kg × 10-12回', '50kg × 10-12回', False))

plans = []
for pn, old, new, center in jobs:
    p = d[pn]
    s = find_span(p, old)
    r = fitz.Rect(s['bbox'])
    w_old = fnt.text_length(old, fontsize=s['size'])
    print(pn, 'bbox幅', round(r.width, 2), '計算幅', round(w_old, 2))
    ox, oy = s['origin']
    if center:
        cx = (r.x0 + r.x1) / 2
        ox = cx - fnt.text_length(new, fontsize=s['size']) / 2
    p.add_redact_annot(r + (-0.3, -0.3, 0.3, 0.3), fill=None)
    plans.append((pn, (ox, oy), new, s['size'], c(s['color'])))

for p in d:
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                       graphics=fitz.PDF_REDACT_LINE_ART_NONE)
for pn, org, new, size, col in plans:
    p = d[pn]
    p.insert_font(fontname='NotoR', fontfile=FONT)
    p.insert_text(org, new, fontname='NotoR', fontsize=size, color=col)
pass
d.save(dst, garbage=4, deflate=True)
print('saved', dst, os.path.getsize(dst))

d2 = fitz.open(dst)
os.makedirs(f'{base}/作業/check', exist_ok=True)
for i, p in enumerate(d2):
    p.get_pixmap(dpi=110).save(f'{base}/作業/check/p{i+1}.png')
d2[3].get_pixmap(dpi=300, clip=fitz.Rect(460, 90, 700, 180)).save(f'{base}/作業/check/zoom_legpress.png')
d2[0].get_pixmap(dpi=250, clip=fitz.Rect(470, 330, 800, 375)).save(f'{base}/作業/check/zoom_cover.png')
for pn in range(4):
    t = d2[pn].get_text()
    print(pn, '47kg × 10-12回' in t, '50kg × 10-12回' in t, 'レッグプレス重量修正' in t)
