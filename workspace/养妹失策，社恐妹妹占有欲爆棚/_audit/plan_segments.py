# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
md = open(f, encoding="utf-8").read()

parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    body = parts[i+1]
    for m in re.finditer(r"(?ms)^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.+?)(?=\n\n|\Z)", body):
        txt = m.group(3)
        chars = 0
        for ln in txt.split("\n"):
            mm = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", ln.strip())
            if mm: chars += len(mm.group(1))
        action = re.split(r"[。]", txt.split("\n")[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
        e_act = min(3.4, 0.5 + 0.8 * max(1, clauses))
        e_dlg = chars / 4.8 + 0.3 if chars else 0
        rows.append({"seg": int(re.search(r"第(\d+)段", parts[i]).group(1)),
                     "no": int(m.group(1)), "title": m.group(2), "chars": chars,
                     "clauses": clauses, "exp": round(max(1.0, e_act, e_dlg), 1)})

total = sum(r["exp"] for r in rows)
print("镜数", len(rows), "按公式总时长", round(total, 1), "s")
# 按顺序打包成 ≤30s 的段，遇到关键切点优先断
cuts = {6, 17, 31}  # 顶配后 / 你爸呢后 / 进不进后
segs, cur, acc = [], [], 0.0
for r in rows:
    if cur and (acc + r["exp"] > 30 or (len(cur) and r["no"] - 1 in cuts and acc >= 12)):
        segs.append((cur, round(acc, 1))); cur, acc = [], 0.0
    cur.append(r); acc += r["exp"]
if cur: segs.append((cur, round(acc, 1)))
for i, (s, d) in enumerate(segs, 1):
    print(f"第{i}段 {d}s / {len(s)}镜 / {s[0]['title']} → {s[-1]['title']}")
