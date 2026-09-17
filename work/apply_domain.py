import pathlib
base = pathlib.Path(r"C:\Users\orang\Desktop\网页制作")
site = "https://ynfr7772-coder.github.io/cpl"
pages = [
    "report-ny-kitchenware-summary.html",
    "report-beauty-salon-summary.html",
    "report-food-import-summary.html",
    "report-h-wholesale-case-summary.html",
    "report-r-capital-case-summary.html",
]
for name in pages:
    p = base / name
    t = p.read_text(encoding="utf-8")
    if "rel=\"canonical\"" in t:
        print(name, "already has canonical, skip")
        continue
    tag = '<link rel="canonical" href="%s/%s">\n<meta property="og:url" content="%s/%s">' % (site, name, site, name)
    # insert right after the description meta line
    lines = t.split("\n")
    out = []
    inserted = False
    for ln in lines:
        out.append(ln)
        if (not inserted) and ('name="description"' in ln):
            out.append(tag)
            inserted = True
    assert inserted, name
    p.write_text("\n".join(out), encoding="utf-8")
    print(name, "canonical added")

# preview-new.html is an old draft: keep it out of search results
pp = base / "preview-new.html"
t = pp.read_text(encoding="utf-8")
if 'name="robots"' not in t:
    t = t.replace("</title>", "</title>\n<meta name=\"robots\" content=\"noindex,nofollow\">", 1)
    pp.write_text(t, encoding="utf-8")
    print("preview-new.html noindex added")
else:
    print("preview-new.html already noindex")
