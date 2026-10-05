"""アプリアイコンを作る（Python標準ライブラリのみ）。
使い方: python3 tools/make_icons.py  → icons/ にPNGを書き出す"""
import os, struct, zlib

BG = (42, 42, 42)       # #2a2a2a
INK = (239, 238, 233)   # #efeee9
GOLD = (214, 178, 106)  # #d6b26a

def png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(c for p in px[y*w:(y+1)*w] for c in p) for y in range(h))
    def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    open(path, "wb").write(data)

def draw(size, pad):
    """プレートを重ねたバーベルを横から見た形。pad は外側の余白（maskable用）"""
    s = size
    px = [BG] * (s * s)
    def rect(x0, y0, x1, y1, col, r=0):
        for y in range(max(0, int(y0)), min(s, int(y1))):
            for x in range(max(0, int(x0)), min(s, int(x1))):
                if r:
                    cx = min(max(x + .5, x0 + r), x1 - r); cy = min(max(y + .5, y0 + r), y1 - r)
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 > r * r: continue
                px[y * s + x] = col
    u = (s - 2 * pad) / 100.0  # 100単位の座標系
    X = lambda v: pad + v * u
    # バー
    rect(X(6), X(47.5), X(94), X(52.5), INK, 1.5 * u)
    # 左右のプレート（外側ほど小さい）
    for x0, x1, h in [(25, 33, 48), (17, 23, 36), (10, 15, 24)]:
        rect(X(x0), X(50 - h / 2), X(x1), X(50 + h / 2), INK, 2.5 * u)
        rect(X(100 - x1), X(50 - h / 2), X(100 - x0), X(50 + h / 2), INK, 2.5 * u)
    # 中央の小さな印
    rect(X(47), X(70), X(53), X(76), GOLD, 3 * u)
    return px

os.makedirs("icons", exist_ok=True)
for size, pad, name in [(180, 0, "icon-180.png"), (192, 0, "icon-192.png"), (512, 0, "icon-512.png"), (512, 64, "icon-maskable-512.png")]:
    png(os.path.join("icons", name), size, size, draw(size, pad))
print("icons written")
