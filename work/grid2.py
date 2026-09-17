from PIL import Image, ImageDraw
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
for name, src in [("p1", "images/directors/originals/p1_duo.jpg"),
                  ("kjcut", "images/directors/cutouts/keejong_cut.png")]:
    im = Image.open(src).convert("RGBA").copy()
    d = ImageDraw.Draw(im)
    W, H = im.size
    stepx = max(50, W // 14)
    stepy = max(50, H // 14)
    for x in range(0, W + 1, stepx):
        d.line([(x, 0), (x, H)], fill=(255, 0, 0, 255), width=2)
        d.text((x + 3, 3), str(x), fill=(255, 0, 0, 255))
    for y in range(0, H + 1, stepy):
        d.line([(0, y), (W, y)], fill=(0, 255, 0, 255), width=2)
        d.text((3, y + 3), str(y), fill=(0, 255, 0, 255))
    im.convert("RGB").save("images/directors/grid_%s.png" % name, quality=88)
    print(name, (W, H), stepx, stepy)
