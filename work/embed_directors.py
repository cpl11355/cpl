from PIL import Image
import base64, io, os

html_path = r"C:\Users\orang\Desktop\网页制作\index.html"
with open(html_path, encoding="utf-8") as f:
    html = f.read()

mapping = [
    "images/directors/board_qigong.jpg",
    "images/directors/board_penlan.jpg",
    "images/directors/board_keejongchang.jpg",
]

for src in mapping:
    fp = os.path.join(r"C:\Users\orang\Desktop\网页制作", src)
    im = Image.open(fp).convert("RGB")
    w, h = im.size
    nw = 600
    nh = int(h * nw / w)
    im = im.resize((nw, nh), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=72, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    data_uri = "data:image/jpeg;base64," + b64
    print(src, str(w) + "x" + str(h) + " -> " + str(nw) + "x" + str(nh), str(len(buf.getvalue())) + " bytes")
    html = html.replace('src="' + src + '"', 'src="' + data_uri + '"')

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("EMBED DONE, new size:", os.path.getsize(html_path))
