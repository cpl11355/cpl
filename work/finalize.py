from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")

srcs = {
    "qigong": "images/directors/cutouts/red_cut.png",
    "penlan": "images/directors/cutouts/gray_cut.png",
    "keejongchang": "images/directors/cutouts/keejong_cut.png",
}
for name, p in srcs.items():
    im = Image.open(p).convert("RGBA")
    # trim transparent margins
    bbox = im.split()[3].getbbox()
    im = im.crop(bbox)
    w, h = im.size
    # pad to 3:4, subject bottom-centered
    tw = max(w, int(h * 0.75))
    th = max(h, int(w / 0.75))
    # keep 3:4 exactly
    if tw / th > 0.75:
        th = int(tw / 0.75)
    else:
        tw = int(th * 0.75)
    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    canvas.paste(im, ((tw - w) // 2, th - h), im)
    canvas.save("images/directors/%s.png" % name)
    print(name, "raw", (w, h), "final", canvas.size)
print("FINALS DONE")
