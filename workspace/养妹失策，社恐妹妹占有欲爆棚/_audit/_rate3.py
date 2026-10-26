import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\鍏诲澶辩瓥锛岀ぞ鎭愬濡瑰崰鏈夋鐖嗘"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v13.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
rows = []
cur = 0
for ln in md.splitlines():
    m = re.match(r"^## 銆愮(\d+)娈?, ln)
    if m:
        cur = int(m.group(1)); continue
    mm = re.match(r"^(" + T + r")-(" + T + r")锛?.+?)锛?.+)$", ln.strip())
    if not mm: continue
    d = max(sec(mm.group(2)) - sec(mm.group(1)), 1e-6)
    n = len(re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4)))
    rows.append((n / d, cur, mm.group(1), mm.group(2), n))
print("鎬昏鏁?", len(rows), "| 瓒呰繃 5.4 瀛?绉?", sum(1 for r in rows if r[0] > 5.4))
for r in sorted(rows, reverse=True)[:6]:
    print(f"  {r[0]:4.1f} 瀛?绉? 娈祘r[1]} {r[2]}-{r[3]}  {r[4]}瀛?)
