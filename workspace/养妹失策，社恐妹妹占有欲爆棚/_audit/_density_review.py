# -*- coding: utf-8 -*-
import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
segs = re.split(r"(?m)^## (\u3010\u7b2c\d+\u6bb5.*?\u3011)\s*$", md)
print(f"{'段':>2} {'镜':>3} {'时长':>5} {'分句':>3} {'句/秒':>5} {'台词':>4}  标题")
flags = []
for i in range(1, len(segs), 2):
    head, body = segs[i], segs[i + 1]
    sno = re.match(r"\u3010\u7b2c(\d+)\u6bb5", head).group(1)
    blocks = re.split(r"(?m)^\u3010\u955c\u5934(\d+)\uff5c\[([\d.]+)s-([\d.]+)s\]\uff5c(.+?)\u3011$", body)
    for j in range(1, len(blocks), 5):
        no, a, b, title, txt = blocks[j], blocks[j+1], blocks[j+2], blocks[j+3], blocks[j+4]
        dur = float(b) - float(a)
        lines = [l for l in txt.splitlines() if l.strip()]
        desc = [l for l in lines if not l.startswith("[")]
        dlg = [l for l in lines if l.startswith("[")]
        body_line = " ".join(desc)
        clauses = [c for c in re.split(r"[；。]", body_line) if len(c.strip()) > 4]
        n = max(len(clauses) - 1, 1)
        rate = n / dur if dur else 0
        dchars = sum(len(re.sub(r"[^\u4e00-\u9fff]", "", d)) for d in dlg)
        print(f"{sno:>2} {no:>3} {dur:>5.1f} {n:>3} {rate:>5.1f} {dchars:>4}  {title[:12]}")
        if rate > 3.2 or (rate < 1.0 and dur >= 2):
            flags.append((sno, no, dur, n, rate, title))
print("\n可疑:", len(flags))
for f in flags:
    print("  ", f)
