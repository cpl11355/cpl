from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
im = Image.open("images/directors/cutouts/penlan_p1_cut.png").convert("RGBA")
print("size", im.size)
print("bbox", im.split()[3].point(lambda v: 255 if v > 32 else 0).getbbox())
