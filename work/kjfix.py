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

kj = Image.open("images/directors/cutouts/keejong_cut.png").convert("RGBA").crop((0, 0, 170, 235))
pad = Image.new("RGBA", (170, 250), (0, 0, 0, 0))
pad.paste(kj, (0, 15), kj)
r, g, b, a = pad.split()
pad.putalpha(ImageChops.darker(a, a.filter(ImageFilter.MinFilter(3))))
pad = pad.resize((340, 500), Image.LANCZOS)
pad = ImageEnhance.Brightness(pad).enhance(1.03)
pad = ImageEnhance.Contrast(pad).enhance(1.05)
pad = ImageEnhance.Color(pad).enhance(1.04)
pad = pad.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
bg = studio_bg(340, 500)
bg.paste(pad, (0, 0), pad)
bg.save("images/directors/keejongchang_id.jpg", quality=90)
print("keejong", bg.size)
