import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v12.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
rows = []
cur = 0
for ln in md.splitlines():
    m = re.match(r"^## 【第(\d+)段", ln)
    if m:
        cur = int(m.group(1)); continue
    mm = re.match(r"^(" + T + r")-(" + T + r")，(.+?)：(.+)$", ln.strip())
    if not mm: continue
    d = max(sec(mm.group(2)) - sec(mm.group(1)), 1e-6)
    n = len(re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4)))
    rows.append((n / d, cur, mm.group(1), mm.group(2), n))
print("总行数:", len(rows), "| 超过 5.4 字/秒:", sum(1 for r in rows if r[0] > 5.4))
for r in sorted(rows, reverse=True)[:6]:
    print(f"  {r[0]:4.1f} 字/秒  段{r[1]} {r[2]}-{r[3]}  {r[4]}字")
