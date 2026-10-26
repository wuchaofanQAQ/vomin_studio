# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

def scale_seg(seg_text, target):
    ms = list(re.finditer(r"【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】", seg_text))
    cur_total = float(ms[-1].group(3))
    durs = [round((float(m.group(3)) - float(m.group(2))) * target / cur_total, 1) for m in ms]
    durs[-1] = round(target - sum(durs[:-1]), 1)
    t0 = 0.0
    for m, d in zip(ms, durs):
        a, b = round(t0, 1), round(t0 + d, 1)
        seg_text = seg_text.replace(m.group(0), f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】", 1)
        seg_text = seg_text.replace(f"[{m.group(2)}s-{m.group(3)}s]，", f"[{a:g}s-{b:g}s]，")
        t0 = b
    return re.sub(r"## 【第\d+段｜\[0s-[\d.]+s\]", lambda mm: re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target}s]", mm.group(0)), seg_text)

for segno, target in ((2, 30), (3, 30)):
    a = s.index(f"## 【第{segno:02d}段")
    b = s.index("## 【第", a + 5) if segno != 3 else len(s)
    s = s[:a] + scale_seg(s[a:b], target) + s[b:]

open(f, "w", encoding="utf-8").write(s)
print("p02/p03 扩到 30s")
