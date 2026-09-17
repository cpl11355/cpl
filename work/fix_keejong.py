from PIL import Image
from rembg import remove, new_session
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")

p3 = Image.open("images/directors/originals/p3_thumb.jpg").convert("RGB")
kj = p3.crop((395, 600, 650, 1000))
kj.save("images/directors/crops/keejong_crop.png")
print("keejong crop", kj.size)

session = new_session("u2net")
out = remove(kj, session=session)
out.save("images/directors/cutouts/keejong_cut.png")
print("keejong cut done", out.size)

# checker preview
bg = Image.new("RGBA", out.size, (255, 255, 255, 255))
tile = 16
grid = Image.new("RGBA", out.size)
px = grid.load()
for y in range(out.size[1]):
    for x in range(out.size[0]):
        px[x, y] = (230, 230, 230, 255) if ((x // tile) + (y // tile)) % 2 == 0 else (255, 255, 255, 255)
comp = Image.alpha_composite(grid, out.convert("RGBA")).convert("RGB")
comp.save("images/directors/cutouts/preview_keejong.png")
print("preview done")
