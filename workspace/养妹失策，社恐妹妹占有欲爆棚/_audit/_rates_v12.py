import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\鍏诲澶辩瓥锛岀ぞ鎭愬濡瑰崰鏈夋鐖嗘"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v12.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
rows = []
cur = None
for ln in md.splitlines():
    m = re.match(rf"^## 銆愮(\d+)娈?, ln)
    if m: cur = int(m.group(1)); continue
    mm = re.match(rf"^({T})-({T})锛?.+?)锛?.+)$", ln.strip())
    if not mm: continue
    d = max(sec(mm.group(2)) - sec(mm.group(1)), 1e-6)
    n = len(re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4)))
    rows.append((n/d, cur, mm.group(1), mm.group(2), n, mm.group(3)[:14]))
rows.sort(reverse=True)
print("鏈€鎱?5 鍙ワ細")
for r in rows[:5]: print(f"  {r[0]:4.1f} 瀛?绉? 娈祘r[1]} {r[2]}-{r[3]}  {r[4]}瀛? {r[5]}")
print("鏈€蹇?5 鍙ワ細")
for r in rows[-5:]: print(f"  {r[0]:4.1f} 瀛?绉? 娈祘r[1]} {r[2]}-{r[3]}  {r[4]}瀛? {r[5]}")
print("瓒呰繃 5.6 瀛?绉掔殑锛?, sum(1 for r in rows if r[0] > 5.6))
