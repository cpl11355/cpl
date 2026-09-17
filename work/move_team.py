import re, pathlib
p = pathlib.Path(r"C:\Users\orang\Desktop\网页制作\index.html")
t = p.read_text(encoding="utf-8")

# 1. move <section id="team">...</section> to after <section id="future">...</section>
team_m = re.search(r'<section id="team">.*?</section>', t, re.S)
fut_m = re.search(r'<section id="future".*?</section>', t, re.S)
assert team_m and fut_m, "sections not found"
team_block = team_m.group(0)
fut_block = fut_m.group(0)
# remove team from its original place (keep surrounding whitespace tidy)
t = t.replace(team_block, "", 1)
# re-find future in updated text, insert team right after it
fut_m2 = re.search(r'<section id="future".*?</section>', t, re.S)
t = t[:fut_m2.end()] + "\n\n" + team_block + t[fut_m2.end():]
# collapse possible triple blank lines left by removal
t = re.sub(r"\n{4,}", "\n\n\n", t)

# 2. nav order: Board after Future (desktop + mobile)
team_link = '<a href="#team"><span class="t-cn">\u8463\u4e8b\u4f1a</span><span class="t-en en">Board</span></a>'
future_link = '<a href="#future"><span class="t-cn">\u672a\u6765\u65b9\u5411</span><span class="t-en en">Future</span></a>'
assert team_link in t and future_link in t
t = t.replace(team_link + "\n      " + future_link, future_link + "\n      " + team_link)

team_link_m = '<a href="#team"><span class="t-cn">\u8463\u4e8b\u4f1a</span><span class="t-en en">Board</span></a>'
future_link_m = '<a href="#future"><span class="t-cn">\u672a\u6765\u65b9\u5411</span><span class="t-en en">Future</span></a>'
# mobile menu uses different labels
team_mob = '<a href="#team"><span class="t-cn">\u8463\u4e8b\u4f1a</span><span class="t-en en">Board</span></a>'
future_mob = '<a href="#future"><span class="t-cn">\u672a\u6765\u65b9\u5411</span><span class="t-en en">Future</span></a>'
# generic swap for any remaining team-before-future adjacency (mobile labels differ)
t = re.sub(
    r'(<a href="#team">.*?</a>\s*)(<a href="#future">.*?</a>)',
    lambda m: m.group(2) + "\n    " + m.group(1).strip(),
    t,
)

# 3. scroll-spy order matches new page order
t = t.replace(
    "const secs=['about','services','future','cases','team','contact']",
    "const secs=['about','services','cases','future','team','contact']",
)

p.write_text(t, encoding="utf-8")
print("MOVE DONE")
# verify order
import re as _re
ids = _re.findall(r'<section id="(\w+)"', t)
print("section order:", ids)
