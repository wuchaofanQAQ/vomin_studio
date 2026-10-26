import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
pat = re.compile(r"^\[([\d.]+)s-([\d.]+)s\]\uff0c(.+?)\uff1a(.+)$")
rows = []
for ln in md.splitlines():
    m = pat.match(ln.strip())
    if not m: continue
    d = float(m.group(2)) - float(m.group(1))
    n = len(re.sub(r"[^\u4e00-\u9fff]", "", m.group(4)))
    rows.append((round(n/d, 1), m.group(4)))
print("lines:", len(rows), "| >5.3:", sum(1 for r in rows if r[0] > 5.3))
texts = [r[1] for r in rows]
print("dups:", len([t for t in set(texts) if texts.count(t) > 1]))
print("max rate:", max(r[0] for r in rows))
