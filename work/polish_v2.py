from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageChops
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

def defringe(im):
    # eat 1px contaminated edge
    r, g, b, a = im.split()
    a2 = a.filter(ImageFilter.MinFilter(3))
    im2 = im.copy()
    im2.putalpha(ImageChops.darker(a, a2))
    return im2

jobs = [
    ("penlan", "images/directors/cutouts/gray_cut.png", (25, 0, 265, 390), 1.8),
    ("keejongchang", "images/directors/cutouts/keejong_cut.png", (15, 0, 245, 400), 1.8),
]
for name, src, crop, scale in jobs:
    cut = Image.open(src).convert("RGBA").crop(crop)
    cut = defringe(cut)
    cut = cut.resize((int(cut.width * scale), int(cut.height * scale)), Image.LANCZOS)
    cut = ImageEnhance.Brightness(cut).enhance(1.03)
    cut = ImageEnhance.Contrast(cut).enhance(1.05)
    cut = ImageEnhance.Color(cut).enhance(1.04)
    cut = cut.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    bg = studio_bg(cut.width, cut.height)
    bg.paste(cut, (0, 0), cut)
    bg.save("images/directors/%s_web.jpg" % name, quality=90)
    print(name, bg.size, "saved")
print("REDO DONE")
