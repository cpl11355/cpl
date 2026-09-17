# -*- coding: utf-8 -*-
"""USCIS letter editor v2 (fixed): correct fonts, cap-band height fit,
local background, uniform scaling only."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'uscis_page1.jpg')
OUT_JPG = os.path.join(HERE, 'uscis_edited.jpg')
FD = os.path.join(os.environ['WINDIR'], 'Fonts')
F_ARIAL = os.path.join(FD, 'arial.ttf')
F_NARROW = os.path.join(FD, 'LiberationSansNarrow-Regular.ttf')
F_BOLD = os.path.join(FD, 'arialbd.ttf')

INK = (65, 65, 65)

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

def cap_band(y0, y1, x0, x1, thr=180, frac=0.25):
    """Main glyph band: rows with ink count >= frac*max (drops comma tails,
    faint blur edges, crud)."""
    g = arr[y0:y1, x0:x1].mean(axis=2)
    m = g < thr
    counts = m.sum(axis=1)
    mx = counts.max()
    good = counts >= mx * frac
    # longest contiguous run
    best = (0, -1, 0)
    s = None
    for i, v in enumerate(good):
        if v and s is None:
            s = i
        if not v and s is not None:
            if i - 1 - s > best[1] - best[0]:
                best = (s, i - 1, i - s)
            s = None
    if s is not None and len(good) - 1 - s > best[1] - best[0]:
        best = (s, len(good) - 1, len(good) - s)
    return (y0 + best[0], y0 + best[1])

def local_bg(y0, y1, x0, x1, pad=14):
    ry0, ry1 = max(0, y0 - pad), min(H, y1 + pad)
    rx0, rx1 = max(0, x0 - pad * 2), min(W, x1 + pad * 2)
    ring = arr[ry0:ry1, rx0:rx1].reshape(-1, 3)
    g = ring.mean(axis=1)
    sel = ring[g > 225]
    if len(sel) < 10:
        return (252, 252, 252)
    return tuple(int(v) for v in np.median(sel, axis=0))

def whiteout(box, bg):
    x0, y0, x1, y1 = [int(v) for v in box]
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(W - 1, x1); y1 = min(H - 1, y1)
    ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], fill=bg)

def render_text(text, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    tmp = Image.new('RGB', (int(size * len(text) * 0.85) + 120, int(size * 3)),
                    (255, 255, 255))
    ImageDraw.Draw(tmp).text((50, int(size * 0.4)), text, font=f,
                             fill=(INK[0], INK[1], INK[2]))
    a = np.array(tmp).astype(int)
    m = a.mean(axis=2) < 200
    ys, xs = np.where(m)
    return tmp.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def render_tracked(text, fontpath, size, target_w, scale):
    f = ImageFont.truetype(fontpath, size)
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    adv = [d.textlength(c, font=f) for c in text]
    nat = sum(adv)
    pre_w = target_w / scale
    track = (pre_w - nat) / max(1, len(text) - 1)
    strip_w = int(pre_w + 120)
    strip = Image.new('RGB', (strip_w, int(size * 3)), (255, 255, 255))
    dd = ImageDraw.Draw(strip)
    x = 50.0
    for c, a in zip(text, adv):
        dd.text((x, int(size * 0.4)), c, font=f, fill=(INK[0], INK[1], INK[2]))
        x += a + track
    strip = strip.resize((int(strip_w * scale), int(strip.height * scale)))
    a = np.array(strip).astype(int)
    m = a.mean(axis=2) < 200
    ys, xs = np.where(m)
    return strip.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def fit_place(label, new_text, fontpath, sizes, sbox, white_box, bg,
              ox=None, tracked_w=None, band_box=None):
    """Fit crop height to cap band with uniform scale; paste left-aligned,
    v-centered in band."""
    y0, y1, x0, x1 = sbox
    old = ink_bbox(y0, y1, x0, x1)
    by0, by1, bx0, bx1 = band_box if band_box else sbox
    cy0, cy1 = cap_band(by0, by1, bx0, bx1)
    cap_h = cy1 - cy0 + 1
    print('%s old ink %s cap band y%d-%d (h=%d)' % (label, old, cy0, cy1, cap_h))
    best = None
    for size in sizes:
        if tracked_w:
            crop = render_tracked(new_text, fontpath, size,
                                  tracked_w, cap_h / render_tracked(
                                      new_text, fontpath, size,
                                      tracked_w, 1.0).height)
            s = 1.0
        else:
            crop = render_text(new_text, fontpath, size)
            s = cap_h / crop.height
        if 0.9 <= s <= 1.12 and (best is None or abs(s - 1.0) < abs(best[0] - 1.0)):
            best = (s, size, crop)
    if best is None:
        raise RuntimeError('no size fit for ' + label)
    s, size, crop = best
    if abs(s - 1.0) > 0.005:
        crop = crop.resize((max(1, int(crop.width * s)),
                            max(1, int(crop.height * s))))
    px = old[0] if ox is None else ox
    if ox is not None and band_box is not None:
        # relocated field: keep same offset inside new white box as the
        # cap band had inside the measured band box
        py = white_box[1] + (cy0 - band_box[0])
    else:
        py = cy0 + (cap_h - crop.height) // 2
    whiteout((white_box[0], white_box[1],
              max(white_box[2], px + crop.width), white_box[3]), bg)
    img.paste(crop, (px, py))
    print('  -> font sz%d scale=%.3f pasted at (%d,%d) %s' %
          (size, s, px, py, (crop.width, crop.height)))

# ---------------- header: receipt# ----------------
bg = local_bg(395, 418, 197, 415)
crop = render_tracked('IOE0938252886', F_NARROW, 36, target_w=230, scale=23/25)
cy0, cy1 = cap_band(393, 421, 195, 420)
ch = cy1 - cy0 + 1
s = ch / crop.height
print('receipt cap band y%d-%d h=%d scale=%.3f' % (cy0, cy1, ch, s))
if abs(s - 1.0) > 0.005:
    crop = crop.resize((max(1, int(crop.width * s)), max(1, int(crop.height * s))))
whiteout((195, 393, max(420, 197 + crop.width), 421), bg)
img.paste(crop, (197, cy0 + (ch - crop.height) // 2))
print('  receipt pasted at (197,%d) %s' % (cy0 + (ch - crop.height) // 2, (crop.width, crop.height)))

# ---------------- header: dates ----------------
fit_place('received', '05/11/2026', F_ARIAL, [30, 31],
          (476, 506, 192, 360), (194, 477, 347, 505), local_bg(479, 502, 196, 345))
fit_place('priority', '05/11/2026', F_ARIAL, [30, 31],
          (476, 506, 726, 890), (728, 477, 880, 505), local_bg(480, 503, 730, 878))
fit_place('notice', '05/21/2026', F_ARIAL, [30, 31],
          (560, 592, 192, 360), (194, 560, 347, 592), local_bg(563, 587, 196, 345))

# ---------------- header: A# (true box starts x=1382) ----------------
fit_place('anum', 'A063331563', F_ARIAL, [31, 32, 33],
          (436, 470, 1380, 1590), (1380, 436, 1592, 467),
          local_bg(440, 463, 1382, 1568), ox=1382)

# ---------------- header: applicant name ----------------
fit_place('name_hdr', 'CHEN LIZHEN', F_ARIAL, [30, 32, 34],
          (476, 510, 1260, 1535), (1261, 476, 1530, 510),
          local_bg(480, 506, 1263, 1515))

# ---------------- address block ----------------
fit_place('addr_name', 'CHEN LIZHEN', F_ARIAL, [34, 36, 38, 40],
          (650, 702, 265, 600), (269, 650, 600, 702),
          local_bg(654, 698, 271, 587))

co = ink_bbox(702, 746, 265, 660)
print('c/o ink:', co)
whiteout((co[0] - 2, co[1] - 2, co[2] + 2, co[3] + 2), local_bg(*co))

st_old = ink_bbox(756, 794, 270, 930)
ct_old = ink_bbox(806, 844, 265, 690)
print('street old:', st_old, 'city old:', ct_old)
whiteout((st_old[0] - 2, st_old[1] - 2, st_old[2] + 2, st_old[3] + 2),
         local_bg(*st_old))
whiteout((ct_old[0] - 2, ct_old[1] - 2, ct_old[2] + 2, ct_old[3] + 2),
         local_bg(*ct_old))

street_y = co[1]
city_y = street_y + 52
fit_place('street_new', '146-33 21ST AVENUE', F_BOLD, [38, 40],
          (street_y - 4, street_y + 36, 270, 930), (273, street_y - 4, 930, street_y + 36),
          local_bg(*st_old), ox=275, band_box=(756, 794, 270, 930))
fit_place('city_new', 'WHITESTONE NY 11357', F_BOLD, [38, 40],
          (city_y - 4, city_y + 36, 265, 700), (269, city_y - 4, 700, city_y + 36),
          local_bg(*ct_old), ox=271, band_box=(806, 844, 265, 690))

img.save(OUT_JPG, 'JPEG', quality=95)
print('saved', OUT_JPG)
