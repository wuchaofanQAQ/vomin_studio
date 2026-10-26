# -*- coding: utf-8 -*-
import re, math
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

shots = []
for m in re.finditer(r"(?ms)^【镜头\d+｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\n## |\Z)", t):
    blk = m.group(4).strip()
    lines = [l for l in blk.split("\n") if l.strip()]
    shots.append({"title": m.group(3), "dur0": round(float(m.group(2)) - float(m.group(1)), 1),
                  "body": "\n".join(l for l in lines if not l.startswith("[")),
                  "dlg": [l for l in lines if l.startswith("[")]})
print("镜数", len(shots))

GROUPS = [(0, 14), (14, 26), (26, 30), (30, len(shots))]
NAMES = ["走廊·我是沈幼怡", "走廊·我这儿不是民宿", "走廊·进不进", "玄关客厅·你哥哥会照顾好你的"]

out = []
for gi, (a, b) in enumerate(GROUPS, 1):
    g = shots[a:b]
    durs = [3.0 if s["title"] == "拎箱子" else s["dur0"] for s in g]
    raw = sum(durs)
    dur = int(math.ceil(raw))
    delta = round(dur - raw, 1)
    if delta:
        durs[-1] = round(durs[-1] + delta, 1)
    out.append(f"## 【第{gi:02d}段｜[0s-{dur}s]｜{NAMES[gi-1]}】\n")
    # 段落内容从模板拼接（见下方常量）
    out.append("__SEG__" + str(gi) + "\n")
    t0 = 0.0
    for idx, (s, d) in enumerate(zip(g, durs), 1):
        a2, b2 = round(t0, 1), round(t0 + d, 1); t0 = b2
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a2:g}s-{b2:g}s]", dl)
        out.append(f"【镜头{idx:02d}｜[{a2:g}s-{b2:g}s]｜{s['title']}】\n{body}\n")
    out.append("__FINAL__" + str(gi) + "\n")

open(f + ".tmp", "w", encoding="utf-8").write("\n".join(out))
print("结构骨架完成:", [(b-a, ) for a, b in GROUPS])
