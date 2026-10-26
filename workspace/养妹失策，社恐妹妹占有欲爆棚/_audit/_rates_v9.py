import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v9.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
rows = []
cur = None
for ln in md.splitlines():
    m = re.match(rf"^## 【第(\d+)段", ln)
    if m: cur = int(m.group(1)); continue
    mm = re.match(rf"^({T})-({T})，(.+?)：(.+)$", ln.strip())
    if not mm: continue
    d = max(sec(mm.group(2)) - sec(mm.group(1)), 1e-6)
    n = len(re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4)))
    rows.append((n/d, cur, mm.group(1), mm.group(2), n, mm.group(3)[:14]))
rows.sort(reverse=True)
print("最慢 5 句：")
for r in rows[:5]: print(f"  {r[0]:4.1f} 字/秒  段{r[1]} {r[2]}-{r[3]}  {r[4]}字  {r[5]}")
print("最快 5 句：")
for r in rows[-5:]: print(f"  {r[0]:4.1f} 字/秒  段{r[1]} {r[2]}-{r[3]}  {r[4]}字  {r[5]}")
print("超过 5.6 字/秒的：", sum(1 for r in rows if r[0] > 5.6))
