from docx import Document
import glob, os, json
os.chdir(r"C:\Users\orang\Desktop\网页制作")
out = {}
for f in glob.glob("*.docx"):
    if "简介" in f or "换公司名" in f:
        continue
    try:
        doc = Document(f)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        # heuristic: find TOC-like lines: start with digit, 第, CHAPTER, or short lines <30 chars in first 150 paras
        toc = []
        for p in doc.paragraphs[:200]:
            t = p.text.strip()
            if not t or len(t) > 60:
                continue
            style = p.style.name
            if style.startswith("Heading") or t.startswith("第") or (len(t) < 30 and ("章" in t or "节" in t or t[0].isdigit())):
                toc.append({"style": style, "text": t})
                if len(toc) >= 40:
                    break
        out[f] = {"total_paras": len(paras), "tables": len(doc.tables), "toc_guess": toc[:40], "head": paras[:8]}
    except Exception as e:
        out[f] = {"error": repr(e)}
with open(r"C:\Users\orang\Desktop\网页制作\work\toc.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print("wrote toc.json")
