# -*- coding: utf-8 -*-
"""Rebuild PDF with edited JPEG at exact original page size."""
import os
from pypdf import PdfReader
from pypdf.generic import (DecodedStreamObject, NameObject, NumberObject,
                           FloatObject, DictionaryObject, ArrayObject)

WORK = os.path.dirname(os.path.abspath(__file__))
SRC_PDF = ('C:\\Users\\orang\\.pawwork\\dsh\\attachments\\v1\\files\\b3\\'
           'b373faf14d0a1f44bfe9348f48caf219e8d345b9f3746d70fde1d2c7d8eec4ef\\'
           'USCIS LETTER.pdf')
OUT_PDF = os.path.join(os.path.dirname(WORK), 'USCIS LETTER - edited.pdf')

with open(SRC_PDF, 'rb') as f:
    reader = PdfReader(f)
    src_page = reader.pages[0]
    mb = src_page.mediabox
    w, h = float(mb.width), float(mb.height)
print('page size: %.2f x %.2f pt' % (w, h))

with open(os.path.join(WORK, 'uscis_edited.jpg'), 'rb') as f:
    jpg = f.read()

from PIL import Image
im = Image.open(os.path.join(WORK, 'uscis_edited.jpg'))
print('image:', im.size, im.mode)
iw, ih = im.size

from pypdf import PdfWriter
writer = PdfWriter()
page = writer.add_blank_page(width=w, height=h)

img_obj = DecodedStreamObject()
img_obj.set_data(jpg)
img_obj.update({
    NameObject('/Type'): NameObject('/XObject'),
    NameObject('/Subtype'): NameObject('/Image'),
    NameObject('/Width'): NumberObject(iw),
    NameObject('/Height'): NumberObject(ih),
    NameObject('/ColorSpace'): NameObject('/DeviceRGB'),
    NameObject('/BitsPerComponent'): NumberObject(8),
    NameObject('/Filter'): NameObject('/DCTDecode'),
})
img_ref = writer._add_object(img_obj)

content = DecodedStreamObject()
content.set_data(
    ('q\n%.4f 0 0 %.4f 0 0 cm\n/Im1 Do\nQ' % (w, h)).encode('latin-1'))
content_ref = writer._add_object(content)

page[NameObject('/Resources')] = DictionaryObject({
    NameObject('/XObject'): DictionaryObject({NameObject('/Im1'): img_ref})
})
page[NameObject('/Contents')] = ArrayObject([content_ref])
page[NameObject('/MediaBox')] = ArrayObject(
    [NumberObject(0), NumberObject(0), FloatObject(w), FloatObject(h)])

saved = False
for cand in [OUT_PDF] + [os.path.join(os.path.dirname(WORK), 'USCIS LETTER - edited v%d.pdf' % i) for i in (2, 3, 4, 5)]:
    try:
        with open(cand, 'wb') as f:
            writer.write(f)
        print('saved', cand, os.path.getsize(cand), 'bytes')
        saved = True
        break
    except PermissionError:
        continue
if not saved:
    raise RuntimeError('all output names locked')
