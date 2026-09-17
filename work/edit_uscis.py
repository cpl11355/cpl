# -*- coding: utf-8 -*-
"""USCIS I-797C scanned letter editor: replace name/address/A#/dates."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np, os

WORK = r'C:\Users\orang\Desktop\网页制作\work'
SRC = os.path.join(WORK, 'uscis_page1.jpg')
OUT_JPG = os.path.join(WORK, 'uscis_edited.jpg')
FONTS_DIR = os.path.join(os.environ['WINDIR'], 'Fonts')
ARIAL = os.path.join(FONTS_DIR, 'arial.ttf')

BG = (253, 253, 253)     # sampled scan background
INK = (70, 70, 70)       # matches scanned black-ink core (~50-120)
PAD = 3

img = Image.open(SRC).convert('RGB')
arr = np.array(img).astype(int)
H, W, _ = arr.shape
print('canvas', W, 'x', H)

def ink_bbox(y0, y1, x0, x1, thr=180):
    g = arr[y0:y1, x0:x1].mean(axis=2)
    m = g < thr
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (int(x0 + xs.min()), int(y0 + ys.min()),
            int(x0 + xs.max()), int(y0 + ys.max()))

def whiteout(box, pad=PAD):
    x0, y0, x1, y1 = box
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(W - 1, x1 + pad); y1 = min(H - 1, y1 + pad)
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=BG)
    return (x0, y0, x1, y1)

def render_crop(text, size):
    f = ImageFont.truetype(ARIAL, size)
    tmp = Image.new('RGB', (int(size * len(text) * 0.85) + 120, int(size * 3)), BG)
    d = ImageDraw.Draw(tmp)
    d.text((50, int(size * 0.5)), text, font=f, fill=INK)
    a = np.array(tmp).astype(int)
    g = a.mean(axis=2)
    m = g < 200
    ys, xs = np.where(m)
    return tmp.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def replace(search_box, new_text, size, new_xy=None):
    """Find old ink in search_box, white it out, draw new_text top-left aligned."""
    y0, y1, x0, x1 = search_box
    old = ink_bbox(y0, y1, x0, x1)
    if old is None:
        raise RuntimeError('no ink found in %r' % (search_box,))
    print('old ink', old, '->', repr(new_text))
    crop = render_crop(new_text, size)
    ox0, oy0 = old[0], old[1]
    if new_xy is not None:
        ox0, oy0 = new_xy
    # whiteout covers old ink AND new crop footprint
    whiteout((min(ox0, old[0]), min(oy0, old[1]),
              max(ox0 + crop.width, old[2]), max(oy0 + crop.height, old[3])))
    img.paste(crop, (ox0, oy0))
    return (ox0, oy0, ox0 + crop.width, oy0 + crop.height)

def erase(search_box):
    y0, y1, x0, x1 = search_box
    old = ink_bbox(y0, y1, x0, x1)
    print('erase ink', old)
    if old:
        whiteout(old)
    return old

# ---- header fields ----
# Received Date 04/06/2026 -> 05/11/2026
replace((476, 506, 192, 360), '05/11/2026', 33)
# Priority Date 04/06/2026 -> 05/11/2026
replace((476, 506, 726, 890), '05/11/2026', 33)
# Notice Date 04/24/2026 -> 05/21/2026
replace((560, 592, 192, 360), '05/21/2026', 33)
# A-number A065336967 -> A063331563
replace((436, 472, 1400, 1590), 'A063331563', 40)
# Header applicant name ZOU,LIANSONG -> CHEN LIZHEN
replace((476, 510, 1260, 1535), 'CHEN LIZHEN', 37)

# ---- address block ----
# Name -> CHEN LIZHEN
replace((650, 702, 265, 600), 'CHEN LIZHEN', 39)
# c/o line removed
co = erase((702, 746, 265, 660))
# Street moves up to c/o slot; city moves up to old street slot
st_old = ink_bbox(756, 794, 270, 930)
ct_old = ink_bbox(806, 844, 265, 690)
print('street old', st_old, 'city old', ct_old)
if st_old: whiteout(st_old)
if ct_old: whiteout(ct_old)
street_y = co[1] if co else 708          # c/o top
city_y = street_y + 52                    # keep ~52px line pitch
sc = render_crop('146-33 21ST AVENUE', 39)
whiteout((275, street_y, 275 + sc.width, street_y + sc.height))
img.paste(sc, (275, street_y))
print('street new at', (275, street_y))
cc = render_crop('WHITESTONE NY 11357', 39)
whiteout((271, city_y, 271 + cc.width, city_y + cc.height))
img.paste(cc, (271, city_y))
print('city new at', (271, city_y))

img.save(OUT_JPG, 'JPEG', quality=95)
print('saved', OUT_JPG)
