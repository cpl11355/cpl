# -*- coding: utf-8 -*-
"""USCIS letter editor v3: Times New Roman regular everywhere (user request),
no bold. Uniform height-fit, local background sampling."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'uscis_page1.jpg')
OUT_JPG = os.path.join(HERE, 'uscis_edited.jpg')
FD = os.path.join(os.environ['WINDIR'], 'Fonts')
F_TIMES = os.path.join(FD, 'times.ttf')

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
    g = arr[y0:y1, x0:x1].mean(axis=2)
    m = g < thr
    counts = m.sum(axis=1)
    mx = counts.max()
    good = counts >= mx * frac
    best = (0, -1)
    s = None
    for i, v in enumerate(good):
        if v and s is None:
            s = i
        if not v and s is not None:
            if i - 1 - s > best[1] - best[0]:
                best = (s, i - 1)
            s = None
    if s is not None and len(good) - 1 - s > best[1] - best[0]:
        best = (s, len(good) - 1)
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

def render_text(text, size):
    f = ImageFont.truetype(F_TIMES, size)
    tmp = Image.new('RGB', (int(size * len(text) * 0.85) + 120, int(size * 3)),
                    (255, 255, 255))
    ImageDraw.Draw(tmp).text((50, int(size * 0.4)), text, font=f,
                             fill=(INK[0], INK[1], INK[2]))
    a = np.array(tmp).astype(int)
    m = a.mean(axis=2) < 200
    ys, xs = np.where(m)
    return tmp.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def render_spaced(groups, gap_px, size):
    """Render word groups with fixed inter-group gap (for A# spacing)."""
    f = ImageFont.truetype(F_TIMES, size)
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    widths = [d.textlength(g, font=f) for g in groups]
    total = sum(widths) + gap_px * (len(groups) - 1)
    tmp = Image.new('RGB', (int(total) + 120, int(size * 3)), (255, 255, 255))
    dd = ImageDraw.Draw(tmp)
    x = 50.0
    for g, w in zip(groups, widths):
        dd.text((x, int(size * 0.4)), g, font=f,
                fill=(INK[0], INK[1], INK[2]))
        x += w + gap_px
    a = np.array(tmp).astype(int)
    m = a.mean(axis=2) < 200
    ys, xs = np.where(m)
    return tmp.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def render_cap_h(crop, frac=0.25, thr=200):
    """Cap height of a rendered crop (drops comma-tail rows)."""
    a = np.array(crop).astype(int)
    m = a.mean(axis=2) < thr
    counts = m.sum(axis=1)
    mx = counts.max()
    good = counts >= mx * frac
    best = (0, -1)
    s = None
    for i, v in enumerate(good):
        if v and s is None:
            s = i
        if not v and s is not None:
            if i - 1 - s > best[1] - best[0]:
                best = (s, i - 1)
            s = None
    if s is not None and len(good) - 1 - s > best[1] - best[0]:
        best = (s, len(good) - 1)
    return best[1] - best[0] + 1

def fit_place(label, new_text, sizes, sbox, white_box, bg,
              ox=None, band_box=None, spaced_gap=None,
              force_scale=None, top_align=False):
    y0, y1, x0, x1 = sbox
    old = ink_bbox(y0, y1, x0, x1)
    by0, by1, bx0, bx1 = band_box if band_box else sbox
    cy0, cy1 = cap_band(by0, by1, bx0, bx1)
    cap_h = cy1 - cy0 + 1
    print('%s old ink %s cap band y%d-%d (h=%d)' % (label, old, cy0, cy1, cap_h))
    best = None
    for size in sizes:
        if spaced_gap is not None:
            crop = render_spaced(new_text.split(' '), spaced_gap, size)
        else:
            crop = render_text(new_text, size)
        ref_h = render_cap_h(crop) if top_align else crop.height
        s = force_scale if force_scale is not None else cap_h / ref_h
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
        py = white_box[1] + (cy0 - band_box[0])
    elif top_align:
        py = cy0
    else:
        py = cy0 + (cap_h - crop.height) // 2
    whiteout((white_box[0], white_box[1],
              max(white_box[2], px + crop.width), white_box[3]), bg)
    img.paste(crop, (px, py))
    print('  -> Times sz%d scale=%.3f pasted at (%d,%d) %s' %
          (size, s, px, py, (crop.width, crop.height)))

# ---------------- header ----------------
fit_place('receipt', 'IOE0938252886', [36],
          (393, 421, 195, 420), (195, 393, 440, 421),
          local_bg(395, 418, 197, 415))
fit_place('received', '05/11/2026', [34],
          (476, 506, 192, 360), (194, 477, 347, 505),
          local_bg(479, 502, 196, 345))
fit_place('priority', '05/11/2026', [34],
          (476, 506, 726, 890), (728, 477, 880, 505),
          local_bg(480, 503, 730, 878))
fit_place('notice', '05/21/2026', [34],
          (560, 592, 192, 360), (194, 560, 347, 592),
          local_bg(563, 587, 196, 345))
fit_place('anum', 'A063 331 563', [32],
          (436, 470, 1380, 1590), (1380, 436, 1592, 467),
          local_bg(440, 463, 1382, 1568), ox=1382, spaced_gap=11.5,
          force_scale=1.0)
fit_place('name_hdr', 'CHEN, LIZHEN', [34],
          (476, 510, 1260, 1535), (1261, 476, 1530, 510),
          local_bg(480, 506, 1263, 1515), top_align=True)

# ---------------- address block ----------------
fit_place('addr_name', 'CHEN, LIZHEN', [42],
          (650, 702, 265, 600), (269, 650, 600, 702),
          local_bg(654, 698, 271, 587), top_align=True)

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
fit_place('street_new', '146-33 21ST AVENUE', [42],
          (street_y - 4, street_y + 36, 270, 930), (273, street_y - 4, 930, street_y + 36),
          local_bg(*st_old), ox=275, band_box=(756, 794, 270, 930))
fit_place('city_new', 'WHITESTONE NY 11357', [42],
          (city_y - 4, city_y + 36, 265, 700), (269, city_y - 4, 760, city_y + 36),
          local_bg(*ct_old), ox=271, band_box=(806, 844, 265, 690))

img.save(OUT_JPG, 'JPEG', quality=95)
print('saved', OUT_JPG)
