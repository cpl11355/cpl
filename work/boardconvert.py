from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
os.makedirs("images/directors", exist_ok=True)
jobs = [
    ("董事资料/qi gong.png", "images/directors/board_qigong.jpg"),
    ("董事资料/pen lan.png", "images/directors/board_penlan.jpg"),
    ("董事资料/keejong chang.png", "images/directors/board_keejongchang.jpg"),
]
for src, dst in jobs:
    im = Image.open(src).convert("RGB")
    im.save(dst, quality=88)
    print(dst, im.size)
print("CONVERT DONE")
