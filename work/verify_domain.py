import pathlib, re
b = pathlib.Path(r"C:\Users\orang\Desktop\网页制作")
t = (b / "index.html").read_text(encoding="utf-8")
print("canonical in index:", "ynfr7772-coder.github.io/cpl/" in t)
for f in ["report-ny-kitchenware-summary.html", "report-beauty-salon-summary.html",
          "report-food-import-summary.html", "report-h-wholesale-case-summary.html",
          "report-r-capital-case-summary.html"]:
    print(f, "canonical:", "canonical" in (b / f).read_text(encoding="utf-8"))
print("root-absolute href/src in index:", len(re.findall(r'(href|src)="/', t)))
print("section order:", re.findall(r'<section id="(\w+)"', t))
print("sitemap exists:", (b / "sitemap.xml").exists(), "robots:", (b / "robots.txt").exists())
