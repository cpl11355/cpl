from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
im = Image.open("images/directors/qigong.png").convert("RGBA")
w, h = im.size
# drop 110px of top transparent padding, re-pad to 3:4 bottom-aligned
im2 = im.crop((0, 110, w, h))
w2, h2 = im2.size
tw = int(h2 * 0.75)
canvas = Image.new("RGBA", (tw, h2), (0, 0, 0, 0))
canvas.paste(im2, ((tw - w2) // 2, 0), im2)
canvas.save("images/directors/qigong.png")
print("qigong polished", canvas.size)
