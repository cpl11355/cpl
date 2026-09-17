import pathlib
b = pathlib.Path(r"C:\Users\orang\Desktop\网页制作")
old_base = "https://ynfr7772-coder.github.io/cpl"
new_base = "https://www.cplbiopharma.com"

# 1. CNAME file for GitHub Pages custom domain (single line, no scheme)
(b / "CNAME").write_text("www.cplbiopharma.com\n", encoding="utf-8")
print("CNAME written")

# 2. index.html + report pages: swap canonical / og:url base
files = ["index.html",
         "report-ny-kitchenware-summary.html",
         "report-beauty-salon-summary.html",
         "report-food-import-summary.html",
         "report-h-wholesale-case-summary.html",
         "report-r-capital-case-summary.html"]
for name in files:
    p = b / name
    t = p.read_text(encoding="utf-8")
    n = t.count(old_base)
    t = t.replace(old_base, new_base)
    # fix possible double slash from old subpath root: new_base + "/" was old "…/cpl/"
    # (replacements of "…/cpl/" -> "https://www.cplbiopharma.com/" are already correct)
    p.write_text(t, encoding="utf-8")
    print(name, "replaced", n)

# 3. sitemap.xml: rewrite with root-domain URLs
sm = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.cplbiopharma.com/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
  <url><loc>https://www.cplbiopharma.com/report-ny-kitchenware-summary.html</loc><changefreq>yearly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.cplbiopharma.com/report-beauty-salon-summary.html</loc><changefreq>yearly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.cplbiopharma.com/report-food-import-summary.html</loc><changefreq>yearly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.cplbiopharma.com/report-h-wholesale-case-summary.html</loc><changefreq>yearly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.cplbiopharma.com/report-r-capital-case-summary.html</loc><changefreq>yearly</changefreq><priority>0.8</priority></url>
</urlset>
"""
(b / "sitemap.xml").write_text(sm, encoding="utf-8")

# 4. robots.txt
(b / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nSitemap: https://www.cplbiopharma.com/sitemap.xml\n",
    encoding="utf-8")
print("sitemap + robots rewritten")

# 5. verify
t = (b / "index.html").read_text(encoding="utf-8")
print("old base remaining:", t.count(old_base), "| new base count:", t.count(new_base))
