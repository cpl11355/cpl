from PIL import Image
import glob, os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
for f in sorted(glob.glob("images/directors/originals/*.jpg")):
    im = Image.open(f)
    print(os.path.basename(f), im.size)
