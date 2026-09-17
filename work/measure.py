from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
for f in ["images/directors/cutouts/keejong_cut.png",
          "images/directors/cutouts/gray_cut.png",
          "images/directors/crops/penlan_p1_crop.png"]:
    im = Image.open(f).convert("RGBA") if "cut" in f else Image.open(f).convert("RGB")
    print(f.split("/")[-1], im.size)
    if "cut" in f:
        a = im.split()[3]
        bbox = a.point(lambda v: 255 if v > 32 else 0).getbbox()
        print("  opaque bbox:", bbox)
