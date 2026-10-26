import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
durs = [float(b) - float(a) for a, b in re.findall(r"【镜头\d+｜\[([\d.]+)s-([\d.]+)s\]", md)]
import collections
buckets = collections.Counter()
for d in durs:
    if d <= 1: buckets["≤1s"] += 1
    elif d <= 2: buckets["1-2s"] += 1
    elif d <= 3.5: buckets["2-3.5s"] += 1
    elif d <= 5: buckets["3.5-5s"] += 1
    else: buckets[">5s"] += 1
print("镜数:", len(durs), "| 最短", min(durs), "| 最长", max(durs), "| 平均", round(sum(durs)/len(durs), 2))
for k in ["≤1s", "1-2s", "2-3.5s", "3.5-5s", ">5s"]:
    print(f"  {k}: {buckets[k]}")
