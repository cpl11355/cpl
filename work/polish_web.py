from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")

def studio_bg(w, h):
    top = (26, 58, 143)
    mid = (14, 37, 96)
    bot = (8, 23, 64)
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
    # soft glow behind head
    glow = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([int(w * 0.05), int(-h * 0.25), int(w * 0.95), int(h * 0.55)], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(w // 6))
    tint = Image.new("RGB", (w, h), (80, 130, 255))
    bg = Image.composite(tint, bg, glow)
    return bg

def retouch(im, sharp=1.1):
    im = ImageEnhance.Brightness(im).enhance(1.03)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(1.04)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=int((sharp - 1) * 300), threshold=2))
    return im

jobs = [
    # name, src, crop-or-None, scale
    ("qigong", "images/directors/qigong.png", (70, 60, 670, 650), 1.0),
    ("penlan", "images/directors/penlan.png", None, 1.5),
    ("keejongchang", "images/directors/keejongchang.png", None, 1.5),
]
for name, src, crop, scale in jobs:
    cut = Image.open(src).convert("RGBA")
    if crop:
        cut = cut.crop(crop)
    if scale != 1.0:
        cut = cut.resize((int(cut.width * scale), int(cut.height * scale)), Image.LANCZOS)
    cut = retouch(cut, sharp=1.2 if scale != 1.0 else 1.1)
    bg = studio_bg(cut.width, cut.height)
    bg.paste(cut, (0, 0), cut)
    out = "images/directors/%s_web.jpg" % name
    bg.save(out, quality=90)
    print(name, bg.size, "saved")
print("WEB DONE")
