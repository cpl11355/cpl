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

def build(name, cut, pad_top, scale):
    W, H = cut.size
    canvas = Image.new("RGBA", (W, H + pad_top), (0, 0, 0, 0))
    canvas.paste(cut, (0, pad_top), cut)
    r, g, b, a = canvas.split()
    canvas.putalpha(ImageChops.darker(a, a.filter(ImageFilter.MinFilter(3))))
    canvas = canvas.resize((int(canvas.width * scale), int(canvas.height * scale)), Image.LANCZOS)
    canvas = ImageEnhance.Brightness(canvas).enhance(1.03)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.05)
    canvas = ImageEnhance.Color(canvas).enhance(1.04)
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    bg = studio_bg(canvas.width, canvas.height)
    bg.paste(canvas, (0, 0), canvas)
    bg.save("images/directors/%s_id.jpg" % name, quality=90)
    print(name, bg.size, "hairline@%.0f%%" % (100.0 * pad_top * scale / bg.height))

pl = Image.open("images/directors/cutouts/penlan_p1_cut.png").convert("RGBA")
build("penlan", pl, 44, 1.67)
kj = Image.open("images/directors/cutouts/keejong_cut.png").convert("RGBA").crop((0, 0, 170, 235))
build("keejongchang", kj, 26, 2.0)
print("FINAL ID DONE")
