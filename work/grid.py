from PIL import Image, ImageDraw
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
p3 = Image.open("images/directors/originals/p3_thumb.jpg").copy()
d = ImageDraw.Draw(p3)
W, H = p3.size
for x in range(0, W + 1, 100):
    d.line([(x, 0), (x, H)], fill=(255, 0, 0), width=2)
    d.text((x + 4, 4), str(x), fill=(255, 0, 0))
for y in range(0, H + 1, 100):
    d.line([(0, y), (W, y)], fill=(0, 255, 0), width=2)
    d.text((4, y + 4), str(y), fill=(0, 255, 0))
p3.save("images/directors/crops/p3_grid.png")
print("saved", p3.size)
