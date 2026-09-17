from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")

# checkerboard previews to inspect cutout edges
names = ["gray", "scarf", "glasses", "red", "idphoto"]
sheet = []
for name in names:
    cut = Image.open("images/directors/cutouts/%s_cut.png" % name).convert("RGBA")
    bg = Image.new("RGBA", cut.size, (255, 255, 255, 255))
    tile = 16
    grid = Image.new("RGBA", cut.size)
    px = grid.load()
    for y in range(0, cut.size[1], 1):
        for x in range(0, cut.size[0], 1):
            if ((x // tile) + (y // tile)) % 2 == 0:
                px[x, y] = (230, 230, 230, 255)
            else:
                px[x, y] = (255, 255, 255, 255)
    comp = Image.alpha_composite(grid, cut).convert("RGB")
    comp.save("images/directors/cutouts/preview_%s.png" % name)
    print(name, cut.size)
print("PREVIEWS DONE")
