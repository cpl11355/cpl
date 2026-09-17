from PIL import Image
from rembg import remove, new_session
import os
os.chdir(r"C:\Users\orang\Desktop\网页制作")
os.makedirs("images/directors/crops", exist_ok=True)
os.makedirs("images/directors/cutouts", exist_ok=True)

p3 = Image.open("images/directors/originals/p3_thumb.jpg").convert("RGB")
jobs = {
    "gray": p3.crop((120, 630, 400, 1020)),
    "scarf": p3.crop((390, 600, 670, 1000)),
    "glasses": p3.crop((730, 605, 1000, 1000)),
    "red": Image.open("images/directors/originals/p4_red_solo.jpg").convert("RGB"),
    "idphoto": Image.open("images/directors/originals/p6_id.jpg").convert("RGB"),
}
for name, im in jobs.items():
    im.save("images/directors/crops/%s_crop.png" % name)
    print(name, "crop", im.size)

session = new_session("u2net")
for name in jobs:
    src = Image.open("images/directors/crops/%s_crop.png" % name)
    out = remove(src, session=session)
    out.save("images/directors/cutouts/%s_cut.png" % name)
    print(name, "cut done", out.size)
print("ALL DONE")
