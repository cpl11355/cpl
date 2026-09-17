from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageChops
from rembg import remove, new_session
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

def finish(name, cut, scale):
    r, g, b, a = cut.split()
    cut.putalpha(ImageChops.darker(a, a.filter(ImageFilter.MinFilter(3))))
    cut = cut.resize((int(cut.width * scale), int(cut.height * scale)), Image.LANCZOS)
    cut = ImageEnhance.Brightness(cut).enhance(1.03)
    cut = ImageEnhance.Contrast(cut).enhance(1.05)
    cut = ImageEnhance.Color(cut).enhance(1.04)
    cut = cut.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    bg = studio_bg(cut.width, cut.height)
    bg.paste(cut, (0, 0), cut)
    bg.save("images/directors/%s_id.jpg" % name, quality=90)
    print(name, bg.size)

# Pen Lan from p1 (arms down), then rembg
p1 = Image.open("images/directors/originals/p1_duo.jpg").convert("RGB")
plc = p1.crop((795, 300, 1130, 700))
plc.save("images/directors/crops/penlan_p1_crop.png")
session = new_session("u2net")
plcut = remove(plc, session=session).convert("RGBA")
plcut.save("images/directors/cutouts/penlan_p1_cut.png")
print("penlan p1 cut", plcut.size)
finish("penlan", plcut, 1.67)

# Keejong: tight ID box on existing seam cut + top pad
kj = Image.open("images/directors/cutouts/keejong_cut.png").convert("RGBA").crop((0, 0, 170, 235))
pad = Image.new("RGBA", (kj.width, kj.height + 30), (0, 0, 0, 0))
pad.paste(kj, (0, 30), kj)
finish("keejongchang", pad, 2.0)
print("ID2 DONE")
