from PIL import Image
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
os.makedirs("images/directors/crops", exist_ok=True)
p3 = Image.open("images/directors/originals/p3_thumb.jpg")
print("p3", p3.size)
crops = {
    "crop_gray.png": (90, 490, 470, 1130),
    "crop_scarf.png": (350, 440, 710, 1080),
    "crop_glasses.png": (810, 455, 1200, 1100),
}
for name, box in crops.items():
    c = p3.crop(box)
    c.save("images/directors/crops/" + name)
    print(name, box, c.size)
