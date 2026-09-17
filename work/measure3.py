from PIL import Image, ImageDraw, ImageFilter
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")

def studio_bg(w, h):
    top = (26, 58, 143); mid = (14, 37, 96); bot = (8, 23, 64)
    bg = Image.new("RGB", (w, h))
    px = bg.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        if t < 0.55:
            k = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * k) for i in range(3))
        for x in range(w):
            px[x, y] = c
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse([int(w * 0.05), int(-h * 0.25), int(w * 0.95), int(h * 0.55)], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(max(w // 6, 8)))
    return Image.composite(Image.new("RGB", (w, h), (80, 130, 255)), bg, glow)

for f in ["images/directors/penlan_id.jpg", "images/directors/keejongchang_id.jpg", "images/directors/qigong_id.jpg"]:
    im = Image.open(f).convert("RGB")
    w, h = im.size
    bg = studio_bg(w, h)
    da = list(im.getdata())
    db = list(bg.getdata())
    a = [abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2]) for x, y in zip(da, db)]
    first = h
    for y in range(h):
        row = a[y * w:(y + 1) * w]
        if sum(row) / len(row) > 4.0:
            first = y
            break
    print(f.split("/")[-1], (w, h), "content starts y=%d (%.1f%%)" % (first, 100.0 * first / h))
