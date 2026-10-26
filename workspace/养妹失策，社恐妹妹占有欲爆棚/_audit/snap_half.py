# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

parts = re.split(r"(?m)^(## 【第\d+段｜\[0s-(\d+)s\]｜.*?】)$", t)
out, i = [parts[0]], 1
while i < len(parts):
    head, dur, body = parts[i], int(parts[i + 1]), parts[i + 2]
    shots = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】", body))
    durs = []
    for m in shots:
        d = float(m.group(3)) - float(m.group(2))
        s = max(1.0, round(d * 2) / 2)
        durs.append(s)
    diff = dur - sum(durs)
    durs[-1] = round(durs[-1] + diff, 1)
    assert durs[-1] >= 1.0
    t0 = 0.0
    for m, d in zip(shots, durs):
        a, b = round(t0, 1), round(t0 + d, 1)
        t0 = b
        body = body.replace(f"【镜头{int(m.group(1)):02d}｜[{m.group(2)}s-{m.group(3)}s]｜{m.group(4)}】",
                            f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】", 1)
        body = body.replace(f"[{m.group(2)}s-{m.group(3)}s]，", f"[{a:g}s-{b:g}s]，", 1)
    out += [head, body]
    i += 3
open(f, "w", encoding="utf-8").write("".join(out))
print("已对齐 0.5 秒网格")
