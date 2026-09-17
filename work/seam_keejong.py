from PIL import Image, ImageFilter
from rembg import remove, new_session
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")

p3 = Image.open("images/directors/originals/p3_thumb.jpg").convert("RGB")
kj = p3.crop((390, 600, 670, 1000))  # 280x400
kj.save("images/directors/crops/keejong_crop.png")

session = new_session("u2net")
out = remove(kj, session=session).convert("RGBA")

# seam: drop everything right of x=158 (Qi Gong's hair/shoulder), 3px feather
W, H = out.size
alpha = out.split()[3]
mask = Image.new("L", (W, H), 0)
mp = mask.load()
SEAM = 158
for y in range(H):
    for x in range(W):
        if x < SEAM - 2:
            mp[x, y] = 255
        elif x > SEAM + 2:
            mp[x, y] = 0
        else:
            mp[x, y] = int(255 * (SEAM + 2 - x) / 4)
mask = mask.filter(ImageFilter.GaussianBlur(1))
a = Image.new("L", (W, H), 0)
# combine: keep min(original alpha, seam mask)
from PIL import ImageChops
a = ImageChops.darker(alpha, mask)
out.putalpha(a)
out.save("images/directors/cutouts/keejong_cut.png")

bg = Image.new("RGBA", out.size, (255, 255, 255, 255))
tile = 16
grid = Image.new("RGBA", out.size)
px = grid.load()
for y in range(H):
    for x in range(W):
        px[x, y] = (230, 230, 230, 255) if ((x // tile) + (y // tile)) % 2 == 0 else (255, 255, 255, 255)
Image.alpha_composite(grid, out).convert("RGB").save("images/directors/cutouts/preview_keejong.png")
print("keejong seam cut done", out.size)
