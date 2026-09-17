import os
p = os.path.expandvars(r"$TEMP\check3.js")
with open(p, encoding="utf-8") as f:
    lines = f.read().split("\n")
print("total", len(lines))
for n in range(126, 138):
    print(n + 1, repr(lines[n][:100]))
