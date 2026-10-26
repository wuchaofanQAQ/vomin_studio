import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v13.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
rows = []
cur = 0
for ln in md.splitlines():
    m = re.match(r"^## \u3010\u7b2c(\d+)\u6bb5", ln)
    if m:
        cur = int(m.group(1)); continue
    mm = re.match(r"^(" + T + r")-(" + T + r")\uff0c(.+?)\uff1a(.+)$", ln.strip())
    if not mm: continue
    d = max(sec(mm.group(2)) - sec(mm.group(1)), 1e-6)
    n = len(re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4)))
    rows.append((round(n / d, 1), cur, mm.group(1), mm.group(2), n))
print("lines:", len(rows), "| >5.4 c/s:", sum(1 for r in rows if r[0] > 5.4))
for r in sorted(rows, reverse=True)[:5]:
    print(" ", r[0], "segment", r[1], r[2], "-", r[3], r[4], "chars")
